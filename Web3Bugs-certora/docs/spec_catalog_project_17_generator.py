#!/usr/bin/env python3
"""Project 17, deterministic historical source catalog generator.
Run inside a checkout of Web3Bugs with a matching PropertyGPT source checkout:
 python3 Web3Bugs-certora/docs/spec_catalog_project_17_generator.py PATH_TO_SOURCE_PROJECT Web3Bugs-certora
This is source extraction, not a CVL2 migration or a Certora Prover run.
"""
import csv
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

BT=chr(96)
FILES=[
 "compound.cvl","accrueInterest.cvl","borrowAndRepayFresh.cvl",
 "mintAndRedeemFresh.cvl","liquidateFresh.cvl","admin_setCollateralFactor.cvl",
 "_setMarketPriceOracle.cvl","general.cvl","frame.cvl","eip20.cvl",
 "_setMarketPolicyHook.cvl","maximillion.cvl","dummy.cvl",
]
MISSING={
 "compound.cvl":"The historical V1 MoneyMarket contract with supply(address,uint256), withdraw(address,uint256), _setOriginationFee, _setOracle and related ABI is absent; the Compound V2 CToken/Comptroller is not a substitute.",
 "accrueInterest.cvl":"The synthetic interestRateModelGetBorrowRate() wrapper declared in CVL is absent from the CToken/CErc20Certora ABI. The external rate-model call is not the same interface.",
 "admin_setCollateralFactor.cvl":"getCollateralFactorREMOVE_ME(address) and getMarketListedREMOVE_ME(address) are CVL workarounds for struct getters without implementations in the supplied Comptroller snapshot.",
 "_setMarketPriceOracle.cvl":"The historical _setMarketPriceOracle(address,address) entrypoint is absent; Comptroller._setPriceOracle(PriceOracle) is a different operation and the asserted market tuple is not available.",
 "_setMarketPolicyHook.cvl":"The historical _setMarketPolicyHook(address,address) and policyHook field of the asserted market tuple are missing from this Compound V2 Comptroller.",
}
PRIMARY_VERIFIED={
 ("accrueInterest.cvl","accrueInterest"),
 ("borrowAndRepayFresh.cvl","borrowFresh"),
 ("borrowAndRepayFresh.cvl","repayBorrowFresh"),
 ("mintAndRedeemFresh.cvl","mintFresh"),
 ("mintAndRedeemFresh.cvl","redeemFresh"),
 ("liquidateFresh.cvl","liquidateBorrowFresh"),
 ("liquidateFresh.cvl","seize"),
 ("eip20.cvl","transferFrom"),
 ("maximillion.cvl","repayBehalf"),
}
# An Appendix listing does not establish a per-instance result for other rules,
# especially the V1 compound.cvl, unconstrained frame probes and overlapping names.
SOURCE_TARGET={
 "compound.cvl":"Historical MoneyMarket V1 (missing)",
 "accrueInterest.cvl":"CToken (historical synthetic interest-rate wrapper)",
 "borrowAndRepayFresh.cvl":"CErc20Certora",
 "mintAndRedeemFresh.cvl":"CErc20Certora",
 "liquidateFresh.cvl":"CErc20Certora (linked CTokenCollateral)",
 "admin_setCollateralFactor.cvl":"Comptroller (historical helper ABI missing)",
 "_setMarketPriceOracle.cvl":"Historical Comptroller configuration (missing ABI)",
 "_setMarketPolicyHook.cvl":"Historical Comptroller configuration (missing ABI)",
 "general.cvl":"CErc20Certora (CompoundIgnoreExtCalls.spclnk)",
 "frame.cvl":"CToken (standalone frame probe; no spclnk)",
 "eip20.cvl":"CErc20Certora (EIP20.spclnk)",
 "maximillion.cvl":"MaximillionCertora (Maximillion.spclnk)",
}
SNIPPETS={
 "compound.cvl":[("contracts/Comptroller.sol","_setMaxAssets"),("contracts/CToken.sol","_setPendingAdmin")],
 "accrueInterest.cvl":[("contracts/CToken.sol","accrueInterest")],
 "borrowAndRepayFresh.cvl":[("contracts/CToken.sol","borrowFresh"),("contracts/CToken.sol","repayBorrowFresh"),("spec/formal/contracts/CErc20Certora.sol","borrowFreshPub")],
 "mintAndRedeemFresh.cvl":[("contracts/CToken.sol","mintFresh"),("contracts/CToken.sol","redeemFresh"),("spec/formal/contracts/CErc20Certora.sol","mintFreshPub")],
 "liquidateFresh.cvl":[("contracts/CToken.sol","liquidateBorrowFresh"),("contracts/CToken.sol","seize"),("spec/formal/contracts/CErc20Certora.sol","liquidateBorrowFreshPub")],
 "admin_setCollateralFactor.cvl":[("contracts/Comptroller.sol","_setCollateralFactor")],
 "_setMarketPriceOracle.cvl":[("contracts/Comptroller.sol","_setPriceOracle")],
 "_setMarketPolicyHook.cvl":[("contracts/Comptroller.sol","_supportMarket")],
 "general.cvl":[("contracts/CToken.sol","_setPendingAdmin"),("contracts/CToken.sol","_acceptAdmin"),("contracts/CToken.sol","_setComptroller")],
 "frame.cvl":[("contracts/CToken.sol","balanceOf"),("contracts/CToken.sol","borrowBalanceStored")],
 "eip20.cvl":[("contracts/CToken.sol","transferTokens"),("contracts/CToken.sol","transferFrom")],
 "maximillion.cvl":[("contracts/Maximillion.sol","repayBehalf"),("spec/formal/contracts/MaximillionCertora.sol","borrowBalance")],
}
ACTION_MAP={
 "accrueInterest":"accrueInterest",
 "borrowFresh":"borrowFresh",
 "repayBorrowFresh":"repayBorrowFresh",
 "mintFresh":"mintFresh",
 "mintFresh_extended":"mintFresh",
 "redeemFresh":"redeemFresh",
 "mintThenRedeem":"mintFresh",
 "liquidateBorrowFresh":"liquidateBorrowFresh",
 "seize":"seize",
 "transferFrom":"transferTokens",
 "repayBehalf":"repayBehalf",
}
def sha256(p):
 return hashlib.sha256(p.read_bytes()).hexdigest()
def linestr(xs):
 if not xs: return ""
 out=[]; beg=last=xs[0]
 for n in xs[1:]:
  if n==last+1: last=n
  else:
   out.append(str(beg) if beg==last else str(beg)+"-"+str(last))
   beg=last=n
 out.append(str(beg) if beg==last else str(beg)+"-"+str(last))
 return ";".join(out)
def parse_file(path):
 raw=path.read_text(encoding="utf-8")
 lines=raw.splitlines(keepends=True)
 assert lines and lines[0].strip()=="methods {" or path.name=="dummy.cvl", path
 if path.name=="dummy.cvl": return []
 method_end=next(i for i,x in enumerate(lines) if i>0 and x.strip()=="}")
 methods=lines[:method_end+1]
 starts=[i for i,line in enumerate(lines[method_end+1:],method_end+1) if re.match(r"^[A-Za-z_]\w*\s*\(",line)]
 props=[]
 for first in starts:
  name=re.match(r"^([A-Za-z_]\w*)\s*\(",lines[first]).group(1)
  last=next((k for k in range(first+1,len(lines)) if lines[k].strip()=="}" and lines[k].startswith("}")),None)
  assert last is not None,(path,name)
  block="".join(lines[first:last+1])
  # Every property has one historical named rule and at least one assertion.
  assert "static_assert" in block,(path,name)
  calls=set(re.findall(r"\b(?:sinvoke|invoke)\s+([A-Za-z_]\w*)\s*\(",block))
  keep=[(i+1,line) for i,line in enumerate(methods[1:-1],1) if re.match(r"\s*(?:/\*[^*]*\*/\s*)?([A-Za-z_]\w*)\s*\(",line) and re.match(r"\s*(?:/\*[^*]*\*/\s*)?([A-Za-z_]\w*)\s*\(",line).group(1) in calls]
  # Preserve each original methods line verbatim; no syntax modernization.
  extracted="methods {\n"+"".join(line for _,line in keep)+"}\n\n"+block
  assert block in extracted
  selected=[i for i,_ in keep]+list(range(first+1,last+2))
  props.append({"name":name,"source":path.name,"block":block,"extracted":extracted,
                "start":first+1,"end":last+1,"calls":calls,"decls":[i for i,_ in keep],
                "spec_lines":linestr(sorted(selected))})
 return props
def candidate_files(name):
 if name=="frame.cvl": return ["contracts/CToken.sol","contracts/CErc20.sol","spec/formal/contracts/CErc20Certora.sol"]
 if name=="maximillion.cvl": return ["contracts/Maximillion.sol","spec/formal/contracts/MaximillionCertora.sol"]
 if name=="general.cvl": return ["contracts/CToken.sol","contracts/CErc20.sol","spec/formal/contracts/CErc20Certora.sol"]
 if name=="admin_setCollateralFactor.cvl":return ["contracts/Comptroller.sol","contracts/ComptrollerStorage.sol"]
 if name.startswith("_setMarket"):return ["contracts/Comptroller.sol","contracts/ComptrollerStorage.sol"]
 if name=="compound.cvl":return ["contracts/Comptroller.sol"]
 return ["contracts/CToken.sol","contracts/CErc20.sol","spec/formal/contracts/CErc20Certora.sol","spec/formal/contracts/CTokenCollateral.sol"]
def abi_present(fname, files):
 esc=re.escape(fname)
 pat=re.compile(r"\bfunction\s+"+esc+r"\s*\(|\b"+esc+r"\s*(?:=|;)",re.M)
 return any(pat.search(text) for text in files.values())
def relevant_choice(prop):
 n=prop["name"];src=prop["source"]
 if src=="frame.cvl": return [("contracts/CToken.sol",n.replace("frame_",""))]
 if n in ACTION_MAP:
  fn=ACTION_MAP[n]
  sol="contracts/Maximillion.sol" if src=="maximillion.cvl" else "contracts/CToken.sol"
  return [(sol,fn)]
 if src=="compound.cvl":
  if "Admin" in n: return [("contracts/CToken.sol","_setPendingAdmin")]
  if "Oracle" in n:return [("contracts/Comptroller.sol","_setPriceOracle")]
  return SNIPPETS[src][:1]
 if n=="_setCollateralFactor":return SNIPPETS[src]
 if n=="_setMarketPriceOracle":return SNIPPETS[src]
 if n=="_setMarketPolicyHook":return SNIPPETS[src]
 if n in ("_setPendingAdmin","_acceptAdmin","invariantRequireAdminToChangeAdmin"):
  return [("contracts/CToken.sol","_setPendingAdmin"),("contracts/CToken.sol","_acceptAdmin")]
 if n=="_setComptroller":return [("contracts/CToken.sol","_setComptroller")]
 return SNIPPETS[src][:1]
def code_excerpt(source,prop):
 chunks=[];referenced=[]
 for path,fn in relevant_choice(prop):
  content=(source/path).read_text(encoding="utf-8").splitlines(keepends=True)
  pat=re.compile(r"\bfunction\s+"+re.escape(fn)+r"\s*\(")
  hits=[i for i,s in enumerate(content) if pat.search(s)]
  if not hits:
   # For an automatically generated public getter, include the exact storage declaration.
   hits=[i for i,s in enumerate(content) if re.search(r"\b"+re.escape(fn)+r"\b\s*(?:;|=)",s)]
  if not hits: continue
  start=hits[0]
  end=start
  if "function " in content[start]:
   opened=False;depth=0
   for ix in range(start,len(content)):
    s=re.sub(r"//.*","",content[ix])
    if "{" in s: opened=True
    depth+=s.count("{")-s.count("}")
    end=ix
    if opened and depth==0: break
    if ix>=start+190:break
  start=max(0,start-2)
  rel="contracts/17/"+path
  chunks.append("// Original: "+rel+" lines "+str(start+1)+"-"+str(end+1)+"\n"+"".join(content[start:end+1]))
  referenced.append((rel,str(start+1)+"-"+str(end+1)))
 if not chunks:
  raise RuntimeError("No relevant Solidity evidence: "+repr(prop))
 return "\n\n".join(chunks).rstrip("\n")+"\n",referenced
def classify(prop,source):
 fname=prop["source"];n=prop["name"];reason=MISSING.get(fname,"")
 files={x:(source/x).read_text(encoding="utf-8") for x in candidate_files(fname)}
 missing=[f for f in sorted(prop["calls"]) if f!="f" and not abi_present(f,files)]
 if missing and not reason:reason="CVL-called methods lack an implementation in the declared target and its included snapshot ABI: "+", ".join(missing)+"."
 if fname=="frame.cvl":
  # Probe asks which arbitrary method can mutate a field; no allowed-method partition.
  label="UNMAPPED";intent="Unrestricted frame/mutation diagnostic: identifies calls that can change "+n[6:]+", not a forbidden transition."
 elif fname.startswith("_set") or fname in ("compound.cvl","general.cvl","admin_setCollateralFactor.cvl"):
  label="S5-3";intent="Check administrative authorization and return/state transition conditions asserted by the historical CVL."
 elif fname=="accrueInterest.cvl":
  label="S6-3";intent="Check exact interest, borrow-index, reserves and outstanding-borrow arithmetic."
 else:
  label="S6-4";intent="Check recorded balance, supply, borrowing, reserve or settlement conservation/error behavior."
 # The report states aggregate verification for named entrypoints and includes
 # applicable source rules in the appendix. Never propagate that to variants.
 result="VERIFIED" if (fname,n) in PRIMARY_VERIFIED else "NOT_STATED"
 outcome="NO_FINDING" if result=="VERIFIED" else "NOT_STATED"
 return ("incomplete" if reason else "complete"),label,intent,result,outcome,reason,missing
def as_md(prop,status,label,intent,result,outcome,reason,missing,refs,sha):
 n=prop["name"];src=prop["source"];calls=", ".join(sorted(prop["calls"]))
 asserted=[x.strip()[:130] for x in prop["block"].splitlines() if "static_assert" in x]
 why=(
  "A counterexample selects environments and inputs satisfying the CVL prerequisites, executes the invoked entrypoint and obtains a post-state or result that falsifies at least one original static_assert. "
  "For an unrestricted frame rule, a normal write by an unconstrained method f can falsify old == new without being a security issue."
  if src=="frame.cvl" else
  "A counterexample selects valid symbolic inputs/environment constraints, invokes the specified historical entrypoint and demonstrates a return code or observed post-state inconsistent with the asserted authorization, balances, reserves, cash or borrow behavior."
 )
 line_names="; ".join(x[0]+" ("+x[1]+")" for x in refs)
 s="# Example "+str(prop["index"])+" — "+BT+n+BT+"\n\n"
 s+="## Status\n"+status+"; historical CVL/Specify retained, no CVL2 conversion. Result="+result+"; Detection Outcome="+outcome+".\n\n"
 s+="## Bug Label relationship\n"+BT+label+BT+": "+intent+"\n\n"
 s+="## Original sources\n- "+BT+"contracts/17/spec/formal/"+src+BT+" lines "+prop["spec_lines"]+"; source SHA-256 "+sha+".\n- Target: "+SOURCE_TARGET[src]+".\n- Solidity: "+line_names+".\n\n"
 s+="## Motivation\n"+intent+" The label refers to the executable assertion and does not automatically classify a historical finding.\n\n"
 s+="## Reconstructed methodology\nThe original block contains "+str(len(asserted))+" statement(s) beginning with static_assert, and invokes/observes: "+(calls or "(none)")+". "+why+"\n\n"
 s+="## Why the Solidity excerpt is relevant\nThe extracted functions or storage entries expose the state transitions read by the CVL (token balances, accountBorrows, totalSupply, totalBorrows, totalReserves, accrualBlockNumber or privileged admin fields as applicable). The cited code is historical context and not a replacement for absent verification wrappers. Inspect the precise source implementation before inferring a proof obligation.\n\n"
 s+="## Dependencies included\nThe extracted .spec includes only original method signatures called by this rule and its literal full property block. Linker .spclnk data, imported Solidity, dynamic method quantification, and environment assumptions remain separate historical configuration concerns.\n\n"
 if status=="incomplete":s+="## Missing dependencies\n"+reason+"\n\nThe issue is a missing target interface/implementation, not merely absent modern compiler or Certora Prover.\n\n"
 s+="## Historical outcome boundaries\n"
 if result=="VERIFIED":
  s+="The PDF executive summary (pages 2–3) explicitly states verification for this primary operation and the appendix includes the matching verification family. This is a reported historical achievement under the modeled harnesses; **it is not a fresh proof** of this extracted file, other targets, or variants.\n"
 else:
  s+="The PDF does not identify an individual completed outcome for this exact source-rule/target instance. Aggregate verification, similarly named appendices and bugs fixed before release are not automatically transferred to this rule.\n"
 s+="The PDF reports previous issues related to account roles, rounding/zero-output, ERC20 false-return behavior and Maximillion interest accrual; none is individually attributed as a new exploitable issue to this source block without evidence.\n"
 if src=="frame.cvl":s+="The source quantifies an unrestricted method f: asserting that no method can change this getter would generally be false for normal operations, so this is a mutation probe, not a normative invariant.\n"
 if src=="compound.cvl":s+="This source uses a V1-style MoneyMarket ABI unlike the Compound V2 contracts; do not conflate similarly named admin operations or PDF tables.\n"
 return s
def main():
 if len(sys.argv)!=3:
  raise SystemExit("Usage: generator.py source_project_dir Web3Bugs-certora")
 source=Path(sys.argv[1]).resolve()
 dest=Path(sys.argv[2]).resolve()
 assert (source/"spec/formal/compound.cvl").is_file()
 proj=dest/"contracts/17"
 assert not proj.exists() or (proj/"spec/formal/compound.cvl").is_file(), "Project 17 already occupied"
 # Verbatim historical source tree: contracts, formal specs/linkers and scenarios.
 for sub in ("contracts","spec"):
  shutil.copytree(source/sub,proj/sub,dirs_exist_ok=True,copy_function=shutil.copy2)
 pdf=source/"CompoundMoneyMarketV2Aug2019.pdf"
 resources=dest/"resources/17";resources.mkdir(parents=True,exist_ok=True)
 shutil.copy2(pdf,resources/pdf.name)
 # Extract textual report while keeping the original PDF authoritative for layout.
 rep=subprocess.run(["pdftotext","-layout",str(pdf),"-"],capture_output=True,check=True).stdout.decode("utf-8")
 pages=rep.split("\f")
 if pages and not pages[-1].strip():pages.pop()
 text="# Compound Money Market V2 — historical formal verification report\n\n"
 text+="Historical report reproduced as page-separated extracted text from "+BT+pdf.name+BT+". The source PDF in resources/17 is authoritative for tables, typography, proof scope and page numbers. Extraction is not a new audit.\n\n"
 for i,page in enumerate(pages,1):
  text+="## PDF page "+str(i)+"\n\n"+BT*3+"text\n"+page.rstrip()+"\n"+BT*3+"\n\n"
 (dest/"reports/17.md").write_text(text.rstrip("\n")+"\n",encoding="utf-8")
 # Exact active rule declarations in old Specify syntax, not CVL2's rule/invariant tokens.
 rules=[]
 for fn in FILES:
  rules+=parse_file(source/"spec/formal"/fn)
 assert len(rules)==41,("Unexpected active source count",len(rules))
 assert len(set((p["source"],p["start"]) for p in rules))==41
 hdr=dest/"results/spec/spec_buglabel.csv"
 raw=hdr.read_bytes()
 raw=b"".join(ln for ln in raw.splitlines(keepends=True) if not ln.startswith(b"17,"))
 newline="\r\n" if b"\r\n" in raw else "\n"
 fields=next(csv.reader([raw.decode("utf-8").splitlines()[0]]))
 expected=["Project ID","Status","Example ID","Bug Label","Property","Result","Detection Outcome","Target Contract","Spec","Code","Documentation","Incomplete Reason","Original Spec","Original Spec Lines","Original Contract","Original Contract Lines","Detection Intent"]
 assert fields==expected
 assert not any(row["Project ID"].strip()=="17" for row in csv.DictReader(io.StringIO(raw.decode("utf-8"))))
 outrows=[]
 summary=[]
 manifest=["# Project 17 — Compound Money Market V2\n",
           "Source: matheus-junio-da-silva/PropertyGPT, certora_projects/compound_moneymarket.\n",
           "Snapshot source SHA: "+subprocess.check_output(["git","-C",str(source),"rev-parse","HEAD"],text=True).strip()+".\n",
           "PDF SHA-256: "+sha256(pdf)+".\n\n",
           "Legacy Specify: exactly 41 executable top-level property blocks; alias .spclnk entries are configurations, not properties.\n",
           "Historical report gives aggregate assurances; source blocks are never treated as newly proved.\n\n",
           "## Per-property reconstruction\n\n"]
 for sub in ("complete","incomplete"):
  shutil.rmtree(dest/("results/spec/"+sub+"/17"),ignore_errors=True)
 for idx,p in enumerate(rules,1):
  p["index"]=idx
  status,label,intent,result,outcome,reason,missing=classify(p,source)
  base="results/spec/"+status+"/17/"+str(idx)
  full=dest/base;full.parent.mkdir(parents=True,exist_ok=True)
  sha=sha256(source/"spec/formal"/p["source"])
  header="// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/"+p["source"]+"\n"
  header+="// Rule "+p["name"]+" original lines "+str(p["start"])+"-"+str(p["end"])+"; SHA256 "+sha+"\n"
  header+="// Original legacy Specify/CVL syntax; not migrated to CVL2.\n"
  (dest/(base+".spec")).write_text(header+p["extracted"],encoding="utf-8")
  sol,refs=code_excerpt(source,p)
  (dest/(base+".sol")).write_text(sol,encoding="utf-8")
  (dest/(base+".md")).write_text(as_md(p,status,label,intent,result,outcome,reason,missing,refs,sha),encoding="utf-8")
  if reason:
   (dest/(base+".txt")).write_text("Historical dependency closure blocker for "+p["source"]+"::"+p["name"]+":\n"+reason+"\nCVL methods declared are not implementation evidence; no invented mock or CVL2 migration has been inserted.\n",encoding="utf-8")
  paths="; ".join(s for s,_ in refs); locs=" | ".join(l for _,l in refs)
  row=dict(zip(expected,["17",status,str(idx),label,p["name"],result,outcome,SOURCE_TARGET[p["source"]],base+".spec",base+".sol",base+".md",base+".txt" if reason else "","contracts/17/spec/formal/"+p["source"],p["spec_lines"],paths,locs,intent]))
  outrows.append(row)
  summary.append((p,status,reason,label,result))
  manifest.append("| "+str(idx)+" | "+p["source"]+":"+str(p["start"])+"-"+str(p["end"])+" | "+p["name"]+" | "+status+" | "+label+" | "+result+" | "+(reason.replace("|","/")[:120] if reason else "All called method selectors located in project snapshot")+" |\n")
 # Append only project-specific CSV records while preserving all original CSV bytes.
 f=io.StringIO(newline="")
 writer=csv.DictWriter(f,fieldnames=expected,lineterminator=newline)
 writer.writerows(outrows)
 suffix=f.getvalue().encode("utf-8")
 if raw and not raw.endswith((b"\n",b"\r")):raw+=newline.encode()
 hdr.write_bytes(raw+suffix)
 contest=dest/"results/contests.csv"
 craw=contest.read_bytes()
 craw=b"".join(ln for ln in craw.splitlines(keepends=True) if not ln.startswith(b"17,"))
 cnewline=b"\r\n" if b"\r\n" in craw else b"\n"
 assert not any(row.get("ID","").strip()=="17" for row in csv.DictReader(io.StringIO(craw.decode("utf-8"))))
 contest.write_bytes(craw+(b"" if craw.endswith(b"\n") else cnewline)+b"17,Compound Money Market V2,Money Market,-,-,2019-08,-,-"+cnewline)
 counts=Counter(s for _,s,_,_,_ in summary)
 manifest.insert(7,"Distribution: "+str(dict(counts))+". Historical outcomes: "+str(dict(Counter(p[4] for p in summary)))+".\n\n")
 manifest.append("\n## Snapshot preservation & second-review method\n\n")
 manifest.append("The source's contracts/, spec/formal/, scenario/ and .spclnk files are copied unchanged. Every extracted property block is asserted literally present in its N.spec; CVL method signatures come from the original methods block. This program independently recounts the same 41 top-level declarations and checks each assertion and copied literal block. Dynamic method f and historically absent helpers are never fabricated.\n")
 manifest.append("\n## PDF limitations and findings\n\nThe report summary pages 2–3 claim correctness for specified operations, under modular proof, synthetic Comptroller assumptions and ERC20 modeling. Earlier bugs fixed before release include zero-output exchange rounding, role constraints, false-return ERC20 assumptions and the Maximillion stored/current interest mistake. Those historical findings are not assigned mechanically to any individual CSV result or outcome. Appendix sources may differ from V2 snapshot or be named generically; see each example.\n")
 manifest.append("\n## Configurations and exclusions\n\nFive .spclnk files configure linked external contracts and targets; they do not introduce additional named properties. The dummy.cvl file has zero rules. .scen files and .scen.old are execution scenarios, not active CVL rule declarations. compound.cvl is preserved despite historical V1 ABI incompatibility; frame.cvl probes are included despite being diagnostic rather than normative.\n")
 manifest.append("\n## Reproduction\n\nRun the generator against the SHA-pinned PropertyGPT source with poppler-utils; then from Web3Bugs-certora execute python3 scripts/check_contracts.py ., python3 scripts/check_contests_csv.py ., python3 scripts/check_specs.py . and repository-root git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD. No Certora prover rerun is asserted.\n")
 manifest.insert(8,"\n| # | CVL declaration | Property | Status | Label | Result | Provenance/dependency note |\n|---:|---|---|---|---|---|---|\n")
 (dest/"docs/spec_catalog_project_17.md").write_text("".join(manifest),encoding="utf-8")
 # Integrity pass across both full source and all 41 extracted bodies.
 for idx,p in enumerate(rules,1):
  status=summary[idx-1][1]
  orig=(source/"spec/formal"/p["source"]).read_text(encoding="utf-8")
  extracted=(dest/("results/spec/"+status+"/17/"+str(idx)+".spec")).read_text(encoding="utf-8")
  assert p["block"] in orig and p["block"] in extracted
 for f in (source/"spec").rglob("*"):
  if f.is_file(): assert f.read_bytes()==(proj/"spec"/f.relative_to(source/"spec")).read_bytes()
 print("P17 SOURCE SHA",subprocess.check_output(["git","-C",str(source),"rev-parse","HEAD"],text=True).strip())
 print("P17 PDF SHA256",sha256(pdf),"pages",len(pages))
 print("P17 source 41 properties verified against extracted blocks")
 print("P17 distributions",counts,Counter(p[4] for p in summary))
 print("P17 written artifacts",len(outrows),"CSV rows",len(outrows))
 for p,s,reason,_,result in summary:
  print("P17 example",p["index"],p["source"],p["name"],s,result,"MISSING:"+reason[:130] if reason else "")
if __name__=="__main__":main()
