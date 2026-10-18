#!/usr/bin/env python3
"""Independent second pass for the 41 original Compound old-sterility/Specify blocks.
No dependency on the generator implementation; fails on omissions, incorrect
line provenance, modified CVL bodies, bad Solidity excerpts or altered source.
"""
import csv
import hashlib
import re
import sys
import subprocess
from pathlib import Path
from collections import Counter
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(src,dst):
 assert subprocess.check_output(["git","-C",str(src),"rev-parse","HEAD"],text=True).strip()=="687f654c679ed45ab127b7949e2a29c8f5e491b9"
 exact={}
 formal=src/"spec/formal"
 scan={}
 for p in sorted(formal.glob("*.cvl")):
  raw=p.read_text(encoding="utf-8")
  ls=raw.splitlines(keepends=True)
  if p.name=="dummy.cvl":
   assert len(raw.strip())<=15
   continue
  assert ls[0].strip()=="methods {"
  end_methods=next(i for i in range(1,len(ls)) if ls[i].strip()=="}")
  for i in range(end_methods+1,len(ls)):
   m=re.match(r"^([A-Za-z_]\w*)\s*\(",ls[i])
   if not m:continue
   end=next(j for j in range(i+1,len(ls)) if ls[j].startswith("}") and ls[j].strip()=="}")
   block="".join(ls[i:end+1])
   assert re.search(r"\bstatic_assert\b",block)
   key=(p.name,i+1)
   assert key not in exact
   exact[key]=(m.group(1),block,end+1)
   scan[p.name]=scan.get(p.name,0)+1
 assert len(exact)==41,(len(exact),scan)
 assert len(list(formal.glob("*.spclnk")))==5
 root=dst/"contracts/17"
 assert all(p.read_bytes()==(root/"contracts"/p.relative_to(src/"contracts")).read_bytes() for p in (src/"contracts").rglob("*") if p.is_file())
 assert all(p.read_bytes()==(root/"spec"/p.relative_to(src/"spec")).read_bytes() for p in (src/"spec").rglob("*") if p.is_file())
 assert sha(src/"CompoundMoneyMarketV2Aug2019.pdf")==sha(dst/"resources/17/CompoundMoneyMarketV2Aug2019.pdf")=="cb48b1c159df4ef3d603f84afc2e7fa9da6c2c0b72f9760e6d962807f4177a1a"
 with (dst/"results/spec/spec_buglabel.csv").open(newline="",encoding="utf-8") as f:
  rows=[row for row in csv.DictReader(f) if row["Project ID"].strip()=="17"]
 assert len(rows)==41
 assert sorted(int(r["Example ID"]) for r in rows)==list(range(1,42))
 assert len({(r["Original Spec"],r["Original Spec Lines"],r["Property"]) for r in rows})==41
 seen=set()
 for row in sorted(rows,key=lambda x:int(x["Example ID"])):
  i=int(row["Example ID"]);status=row["Status"]
  assert status in {"complete","incomplete"}
  prefix=dst/"results/spec"/status/"17"/str(i)
  extracted=prefix.with_suffix(".spec").read_text(encoding="utf-8")
  md=prefix.with_suffix(".md").read_text(encoding="utf-8")
  sol=prefix.with_suffix(".sol").read_text(encoding="utf-8")
  match=re.search(r"Rule ([A-Za-z_]\w*) original lines (\d+)-(\d+)",extracted)
  assert match,(i,"No CVL block provenance")
  name,first,last=match.group(1),int(match.group(2)),int(match.group(3))
  fm=re.search(r"Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/([A-Za-z_]\w*\.cvl)",extracted)
  assert fm,(i,"No source")
  fn=fm.group(1)
  key=(fn,first)
  assert key in exact,(i,fn,first)
  orig_name,orig_block,orig_last=exact[key]
  assert name==orig_name==row["Property"] and last==orig_last
  assert row["Original Spec"]=="contracts/17/spec/formal/"+fn
  assert orig_block in extracted,(i,"Literal CVL property mismatch")
  assert "## Hypothetical counterexample" in md and "## Exact Solidity state/function relationship" in md,(i,"Missing semantic review")
  assert "## Historical result and soundness limits" in md,(i,"Missing soundness boundaries")
  assert len(re.findall(r"\bstatic_assert\b",orig_block))==len(re.findall(r"\bstatic_assert\b",extracted)),(i,"Extra assertion")
  # All CVL method declarations that were selected in the extract are literal
  # original lines, excluding source header and properties.
  original_lines=(formal/fn).read_text(encoding="utf-8").splitlines(keepends=True)
  original_methods="".join(original_lines[1:next(k for k in range(1,len(original_lines)) if original_lines[k].strip()=="}")])
  prelude=extracted[extracted.index("methods {\n")+len("methods {\n"):extracted.index("}\n\n",extracted.index("methods {\n"))]
  for line in prelude.splitlines(keepends=True):
   assert line in original_methods,(i,"non-original CVL method",repr(line))
  # Every Solidity block is a literal line range from the preserved source,
  # including all snippets when the example uses multiple contracts.
  pat=re.compile(r"^// Original: contracts/17/([^\n]+?) lines (\d+)-(\d+)\n",re.M)
  matches=list(pat.finditer(sol))
  assert matches,(i,"missing Solidity provenance")
  for k,m in enumerate(matches):
   rel,a,b=m.group(1),int(m.group(2)),int(m.group(3))
   source_sol=src/rel
   assert source_sol.exists() and a>0 and b>=a,(i,rel,a,b)
   ls=source_sol.read_text(encoding="utf-8").splitlines(keepends=True)
   expected="".join(ls[a-1:b]).rstrip("\n")
   actual=sol[m.end():(matches[k+1].start() if k+1<len(matches) else len(sol))].rstrip("\n")
   assert expected==actual,(i,rel,"Solidity excerpt diverges from original")
  if status=="incomplete":
   reason=prefix.with_suffix(".txt").read_text(encoding="utf-8")
   assert reason.strip() and "Historical dependency closure blocker" in reason
  else:assert not prefix.with_suffix(".txt").exists()
  seen.add(key)
  print("INDEPENDENT REVIEW",i,fn,name,status,row["Bug Label"],row["Result"],"Solidity excerpts",len(matches))
 assert seen==set(exact),(seen.symmetric_difference(set(exact)))
 assert Counter(r["Status"] for r in rows)==Counter({"complete":31,"incomplete":10})
 assert Counter(r["Result"] for r in rows)==Counter({"VERIFIED":9,"NOT_STATED":32})
 assert len(list((dst/"reports/17.md").read_text(encoding="utf-8").split("## PDF page ")))==48
 print("INDEPENDENT P17 PASS: 41/41 literal original properties, 41/41 source/label/status rows, exact Solidity line excerpts, 31 complete, 10 incomplete, 9 verified, 32 not stated")
 print("SOURCE SHA 687f654c679ed45ab127b7949e2a29c8f5e491b9; PDF SHA256 cb48b1c159df4ef3d603f84afc2e7fa9da6c2c0b72f9760e6d962807f4177a1a")
if __name__=="__main__":
 if len(sys.argv)!=3:raise SystemExit("usage: audit.py source_project_dir Web3Bugs-certora_dir")
 check(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve())
