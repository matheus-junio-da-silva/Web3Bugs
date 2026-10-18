#!/usr/bin/env python3
"""Radicle Drips P23: historical literal CVL catalog, never migration or new proof."""
import re,csv,io,hashlib,shutil,subprocess,sys
from pathlib import Path
from collections import Counter
BT=chr(96)
SRC_SHA="687f654c679ed45ab127b7949e2a29c8f5e491b9"
NAMES=["DripsHub.spec","DripsHubBackup.spec","Reserve.spec","SlotTester.spec","Splits.spec","Splits2.spec"]
EXPECTED=[12,6,5,1,17,5]
VERIFIED="correctnessOfSplitResults correctnessOfSplit integrityOfCollect revertCharacteristicsOfCollect correctnessOfGive splittableOfNonReceiverNotAffectedByGive correctnessOfHashSplits integrityOfSplit assetsDoNotInterfereEachOther moneyNotLostOrCreatedDuringSplit sameReturnOfSplitAndSplitResults equalSplitWeightsResultEqualSplittableIncrease cannotFrontRunSplitDifferentUsers cannotFrontRunSplitTwoSameUsers cannotFrontRunSplitThreeSameUsers".split()
REPORT_NAMES=set(VERIFIED+["splitReceiverShouldGetMoneyUponSplit","cannotFrontRunSplitGeneralCase"])
REASON={
"DripsHub.spec":"Original using DripsHubHarness as DH requires missing DripsHubHarness.sol; symbolic getDripsReceiverLocalArr, getRelevantStateVars and helperUpdateReceiverStates require its CVT wrappers. Production DripsHub.sol does not implement DH, and the historical external-library source/run configuration is not present.",
"DripsHubBackup.spec":"Original using UpdateReceiverStatesHarness as DH requires missing UpdateReceiverStatesHarness.sol, DH.DripsReceiver struct, _helperUpdateReceiverStates, unpackArgs and other harness methods. The primary DripsHubHarness is not a substitute. Original run configuration and vendor imports are absent.",
"Reserve.spec":"ReserveHarness, DummyERC20Impl, DummyERC20A, DummyERC20B, getDeposited/getIsUser adapters, token models and plugin callback configuration used in this spec are missing. Production Reserve.sol alone does not implement them. External imports are absent.",
"SlotTester.spec":"The snapshot does not include SlotTester target or getters getPausedSlot and get_storageSlot in the specified test environment. Managed.pausedSlot and DripsHub._storageSlot are contextual implementations, not a replacement for a missing slot harness.",
"Splits.spec":"The abstract Splits.sol exposes internal _split, _splitResults, _splittable, _collectable, _give and _hashSplits, but the spec invokes missing CVT generated callable wrappers and receiver-array harness getters (getCurrSplitsReceiverLocalArr, getCurrSplitsReceiverLocaLength). No wrapper target or verification configuration is in src/. DripsHub public ABI differs.",
"Splits2.spec":"Distinct Splits2.spec uses absent generated CVT wrappers and receiver-array getters for internal Splits.sol functions. Its similarly named rules do NOT inherit formal results from Splits.spec, and public DripsHub.split is not the missing target.",
}
TARGET={
"DripsHub.spec":"DripsHubHarness (missing; DripsHub.sol contextual)",
"DripsHubBackup.spec":"UpdateReceiverStatesHarness (missing; backup)",
"Reserve.spec":"ReserveHarness (missing; Reserve.sol contextual)",
"SlotTester.spec":"UNSPECIFIED SlotTester harness (missing)",
"Splits.spec":"CVT internal Splits target (missing; Splits.sol contextual)",
"Splits2.spec":"CVT internal Splits target (missing; distinct spec)",
}
FUNC={
"splitResults":("Splits.sol","_splitResults"),"split":("Splits.sol","_split"),
"splittable":("Splits.sol","_splittable"),"collectable":("Splits.sol","_collectable"),
"give":("Splits.sol","_give"),"collect":("Splits.sol","_collect"),
"hashSplits":("Splits.sol","_hashSplits"),"setSplits":("Splits.sol","_setSplits"),
"receivableDrips":("Drips.sol","_receivableDrips"),"receiveDrips":("Drips.sol","_receiveDrips"),
"setDrips":("Drips.sol","_setDrips"),"helperUpdateReceiverStates":("Drips.sol","_updateReceiverStates"),
"_helperUpdateReceiverStates":("Drips.sol","_updateReceiverStates"),
"_dripsState":("Drips.sol","_dripsState"),"totalBalance":("DripsHub.sol","totalBalance"),
"deposit":("Reserve.sol","deposit"),"withdraw":("Reserve.sol","withdraw"),
"getDeposited":("Reserve.sol","deposited"),"getIsUser":("Reserve.sol","isUser"),
"getPausedSlot":("Managed.sol","pausedSlot"),"get_storageSlot":("DripsHub.sol","_storageSlot")
}
FALLBACK={
"DripsHub.spec":[("DripsHub.sol","totalBalance"),("Drips.sol","_updateReceiverStates")],
"DripsHubBackup.spec":[("Drips.sol","_updateReceiverStates"),("Drips.sol","_dripsState")],
"Reserve.spec":[("Reserve.sol","deposit"),("Reserve.sol","withdraw")],
"SlotTester.spec":[("Managed.sol","pausedSlot"),("DripsHub.sol","totalBalance")],
"Splits.spec":[("Splits.sol","_split"),("Splits.sol","_splittable")],
"Splits2.spec":[("Splits.sol","_split"),("Splits.sol","_splittable")]
}
FIELDS=["Project ID","Status","Example ID","Bug Label","Property","Result","Detection Outcome","Target Contract","Spec","Code","Documentation","Incomplete Reason","Original Spec","Original Spec Lines","Original Contract","Original Contract Lines","Detection Intent"]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def mask(s):
 """Mask comments and string literals while retaining byte offsets and newlines."""
 o=list(s);i=0;m=""
 while i<len(s):
  c=s[i];pair=s[i:i+2]
  if m=="//":
   if c=="\n":m=""
   else:o[i]=" "
  elif m=="/*":
   if pair=="*/":o[i]=o[i+1]=" ";i+=2;m="";continue
   elif c!="\n":o[i]=" "
  elif m=='"':
   if pair.startswith("\\") and i+1<len(s):o[i]=o[i+1]=" ";i+=2;continue
   if c=='"':m=""
   if c!="\n":o[i]=" "
  elif pair=="//":o[i]=o[i+1]=" ";i+=2;m="//";continue
  elif pair=="/*":o[i]=o[i+1]=" ";i+=2;m="/*";continue
  elif c=='"':o[i]=" ";m='"'
  i+=1
 return "".join(o)
def extract(path):
 s=path.read_text(encoding="utf-8");m=mask(s)
 starts=list(re.finditer(r"(?m)^[ \t]*(rule|invariant)[ \t]+([A-Za-z_]\w*)\b",m))
 items=[]
 for mt in starts:
  op=m.find("{",mt.end());assert op>=0
  # A filtered{ f -> ... } method filter precedes the rule body: it is
  # NOT itself the rule body. Preserve its text, then scan the next brace.
  if re.search(r"\bfiltered\s*$",m[mt.end():op]):
   dep=1;k=op+1
   while k<len(m) and dep:
    if m[k]=="{":dep+=1
    if m[k]=="}":dep-=1
    k+=1
   assert dep==0,(path,mt.group(2),"unclosed filtered")
   op=m.find("{",k);assert op>=0,(path,mt.group(2),"no body after filtered")
  d=0;end=None
  for i in range(op,len(m)):
   if m[i]=="{":d+=1
   if m[i]=="}":
    d-=1
    if d==0:end=i+1;break
  assert end is not None
  block=s[mt.start():end];sm=mask(block)
  assert re.search(r"\bassert\b",sm),(path,mt.group(2))
  items.append(dict(file=path.name,name=mt.group(2),start=s.count("\n",0,mt.start())+1,
      end=s.count("\n",0,end-1)+1,block=block,asserts=re.findall(r"\bassert\b.*?;",sm,re.S),
      reqs=re.findall(r"\brequire\b.*?;",sm,re.S),
      calls=[k for k in FUNC if re.search(r"\b"+re.escape(k)+r"\s*\(",sm)]))
 return items, s[:starts[0].start()] if starts else s
def snippet(src,filename,method):
 f=src/"src"/filename
 s=f.read_text(encoding="utf-8")
 l=s.splitlines(keepends=True)
 matches=list(re.finditer(r"\bfunction\s+"+re.escape(method)+r"\s*\(",s))
 sm=mask(s)
 mat=next((mt for mt in matches if (lambda op,semi: op>=0 and (semi<0 or op<semi))(sm.find("{",mt.end()),sm.find(";",mt.end()))),None)
 if mat:
  op=sm.find("{",mat.end())
  d=0;end=None
  for i in range(op,len(sm)):
   if sm[i]=="{":d+=1
   elif sm[i]=="}":
    d-=1
    if d==0:end=i+1;break
  if end is None:return None
  start=max(1,s.count("\n",0,mat.start())-1)
  last=s.count("\n",0,end-1)+1
 else:
  pos=next((i+1 for i,ln in enumerate(l) if re.search(r"\b"+re.escape(method)+r"\b",ln)),None)
  if not pos:return None
  start=max(1,pos-2);last=min(len(l),pos+2)
 return filename,start,last,"".join(l[start-1:last])
def source_context(p,clips):
 name=p["name"];n=p["file"];s=" "
 if n.startswith("Splits"):
  s="The central storage is SplitsStorage.splitsStates[userId].balances[assetId] with splittable/collectable credits; _splitResults computes weight allocation, _split debits splittable, credits receivers and moves splitter amounts to collectable. _give credits receiver splittable; _collect decreases collectable. _hashSplits reads receiver ID/weight arrays. Only operations actually invoked in the original rule define its obligation."
 elif n.startswith("DripsHub"):
  s="DripsStorage.states[userId][assetId] contains per-user balance, last update, nextReceivableCycle, and amtDeltas. _updateReceiverStates alters cycle deltas. DripsHubStorage.totalBalances holds per-token aggregate balances. The source's DH harness and nondeterministic summaries affect what these assertions cover."
 elif n=="Reserve.spec":
  s="Reserve.deposited[token] records tracked token balances; isUser gates deposits/withdrawals and plugins[token] governs external callbacks. Reserve.deposit/withdraw alter accounting through IERC20 transfers, which require missing modeled tokens."
 else:
  s="Managed.pausedSlot, DripsHub._storageSlot and DripsHubStorage.totalBalances live in distinct storage contexts. The rule reads specialized getPausedSlot/get_storageSlot wrappers absent from the snapshot."
 return s+" Contextual excerpt targets: "+", ".join(f+" lines "+str(a)+"-"+str(b) for f,a,b,_ in clips)+"."
def category(p):
 n=p["name"];f=p["file"]
 if n.startswith("sanity") or n=="helperTest" or n.startswith("whoChanged"):
  return "UNMAPPED","Unrestricted method-mutation/sanity diagnostic rather than an asserted prohibited security transition"
 if n=="splitReceiverShouldGetMoneyUponSplit":return "L2","Receiver's weighted share can round to zero under integer division"
 if n=="correctnessOfHashSplits":return "LA","Hash equality should imply consistent splits receiver IDs and weights"
 if n.startswith("cannotFrontRunSplit"):return "SE-1","Unexpected interleaving/sequence causes subsequent split to revert"
 if n.startswith("revertCharacteristics"):return "L8","Unexpected revert from split/collect under the rule's environmental assumptions"
 if f=="Reserve.spec" and n=="tokensNonInterference":return "S3-2","Mutation of independent token accounting during unrelated operation"
 if "NonReceiver" in n or "Interfere" in n:return "S3-2","Unexpected update of an unrelated user's or asset's accounting"
 return "S6-4","Conservation, receivable/collectable balances, or exact split/remainder accounting"
def status(p):
 if p["file"]!="Splits.spec":return "NOT_STATED","NOT_STATED"
 if p["name"]=="splitReceiverShouldGetMoneyUponSplit":return "VIOLATED","FINDING"
 if p["name"]=="cannotFrontRunSplitGeneralCase":return "NOT_STATED","INCONCLUSIVE"
 if p["name"] in VERIFIED:return "VERIFIED","NO_FINDING"
 raise RuntimeError("Unmapped report rule "+p["name"])
def counterexample(p):
 n=p["name"]
 if n.startswith("sanity") or n=="helperTest":
  return "A reachable execution reaches assert false, intentionally failing as a sanity test; not evidence of a vulnerability."
 if n.startswith("whoChanged"):
  return "Choose any legal method f that updates the monitored field and falsifies the unconditional pre/post equality; without permitted-writer exclusions this is diagnostic, not necessarily a defect."
 if n=="splitReceiverShouldGetMoneyUponSplit":
  return "Positive splitter balance times receiver weight divided by 1,000,000 rounds down to zero, leaving the receiver with no new splittable tokens. The original PDF explicitly reports this violation."
 if n.startswith("cannotFrontRunSplit"):
  return "The second split call reverts after the first split changes state, despite assert !lastReverted. The rule's exact user-ID and balance bounds must be satisfied and cannot be dropped."
 if n=="correctnessOfHashSplits":return "Distinct receiver arrays produce equal hash, violating the asserted relation between hash and selected list data; depends on symbolic-array semantics."
 return "After the rule's specified transfer, split, collection, or drips update, an observed accounting, storage or return value contradicts at least one original assert. This is a hypothetical falsifying state, not a new solver result."
def doc(p,clips,label,intent,result,outcome,specsha):
 n=p["name"];f=p["file"];src="contracts/23/specs/"+f
 s="# Example "+str(p["id"])+" — "+BT+n+BT+"\n\n"
 s+="## Provenance and target\n- CVL: "+BT+src+BT+" lines "+str(p["start"])+"-"+str(p["end"])+"; SHA256 "+BT+specsha+BT+".\n"
 s+="- Exact historical target: **"+TARGET[f]+"**. Production excerpts are contextual, not a substitute.\n"
 s+="- Status: incomplete. Result: "+result+". Detection Outcome: "+outcome+". Bug Label: "+BT+label+BT+".\n\n"
 s+="## Detection intent\n"+intent+". The classification follows the executable assertions rather than the property name alone.\n\n"
 s+="## Executable assertion(s)\n"
 for i,a in enumerate(p["asserts"],1):s+=str(i)+". "+BT+" ".join(a.split()).replace(BT,"")[:800]+BT+"\n"
 s+="\n## Why the Solidity excerpt is relevant\n"+source_context(p,clips)+"\n\n"
 s+="The original CVL calls/read-set identified by direct lexical analysis are: "+(", ".join(BT+x+BT for x in p["calls"]) if p["calls"] else "none of the mapped operation names")+". The excerpt preserves source line intervals and must be read alongside each assertion and its storage changes; same-named production functions may have different argument signatures from the missing CVT wrappers.\n\n"
 s+="## Hypothetical counterexample\n"+counterexample(p)+"\n\n"
 s+="## Assumptions and soundness\n"
 if p["reqs"]:
  s+="Actual CVL require statements:\n"+"\n".join("- "+BT+" ".join(x.split()).replace(BT,"")[:500]+BT for x in p["reqs"])+"\n"
 else:s+="No explicit active require statements in the property; the spec's methods and summaries can still restrict its reachability.\n"
 if f.startswith("DripsHub"):s+="Historical spec has methods summaries using NONDET/CONSTANT/DISPATCHER and DH harness, potentially diverging from production; preserve their semantics and distinguish main/backup.\n"
 if f=="Reserve.spec":s+="External token dispatchers and nondeterministic plugin callbacks are part of the proof abstraction, not concrete deployed token behavior.\n"
 s+="Original report pp. 2–3 limits loops to two iterations, bounds selected balances by 2^128, and restricts split weights in some rules. These report-level assumptions are not automatically present in other targets; only the source's actual requires constrain the extracted rule.\n\n"
 s+="## Missing dependency / incomplete reason\n"+REASON[f]+"\nThe provided snapshot cannot reproduce the exact target. No invented helper, guessed vendor version, or CVL syntax rewrite is inserted.\n\n"
 s+="## Historical Result evidence\n"
 if f=="Splits.spec":
  if result=="VERIFIED":s+="Report pp. 3–6 individually marks this source rule verified. This does not imply independent standalone re-verification.\n"
  elif result=="VIOLATED":s+="Report p. 5 marks this rule violated; report pp. 1–2 details an informational rounding issue and the project's response. Detection Outcome FINDING reflects this documented issue, despite the project's view that changing the design is unjustified.\n"
  else:s+="Report pp. 5–6 explicitly marks the unconstrained general case timed out; Result NOT_STATED (not formally proved/disproved), Detection Outcome INCONCLUSIVE. The three restricted sibling rules are separate verified obligations.\n"
 else:
  s+="The PDF expressly limits the reviewed formal scope to Splits.sol. It provides NO individual Result for "+f+"::"+n+"; do not transfer a result from similarly named rules in Splits.spec.\n"
 return s
def main():
 if len(sys.argv)!=3:raise SystemExit("Usage: generator.py source_project_root Web3Bugs-certora")
 src=Path(sys.argv[1]).resolve();dst=Path(sys.argv[2]).resolve()
 assert sorted(p.name for p in (src/"src").glob("*.sol"))==sorted(["AddressApp.sol","Drips.sol","DripsHub.sol","Managed.sol","Reserve.sol","Splits.sol"])
 assert all((src/"specs"/n).exists() for n in NAMES)
 assert subprocess.check_output(["git","-C",str(src),"rev-parse","HEAD"],text=True).strip()==SRC_SHA
 project=dst/"contracts/23"
 assert not project.exists() or (project/"specs/DripsHub.spec").exists(),"Project 23 already occupied"
 for sub in ("src","specs"):shutil.copytree(src/sub,project/sub,dirs_exist_ok=True)
 resources=dst/"resources/23";resources.mkdir(parents=True,exist_ok=True)
 pdf=src/"Formal_Verification_Report_of_Radicle_Drips_Contracts.pdf"
 shutil.copy2(pdf,resources/pdf.name)
 pages=[x for x in subprocess.check_output(["pdftotext","-layout",str(pdf),"-"]).decode("utf-8").split("\f") if x.strip()]
 assert len(pages)==6,len(pages)
 report="# Formal Verification Report of Radicle Drips Contracts\n\nThe exact PDF at resources/23/ is authoritative. This page-separated layout-preserving extraction is historical documentation, not a new proof.\n\n"
 for i,txt in enumerate(pages,1):
  report+="## Original PDF page "+str(i)+"\n\n~~~text\n"+txt.rstrip("\n")+"\n~~~\n\n"
 (dst/"reports/23.md").write_text(report.rstrip()+"\n",encoding="utf-8")
 properties=[];preludes={};counts={}
 for n in NAMES:
  found,pre=extract(src/"specs"/n)
  counts[n]=len(found);preludes[n]=pre;properties+=found
 assert [counts[n] for n in NAMES]==EXPECTED,counts
 assert len(properties)==46
 assert set(p["name"] for p in properties if p["file"]=="Splits.spec")==REPORT_NAMES
 shutil.rmtree(dst/"results/spec/incomplete/23",ignore_errors=True)
 csvfile=dst/"results/spec/spec_buglabel.csv";existing=csvfile.read_bytes()
 existing=b"".join(line for line in existing.splitlines(keepends=True) if not line.startswith(b"23,"))
 eol="\r\n" if b"\r\n" in existing else "\n"
 records=list(csv.DictReader(io.StringIO(existing.decode("utf-8"))))
 assert list(records[0])==FIELDS
 assert not any(r["Project ID"].strip()=="23" for r in records)
 destrows=[];matrix=[]
 for index,p in enumerate(properties,1):
  p["id"]=index
  label,intent=category(p);result,outcome=status(p)
  base="results/spec/incomplete/23/"+str(index)
  path=dst/base;path.parent.mkdir(parents=True,exist_ok=True)
  digest=sha(src/"specs"/p["file"])
  # Entire shared prelude preserves the original methods/summaries and
  # referenced CVL definitions with transitive call effects.
  extracted="// Project 23 exact historical source: "+p["file"]+"\n// Property "+p["name"]+" original lines "+str(p["start"])+"-"+str(p["end"])+" SHA256 "+digest+"\n"
  extracted+=preludes[p["file"]].rstrip("\n")+"\n\n"+p["block"]
  (dst/(base+".spec")).write_text(extracted.rstrip("\n")+"\n",encoding="utf-8")
  chosen=[]
  for call in p["calls"]:
   pair=FUNC[call]
   if pair not in chosen:chosen.append(pair)
  for pair in FALLBACK[p["file"]]:
   if pair not in chosen:chosen.append(pair)
  snippets=[]
  for fname,fn in chosen[:6]:
   found=snippet(src,fname,fn)
   if found and not any((a[0],a[1],a[2])==(found[0],found[1],found[2]) for a in snippets):snippets.append(found)
  assert snippets,(p["file"],p["name"])
  sol="".join("// Original: contracts/23/src/"+f+" lines "+str(a)+"-"+str(b)+"\n"+t.rstrip("\n")+"\n\n" for f,a,b,t in snippets).rstrip("\n")+"\n"
  (dst/(base+".sol")).write_text(sol,encoding="utf-8")
  (dst/(base+".md")).write_text(doc(p,snippets,label,intent,result,outcome,digest),encoding="utf-8")
  (dst/(base+".txt")).write_text("Missing historical dependency: "+p["file"]+"::"+p["name"]+"\n"+REASON[p["file"]]+"\n",encoding="utf-8")
  destrows.append(dict(zip(FIELDS,["23","incomplete",str(index),label,p["name"],result,outcome,TARGET[p["file"]],base+".spec",base+".sol",base+".md",base+".txt","contracts/23/specs/"+p["file"],str(p["start"])+"-"+str(p["end"]),"; ".join("contracts/23/src/"+f for f,_,_,_ in snippets)," | ".join(f+":"+str(a)+"-"+str(b) for f,a,b,_ in snippets),intent])))
  matrix.append((p,label,result,outcome))
 # Write append-only CSV; preserve exact prior data and platform line endings.
 out=io.StringIO(newline="");writer=csv.DictWriter(out,fieldnames=FIELDS,lineterminator=eol);writer.writerows(destrows)
 csvfile.write_bytes(existing+(b"" if existing.endswith(b"\n") else eol.encode())+out.getvalue().encode("utf-8"))
 contests=dst/"results/contests.csv";old=contests.read_bytes()
 old=b"".join(line for line in old.splitlines(keepends=True) if not line.startswith(b"23,"))
 assert not any(re.match(rb"^23,",ln) for ln in old.splitlines())
 contests.write_bytes(old+(b"" if old.endswith(b"\n") else b"\n")+b"23,Radicle Drips,Streaming Payments,-,-,2023-01,-,-\n")
 docs="# Project 23 — Radicle Drips Historical CVL Catalog\n\n"
 docs+="## Source provenance\nPropertyGPT main commit "+BT+SRC_SHA+BT+". Source src tree "+BT+"344f4f303849c1337ff0369da66ab840a0a9f8a8"+BT+"; specs tree "+BT+"d7d6012139dbcdb76ce0430e48ed4fe67208aea3"+BT+"; original PDF blob "+BT+"cdadcf1b83b3dc1bfa267d958d8dfde739fd5154"+BT+"; PDF SHA256 "+BT+sha(pdf)+BT+". Preserved byte-for-byte in contracts/23/src, contracts/23/specs and resources/23.\n\n"
 docs+="## Active declaration inventory\n| Original spec | Active CVL declarations | Excluded |\n|---|---:|---|\n"
 for n in NAMES:
  exclusion={"DripsHub.spec":"two commented invariants","DripsHubBackup.spec":"two commented invariants","Splits.spec":"one commented sanity rule"}.get(n,"none")
  docs+="| "+n+" | "+str(counts[n])+" | "+exclusion+" |\n"
 docs+="\n**46 original active properties**, all incomplete against snapshot dependencies, independent of original result. CVL preserved literally without CVL2 migration. Repeated front-run property names in Splits/Splits2 are distinct declarations and not deduplicated. No CVT or target harness is invented.\n\n"
 docs+="## Historical proof result: only Splits.sol\nThe original report (December 2022 to January 2023; reviewed commit 6fe9d38) expressly limits formal scope to Splits.sol, with 15 named verified rules, one violated informational-rounding rule, and one timed-out general-case rule. The remaining 29 properties (DripsHub, backup, Reserve, SlotTester, Splits2) have NOT_STATED result. The timed-out case is NOT_STATED with INCONCLUSIVE outcome, not VERIFIED. The rounding issue yields VIOLATED/FINDING (informational finding), including the team's explicit design/economics response. Three constrained split front-running variants verified in Splits.spec are not evidence for Splits2.spec.\n\n"
 docs+="## Assumptions & soundness\n- The prover unrolled loops at most twice; behavior requiring longer loops was outside proven scope.\n- Some rules assume correctly set receiver weights (sum at most 1,000,000) based on _assertSplitsValid() logic.\n- Sums of balances/transfers were bounded below 2^128.\n- General front-running rule timed out; specialized identity cases were checked independently.\n- External contracts, dummy ERC20s, CVT-generated internal-operation wrappers, and the DripsHubHarness / UpdateReceiverStatesHarness / ReserveHarness are not in the six Solidity files; their generated verification semantics cannot be recovered from the production files alone.\n- Diagnostic sanity and unrestricted-method-mutation rules are UNMAPPED; apparent successful assertions in a soundness-limited model must not be called newly proved.\n\n"
 docs+="## Per-rule matrix\n| Example | Original spec range | Property | Label | Result | Outcome | Missing reason |\n|---:|---|---|---|---|---|---|\n"
 for p,l,r,o in matrix:
  docs+="| "+str(p["id"])+" | "+p["file"]+":"+str(p["start"])+"-"+str(p["end"])+" | "+p["name"]+" | "+l+" | "+r+" | "+o+" | "+REASON[p["file"]][:72]+"… |\n"
 docs+="\n## Reproduction\nThe generator copies all six src and all six spec files, extracts active declaration blocks using comment-aware brace matching, produces .spec, .sol, .md and .txt for each incomplete example, and performs immediate literal-property/source comparisons. The independent auditor checks source-to-destination blobs, CVL lines, snippets and CSV. Then run the three repository Python validators and git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD. The catalog is documentary, not a new Certora Prover run.\n"
 (dst/"docs/spec_catalog_project_23.md").write_text(docs,encoding="utf-8")
 for p,_,_,_ in matrix:
  assert p["block"] in (dst/("results/spec/incomplete/23/"+str(p["id"])+".spec")).read_text(encoding="utf-8")
 for sub in ("src","specs"):
  assert all(p.read_bytes()==(project/sub/p.relative_to(src/sub)).read_bytes() for p in (src/sub).rglob("*") if p.is_file())
 print("P23 COVERAGE "+str(counts));print("P23 TOTAL 46 incomplete 46")
 print("P23 RESULTS "+str(Counter(r for _,_,r,_ in matrix)))
 print("P23 OUTCOMES "+str(Counter(o for _,_,_,o in matrix)))
 print("P23 PDF SHA256 "+sha(pdf))
 for p,l,r,o in matrix:print("P23 PROPERTY",p["id"],p["file"],p["start"],p["end"],p["name"],l,r,o)
 print("P23 SOURCE LITERAL 46/46")
if __name__=="__main__":main()
