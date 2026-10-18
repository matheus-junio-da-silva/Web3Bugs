#!/usr/bin/env python3
"""Deterministic HELIX P15 recatalog, using P2 as an identical historic source."""
import csv, hashlib, io, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "Web3Bugs-certora"
PAIRS = [("complete",1,1),*[( "incomplete",i,i+1) for i in range(1,15)]]
NAMES = [
 "PoRFeedChange","notAllReservesBacked_UnbackedArry_Correlation",
 "integrityOfDisableAssets","integrityOfEnableAssets","enableDuplicationsWithStorage",
 "disableDuplicationsWithStorage","flagConsistancy","uniqueArray",
 "integrityOfDisableAssets","integrityOfEnableAssets","enableDuplicationsWithStorage",
 "disableDuplicationsWithStorage","flagConsistancy","flagConsistancy2","uniqueArray"]
SPECS = {"aggregator.spec":("f6787f5c0a14f0a7cb20115a3bdc1db6379f5301b405d93f610928814a854fb8",2),
"executorV2.spec":("80c9afa753589467785cbcf634c067cecdf24f43c0a1ba18757e76fd68518640",6),
"executorV3.spec":("e213486c2268bdec03db68822e7a244343a32171706aea3104c4679eba1f0c06",7)}
PDF = "Aave-Proof-of-Reserve-Formal-Verification-Report.pdf"
def change(s):
    s=s.replace("contracts/2/","contracts/15/").replace("resources/2/","resources/15/").replace("reports/2.md","reports/15.md")
    s=re.sub(r"results/spec/(complete|incomplete)/2/(\d+)\.(spec|sol|md|txt)",
             lambda m:"results/spec/incomplete/15/{}.{}".format(
             1 if m.group(1)=="complete" else int(m.group(2))+1,m.group(3)),s)
    return s
def append_csv(path,rows,cols):
    before=path.read_bytes()
    eol="\r\n" if b"\r\n" in before else "\n"
    s=io.StringIO(newline="")
    csv.DictWriter(s,fieldnames=cols,lineterminator=eol).writerows(rows)
    path.write_bytes(before+(b"" if before.endswith((b"\n",b"\r")) else eol.encode())+s.getvalue().encode())
def run():
    assert not (ROOT/"contracts/15").exists(), "Refusing to overwrite P15"
    assert not (ROOT/"results/spec/incomplete/15").exists(), "Refusing to overwrite P15 examples"
    for f,(digest,n) in SPECS.items():
        src=(ROOT/"contracts/2/specs"/f).read_bytes()
        assert hashlib.sha256(src).hexdigest()==digest, f
        active=re.findall(r"(?m)^[ \t]*(?:rule|invariant)\s+([A-Za-z_]\w*)",src.decode())
        assert len(active)==n,(f,active)
    for f in ("executorV2.spec","executorV3.spec"):
        assert "// rule integrityOfExecuteEmergencyAction" in (ROOT/"contracts/2/specs"/f).read_text()
    shutil.copytree(ROOT/"contracts/2",ROOT/"contracts/15")
    (ROOT/"resources/15").mkdir()
    shutil.copy2(ROOT/"resources/2"/PDF,ROOT/"resources/15"/PDF)
    r=(ROOT/"reports/2.md").read_bytes()
    assert b"contest: 2" in r
    (ROOT/"reports/15.md").write_bytes(r.replace(b"contest: 2",b"contest: 15",1))
    dest=ROOT/"results/spec/incomplete/15"
    dest.mkdir(parents=True)
    for (status,old,new),name in zip(PAIRS,NAMES):
        old_dir=ROOT/f"results/spec/{status}/2"
        target="Aggregator" if new<3 else ("V2" if new<9 else "V3")
        for suffix in ("spec","sol","md","txt"):
            p=old_dir/f"{old}.{suffix}"
            if not p.exists():
                assert status=="complete" and suffix=="txt"
                continue
            t=change(p.read_text())
            if status=="complete" and suffix=="spec":
                t=t.replace("Dependency status: complete","Dependency status: incomplete")
            if suffix=="md":
                t=re.sub(r"^# Example \d+",f"# Example {new}",t,count=1,flags=re.M)
                if status=="complete":
                    t=t.replace("**Complete for dependency cataloging.**",
                       "**Incomplete under recursive Solidity source-dependency closure.**")
                    t=t.replace("All non-built-in dependencies required by this property were found in the available snapshot.",
                       "Local CVL declarations exist; external Solidity imports are unresolved in the snapshot.")
                t+="\n\n## HELIX P15 independent semantic review\n\n"
                t+=f"This source instance is identical to the historic P2 extraction {status}/2/{old}. "
                t+="Its source assertion, assumptions and specific counterexample are documented above; "
                t+="P15 requires additional recursive Solidity closure. External dependencies and "
                t+="historical harness/link configuration remain unresolved, independent of CVL syntax. "
                t+="The target-specific historical report result is not a new Prover run. "
                t+="V2 and V3 emergency logic, access sets, ghosts and hooks are not interchangeable.\n"
                t="\n".join(s.rstrip() for s in t.splitlines())+"\n"
            if suffix=="txt":
                t+="\nP15 additional transitive Solidity imports: solidity-utils Ownable/IERC20 "
                t+="and chainlink-brownie-contracts AggregatorV3Interface; Executor V2/V3 "
                t+="also import aave-address-book interfaces. These packages are not vendored "
                t+="in contracts/15. The original config/solc maps are absent. CVL methods "
                t+="declarations do not supply these implementations. CVL2 migration is unrelated.\n"
            (dest/f"{new}.{suffix}").write_text(t)
        if status=="complete":
            (dest/f"{new}.txt").write_text(
               "INCOMPLETE: PoRFeedChange on ProofOfReserveAggregator. Original aggregator.spec "
               "methods/helper and local mapping mutations are available, but "
               "ProofOfReserveAggregator.sol transitively imports onlyOwner (solidity-utils Ownable), "
               "IERC20 (solidity-utils), and AggregatorV3Interface (chainlink-brownie-contracts), "
               "neither supplied as historical Solidity sources in the PropertyGPT snapshot. "
               "No original Certora dependency/version configuration is present. "
               "The NONDET latestRoundData summary is not a replacement for the imported "
               "interface or Ownable behavior. Its result VERIFIED is explicitly reported "
               "historically; not an independently rerun verification. "
               "This is not a CVL1/CVL2 syntax issue.\n")
    # Strictly additive CSV editing, preserving every byte of prior rows.
    catalog=ROOT/"results/spec/spec_buglabel.csv"
    existing=catalog.read_bytes().decode()
    rd=csv.DictReader(io.StringIO(existing,newline=""))
    fields=list(rd.fieldnames)
    records=list(rd)
    assert sum(x["Project ID"]=="2" for x in records)==16
    assert not any(x["Project ID"]=="15" for x in records)
    newrows=[]
    for row in records:
        if row["Project ID"]!="2":continue
        old_status=row["Status"]
        row=dict(row)
        row["Project ID"]="15"
        row["Status"]="incomplete"
        row["Example ID"]=str(1 if old_status=="complete" else int(row["Example ID"])+1)
        for col in ("Spec","Code","Documentation","Incomplete Reason","Original Spec","Original Contract"):
            row[col]=change(row[col])
        if old_status=="complete":
            row["Incomplete Reason"]="results/spec/incomplete/15/1.txt"
        newrows.append(row)
    append_csv(catalog,newrows,fields)
    cp=ROOT/"results/contests.csv"
    cb=cp.read_bytes()
    assert not re.search(rb"(?m)^15,",cb)
    eol=b"\r\n" if b"\r\n" in cb else b"\n"
    cp.write_bytes(cb+(b"" if cb.endswith((b"\r",b"\n")) else eol)+
       b"15,AAVE Proof of Reserve (HELIX independent recatalog),-,-,-,2022-11,-,-"+eol)
    attrs=ROOT/".gitattributes"
    attrs.write_text(attrs.read_text().rstrip("\n")+
        "\n\n# P15 historic byte-literal source and excerpts only\n"+
        "contracts/15/** -whitespace\nresults/spec/incomplete/15/*.spec -whitespace\n"+
        "results/spec/incomplete/15/*.sol -whitespace\nreports/15.md -whitespace\n")
    matrix=[]
    focus=[
      "feed & wrapper transitions and zero-address checks",
      "aggregate backing boolean disagrees with per-asset helper",
      "disable leaves flag enabled or wrong list length",
      "enable leaves flag disabled or wrong list length",
      "enabling twice differs from once",
      "disabling twice differs from once",
      "V2 mirrored flag/list mismatch",
      "V2 duplicate asset indices",
      "disable leaves flag enabled or wrong list length",
      "enable leaves flag disabled or wrong list length",
      "enabling twice differs from once",
      "disabling twice differs from once",
      "V3 in-range list asset has disabled flag",
      "V3 active flag maps to different asset",
      "V3 duplicate asset indices"]
    for i,name in enumerate(NAMES,1):
        target="Aggregator" if i<3 else ("Executor V2" if i<9 else "Executor V3")
        result="NOT_STATED" if i in (7,8,13,14,15) else "VERIFIED"
        outcome="NOT_STATED" if result=="NOT_STATED" else "NO_FINDING"
        matrix.append(f"| {i} | {target} | {name} | {result} / {outcome} | {focus[i-1]} |")
    doc="""# Project 15 — AAVE Proof of Reserve / HELIX

## Source identity and existing Project 2
This is intentionally an independent *recatalog* of the same historic AAVE
Proof of Reserve material already covered by Project 2. No new distinct
verification engagement, finding or set of 15 extra original properties
is implied. The original Project 2 was not edited. P15 source contracts,
three specs and original PDF are byte-identical to P2; P15 uses a stricter
transitive Solidity dependency test. The supplied PropertyGPT specs have
SHA256 hashes:
"""
    for f,(h,n) in SPECS.items():doc+=f"- {f}: {h}\n"
    doc+="""The preserved historic PDF is resources/15/Aave-Proof-of-Reserve-Formal-Verification-Report.pdf
(Git blob 383307e6076e87d549faa23817a17e79acfc4317).
The report identifies 6–22 Nov 2022 and reviewed commit 12296ce;
there is no proof that the supplied source snapshot matches the historical
upstream commit byte for byte. Reports/15.md is the PDF text-layer transcript
derived from reports/2.md; PDF visuals and status marks are authoritative.

## Coverage and dispositions
Aggregator 2 active rules; Executor V2 4 rules and 2 invariants;
Executor V3 4 rules and 3 invariants = **15 active source instances**.
Two integrityOfExecuteEmergencyAction rules remain commented out and
must not be indexed despite descriptions of proofs in the PDF.
Every CVL property body is copied literally; no migration to CVL2.

**Status: 0 complete / 15 incomplete.** Compared with P2 (1/14), the new
PoRFeedChange incomplete classification additionally requires closed
Solidity imports. The Solidity contracts depend on non-vendored
solidity-utils, chainlink-brownie-contracts, aave-address-book and/or
missing historical harnesses/helpers. N.txt documents concrete deficits.
Not having source dependencies is not evidence that the report's proof failed.

**Results: 10 VERIFIED, 5 NOT_STATED, 0 VIOLATED.**
**Detection Outcomes: 10 NO_FINDING, 5 NOT_STATED, 0 FINDING.**
16 CSV relationship rows (PoRFeedChange has labels S3-2 and S2-1).
The existing report does not attribute a new specific security finding
to one of these active instances; bugs.csv must remain unmodified.

## Individual second semantic review
| ID | Target | Property | Result / outcome | What falsifies the assertion |
| ---: | --- | --- | --- | --- |
"""
    doc+="\n".join(matrix)+"\n"
    doc+="""
The report describes three aggregate invariant concepts, including
Asset Is Not Zero, but five active source invariants are present across
Executor V2/V3. No report glyph is assigned individually to those five
without one-to-one evidence. Four common Executor rules are reported
as verified for each version; aggregator rules are named explicitly.

## Semantic divergences and model caveats
- Aggregator PoRFeedChange prohibits mapping changes by unrelated
  functions, contrary to contradictory PDF prose saying "must change."
- Source disableAssets assertions use assetStateBefore where report
  formulas sometimes use assetStateAfter.
- Duplication-rule report formulas include conditions absent from active
  CVL. No assertions are fabricated.
- Executor V2 uses mirrorArray/mirrorFlag/reverseMap/_assetsLength ghosts,
  preserved invariants and Sload/Sstore hooks, and filters the emergency
  selector. Executor V3 uses distinct OneToOne_arrOfTokens/Consistant_flag
  ghosts, reverseMapInit, access-set hooks and an extra msg.value==0
  requirement in its duplication rules.
- V2 emergency logic disables borrowing across the pool and freezes
  affected assets. V3 freezes affected assets and sets their LTV to zero.
  Commented emergency properties are not revived.
- Missing original areAllReservesBackedCorrelation/allBacked, enableAsset,
  disableAsset, getAssetState, getAsset, getAssetsLength and Dummy/harness
  implementations cannot be inferred from methods declarations.
- The report assumes correct external configurator effects and checks
  only invoked functions; executor aggregator responses are nondeterministic;
  loops are unrolled to three iterations; external calls may affect other
  contracts but are assumed not to change the verified contract state.
  Historical VERIFIED is scoped to these assumptions and is not a new
  unrestricted formal proof.

## Validation and provenance
The original CVL and Solidity snapshot lives under contracts/15;
each results/spec/incomplete/15/N.spec, N.sol, N.md, N.txt describes
a property, actual source line excerpts, its report result, technical
Bug Label, target, specific missing dependencies, and counterexample.
CSV changes are additive only for Project 15; Project 2 records untouched.
Run scripts/check_specs.py, check_contests_csv.py and check_contracts.py
with python from Web3Bugs-certora; run git -c core.whitespace=cr-at-eol
diff --check origin/main...HEAD at Git root, and record exact exit codes.
Structural validation is not Certora re-verification.

The local ZIP was not inspected because local Python/container tooling
failed with infrastructure errors. GitHub checkout and versioned Git
blobs, not an unverified ZIP, are the source for this recatalog.
"""
    (ROOT/"docs/spec_catalog_project_15.md").write_text(
      "\n".join(x.rstrip() for x in doc.splitlines())+"\n")
    for f in SPECS:
        assert (ROOT/"contracts/15/specs"/f).read_bytes()==(ROOT/"contracts/2/specs"/f).read_bytes()
    assert (ROOT/"resources/15"/PDF).read_bytes()==(ROOT/"resources/2"/PDF).read_bytes()
    for (status,old,new),name in zip(PAIRS,NAMES):
        original=(ROOT/f"results/spec/{status}/2/{old}.spec").read_text()
        updated=(dest/f"{new}.spec").read_text()
        loc=re.search(rf"(?m)^[ \t]*(?:rule|invariant)\s+{re.escape(name)}\b",original)
        assert loc and original[loc.start():] in updated,(name,new)
        for ext in ("spec","sol","md","txt"):
            assert (dest/f"{new}.{ext}").is_file()
    assert len(list(dest.glob("*.spec")))==15
    assert len(list(dest.glob("*.sol")))==15
    assert len(list(dest.glob("*.md")))==15
    assert len(list(dest.glob("*.txt")))==15
    print("P15 catalog: 15 literal property extractions, 15 incomplete reasons,")
    print("16 CSV relations, source-spec/PDF byte preservation, no Project 2 mutations.")
if __name__=="__main__":
    run()
