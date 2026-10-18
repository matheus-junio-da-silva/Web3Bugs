#!/usr/bin/env python3
"""P23 independent historical-source catalog audit; does not use the generator."""
import csv,re,hashlib,sys
from pathlib import Path
from collections import Counter
FILES={"DripsHub.spec":12,"DripsHubBackup.spec":6,"Reserve.spec":5,
       "SlotTester.spec":1,"Splits.spec":17,"Splits2.spec":5}
VERIFIED=set("correctnessOfSplitResults correctnessOfSplit integrityOfCollect revertCharacteristicsOfCollect correctnessOfGive splittableOfNonReceiverNotAffectedByGive correctnessOfHashSplits integrityOfSplit assetsDoNotInterfereEachOther moneyNotLostOrCreatedDuringSplit sameReturnOfSplitAndSplitResults equalSplitWeightsResultEqualSplittableIncrease cannotFrontRunSplitDifferentUsers cannotFrontRunSplitTwoSameUsers cannotFrontRunSplitThreeSameUsers".split())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def remove_comments(s):
 # Preserve newlines so source offsets and start-line references are reliable.
 def blank(m):return "".join("\n" if c=="\n" else " " for c in m.group())
 s=re.sub(r"/\*.*?\*/",blank,s,flags=re.S)
 return re.sub(r"//[^\n]*",blank,s)
def main(src,dst):
 sources={}
 for fname,cnt in FILES.items():
  f=src/"specs"/fname
  text=f.read_text(encoding="utf-8")
  clean=remove_comments(text)
  starts=re.findall(r"(?m)^[ \t]*(rule|invariant)[ \t]+([A-Za-z_]\w*)\b",clean)
  assert len(starts)==cnt,(fname,len(starts),cnt)
  sources[fname]=(f,text,starts)
 assert sum(FILES.values())==46
 assert len(list((src/"src").glob("*.sol")))==6
 project=dst/"contracts/23"
 for sub in ("src","specs"):
  files=[p for p in (src/sub).rglob("*") if p.is_file()]
  for f in files:
   d=project/sub/f.relative_to(src/sub)
   assert d.is_file() and d.read_bytes()==f.read_bytes(),("source preservation",f)
 assert digest(src/"Formal_Verification_Report_of_Radicle_Drips_Contracts.pdf")==digest(dst/"resources/23/Formal_Verification_Report_of_Radicle_Drips_Contracts.pdf")
 assert (dst/"reports/23.md").read_text(encoding="utf-8").count("## Original PDF page ")==6
 with (dst/"results/spec/spec_buglabel.csv").open(encoding="utf-8",newline="") as fh:
  rows=[r for r in csv.DictReader(fh) if r["Project ID"]=="23"]
 assert len(rows)==46
 assert sorted(int(r["Example ID"]) for r in rows)==list(range(1,47))
 seen=set();counts=Counter()
 for row in sorted(rows,key=lambda r:int(r["Example ID"])):
  idx=int(row["Example ID"]);f=row["Original Spec"];name=row["Property"]
  assert f.startswith("contracts/23/specs/"),(idx,f)
  fname=f.rsplit("/",1)[-1]
  assert fname in sources
  a,b=map(int,row["Original Spec Lines"].split("-"))
  original_lines=sources[fname][1].splitlines(keepends=True)
  excerpt="".join(original_lines[a-1:b]).rstrip("\n")
  # Exact source-bound text, comments, whitespace and line count.
  assert re.match(r"^\s*(?:rule|invariant)\s+"+re.escape(name)+r"\b",excerpt),(idx,name,a,b)
  spec=dst/row["Spec"]
  assert spec.is_file()
  copied=spec.read_text(encoding="utf-8")
  assert excerpt in copied,(idx,"original CVL body does not occur literally")
  assert ("original lines "+str(a)+"-"+str(b)) in copied,(idx,"missing provenance range")
  assert ("SHA256 "+digest(sources[fname][0])) in copied,(idx,"missing SHA provenance")
  assert len(re.findall(r"(?m)^\s*(?:rule|invariant)\s+\w+",remove_comments(copied)))==1,(idx,"extra active rule")
  key=(fname,a,b,name)
  assert key not in seen,(idx,"duplicated declaration");seen.add(key)
  assert row["Status"]=="incomplete"
  sol=(dst/row["Code"]).read_text(encoding="utf-8")
  matches=list(re.finditer(r"(?m)^// Original: contracts/23/src/([A-Za-z]\w*\.sol) lines (\d+)-(\d+)\n",sol))
  assert matches,(idx,"no Solidity provenance")
  for i,m in enumerate(matches):
   fn,lo,hi=m.group(1),int(m.group(2)),int(m.group(3))
   source_sol=src/"src"/fn
   assert source_sol.is_file() and hi>=lo>0,(idx,fn,lo,hi)
   textlines=source_sol.read_text(encoding="utf-8").splitlines(keepends=True)
   expected="".join(textlines[lo-1:hi]).rstrip("\n")
   actual=sol[m.end():(matches[i+1].start() if i+1<len(matches) else len(sol))].rstrip("\n")
   assert expected==actual,(idx,"Solidity excerpt changed",fn,lo,hi)
  docs=(dst/row["Documentation"]).read_text(encoding="utf-8")
  why=("## Why the Solidity excerpt is relevant","## Executable assertion(s)","## Hypothetical counterexample","## Assumptions and soundness","## Historical Result evidence","## Missing dependency / incomplete reason")
  for h in why:assert h in docs,(idx,h)
  assert (dst/row["Incomplete Reason"]).is_file()
  assert (dst/row["Incomplete Reason"]).read_text(encoding="utf-8").strip()
  assert (fname,name) not in {("Splits2.spec",v) for v in VERIFIED} or row["Result"]=="NOT_STATED"
  if fname=="Splits.spec":
   expected_result=("VERIFIED" if name in VERIFIED else "VIOLATED" if name=="splitReceiverShouldGetMoneyUponSplit" else "NOT_STATED")
   assert row["Result"]==expected_result,(idx,"result mismatch")
   if name=="cannotFrontRunSplitGeneralCase":assert row["Detection Outcome"]=="INCONCLUSIVE"
   if name=="splitReceiverShouldGetMoneyUponSplit":assert row["Detection Outcome"]=="FINDING" and row["Bug Label"]=="L2"
  else:assert row["Result"]=="NOT_STATED",(idx,"result improperly propagated")
  if fname=="DripsHubBackup.spec" and name=="whoChangedBalanceOfToken":
   assert row["Bug Label"]=="S3-2" and "filtered" in excerpt,(idx,"pause filter classified incorrectly")
  if name in ("sanity","sanitySimple","helperTest"):
   assert row["Bug Label"]=="UNMAPPED",(idx,"sanity label")
  counts[fname]+=1
  print("P23 SECOND REVIEW",idx,fname,name,"literal CVL OK","Solidity",len(matches),row["Result"],row["Bug Label"])
 assert dict(counts)==FILES,counts
 assert Counter(r["Result"] for r in rows)==Counter({"VERIFIED":15,"VIOLATED":1,"NOT_STATED":30})
 assert Counter(r["Detection Outcome"] for r in rows)==Counter({"NO_FINDING":15,"FINDING":1,"INCONCLUSIVE":1,"NOT_STATED":29})
 for row in rows:assert (dst/row["Spec"]).exists() and (dst/row["Code"]).exists() and (dst/row["Documentation"]).exists()
 print("P23 INDEPENDENT PASS: 46/46 source properties, 46/46 literal CVL, all exact Solidity excerpts, all CSV and document requirements, 15 VERIFIED 1 VIOLATED 30 NOT_STATED")
 print("P23 PDF SHA256",digest(src/"Formal_Verification_Report_of_Radicle_Drips_Contracts.pdf"))
if __name__=="__main__":
 if len(sys.argv)!=3:raise SystemExit("usage: audit.py path_to_radicle_src Web3Bugs-certora")
 main(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve())
