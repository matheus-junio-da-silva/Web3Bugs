#!/usr/bin/env python3
"""Refresh Project 15 specific Solidity evidence while preserving all source bytes."""
import csv, importlib.util, io, re
from pathlib import Path

module_path=Path(__file__).with_name("p15_gho_generate_catalog.py")
spec=importlib.util.spec_from_file_location("gho_catalog_generator",module_path)
g=importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
out=g.DATA/"results/spec/incomplete/15"
assert out.is_dir(),"Base P15 catalog must exist"
assert (g.ARCHIVE).is_dir(),"Pinned source must be mounted"
old_csv=g.DATA/"results/spec/spec_buglabel.csv"
old_bytes=old_csv.read_bytes()
eol="\r\n" if b"\r\n" in old_bytes else "\n"
existing=list(csv.DictReader(io.StringIO(old_bytes.decode(),newline="")))
p15=[x for x in existing if x["Project ID"]=="15"]
assert len(p15)==116,len(p15)
assert all(x["Status"]=="incomplete" for x in p15)
original_prefix=b"".join(line for line in old_bytes.splitlines(keepends=True)
                         if not line.startswith(b"15,"))
assert len(original_prefix)>len(old_bytes)*0.1
updated=[]
for row in p15:
    i=int(row["Example ID"])
    source=Path(row["Original Spec"]).name
    name=row["Property"]
    target=row["Target Contract"]
    props=g.properties((g.ARCHIVE/source).read_text())
    matches=[d for d in props if d["name"]==name]
    assert len(matches)==1,(i,source,name)
    body=matches[0]["body"]
    sol,paths,lines,mechanisms=g.relevant_solidity(source,body,name,target)
    (out/f"{i}.sol").write_text(sol)
    row["Original Contract"]=paths
    row["Original Contract Lines"]=lines
    source_imports=[]
    for path in g.SOL_FILES[target]:
        src=(g.ARCHIVE/path).read_text()
        source_imports+=re.findall(r"import\s+(?:[^;]*?\s+from\s+)?['\"]([^'\"]+)['\"]\s*;",src,re.S)
    missing=sorted(set(p for p in source_imports if not p.startswith(".")))
    detail="Concrete unvendored dependency paths: "+("; ".join(missing) if missing else "external transitive library imports")+"."
    src_info=f"The original archived Solidity implementation for target {target} is at {paths}, lines {lines}. "
    src_info+=f"The concrete entrypoints/storage extracted for the executable predicate are: {', '.join(mechanisms)}. "
    if source=="set.spec":
        src_info+="GhoToken.sol declares the EnumerableSet.AddressSet storage _facilitatorsList and modifies it via addFacilitator/removeFacilitator; set.spec requires the historical harness getter getFacilitatorsListLen, which is absent. This excerpt documents the real storage container but does not invent a getter body. "
    if source=="VariableDebtToken.spec":
        src_info+="Generic VariableDebtToken rules are imported into the GhoVariableDebtToken target; ScaledBalanceTokenBase and the user-state storage implement its debt/scaled accounting, but an independent stand-alone VariableDebtToken target is not established. "
    src_info+=f"The predicate could be falsified only by a counterexample satisfying the original CVL preconditions in which its assertion/return constraint fails; the {target} implementation and its inherited storage flow are the concrete paths controlling that result. "
    src_info+="All slices retain the original source bytes and exact source-line numbers, and are evidence rather than a stand-alone compiling contract. "
    src_info+=detail
    md=out/f"{i}.md"
    doc=md.read_text()
    doc,n1=re.subn(r"(?m)^- Original Solidity: .*$","- Original Solidity: "+paths+".",doc,count=1)
    doc,n2=re.subn(r"(?m)^- Original Solidity ranges: .*$","- Original Solidity ranges: "+lines+".",doc,count=1)
    assert n1==n2==1,(i,"original source metadata")
    start=doc.index("## Why the Solidity excerpt is relevant\n")
    stop=doc.index("\n## Missing dependency and soundness limitations",start)
    doc=doc[:start]+"## Why the Solidity excerpt is relevant\n"+src_info+"\n"+doc[stop:]
    replace=r"- Unvendored historical Solidity library imports \(Aave V3/OpenZeppelin and other upstream packages\) and original solc/link Prover configuration"
    doc,count=re.subn(replace,"- "+detail+" The original solc/link Prover configuration is absent.",doc)
    assert count==1,(i,"missing import description")
    if source=="set.spec":
        doc=doc.replace("- Generic set probe spec is imported by ghoToken.spec; no independent set harness/run target is archived",
            "- Generic set probe spec is imported by ghoToken.spec; no independent set harness/run target is archived\n- The historical set harness getter getFacilitatorsListLen is explicitly required by set.spec and is absent from GhoToken.sol.")
    md.write_text("\n".join(x.rstrip() for x in doc.splitlines())+"\n")
    txt=out/f"{i}.txt"
    reason=txt.read_text()
    reason,count=re.subn(r"Unvendored historical Solidity library imports \(Aave V3/OpenZeppelin and other upstream packages\) and original solc/link Prover configuration",
                        detail+" The original solc/link Prover configuration is absent",reason)
    assert count==1,(i,"incomplete reason")
    if source=="set.spec":
        reason+="Historical set-specific dependency: set.spec explicitly documents that getFacilitatorsListLen must be defined in a Solidity harness; the GhoToken implementation does not provide it.\n"
    txt.write_text(reason)
    updated.append(row)
buf=io.StringIO(newline="")
csv.DictWriter(buf,fieldnames=g.HDR,lineterminator=eol).writerows(updated)
old_csv.write_bytes(original_prefix+buf.getvalue().encode())
for row in updated:
    i=row["Example ID"]
    assert (out/f"{i}.sol").is_file()
    assert "## Why the Solidity excerpt is relevant" in (out/f"{i}.md").read_text()
    assert "Concrete unvendored dependency paths" in (out/f"{i}.txt").read_text()
assert len(list(out.glob("*.sol")))==116
print("REFRESH: 116/116 specific original Solidity excerpts, target citations and exact missing package import paths")
print("REFRESH: CSV non-P15 prefix retained byte-for-byte; 116 P15 relationships rebuilt")
