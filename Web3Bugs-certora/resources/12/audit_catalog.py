#!/usr/bin/env python3
"""Project 12 snapshot/extraction integrity audit; does not rerun Certora."""
import csv
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path.cwd()
EXPECTED = [
    ("StableDebtToken.spec", 5, 12), ("StableDebtToken.spec", 21, 36),
    ("StableDebtToken.spec", 42, 56), ("StableDebtToken.spec", 62, 101),
    ("StableDebtToken.spec", 106, 116), ("StableDebtToken.spec", 126, 142),
    ("StableDebtToken.spec", 144, 153), ("StableDebtToken.spec", 155, 167),
    ("StableDebtToken.spec", 174, 184),
    ("VariableDebtToken.spec", 6, 20), ("VariableDebtToken.spec", 26, 41),
    ("VariableDebtToken.spec", 46, 60), ("VariableDebtToken.spec", 65, 79),
    ("VariableDebtToken.spec", 90, 102), ("VariableDebtToken.spec", 108, 121),
    ("VariableDebtToken.spec", 129, 138), ("VariableDebtToken.spec", 143, 156),
    ("VariableDebtToken.spec", 164, 174),
    ("UserConfiguration.spec", 11, 12), ("UserConfiguration.spec", 14, 15),
    ("UserConfiguration.spec", 18, 19), ("UserConfiguration.spec", 21, 22),
    ("UserConfiguration.spec", 26, 32), ("UserConfiguration.spec", 34, 44),
    ("UserConfiguration.spec", 47, 53), ("UserConfiguration.spec", 56, 66),
]
SOURCE_SHA = {
    "StableDebtToken.spec": "a486d335352d73d4d81495447d29be20b9916e31",
    "VariableDebtToken.spec": "eb19d1b4f435b67d52f2486fd99335d173883d1b",
    "UserConfiguration.spec": "41a4f93e1323157efb5411cb72ebeb7a5d60f68a",
}
issues = []
def fail(message):
    issues.append(message)

source_lines = {}
for name, sha in SOURCE_SHA.items():
    p = ROOT / "contracts/12/specs" / name
    got = subprocess.run(["git", "hash-object", str(p)], capture_output=True, text=True)
    if got.returncode or got.stdout.strip() != sha:
        fail(f"source hash mismatch: {name}: {got.stdout.strip()} expected {sha}")
    source_lines[name] = p.read_text(encoding="utf-8").splitlines()
    names = re.findall(r"(?m)^\s*(?:rule|invariant)\s+([A-Za-z_]\w*)\b", p.read_text(encoding="utf-8"))
    print(f"source {name}: {len(names)} active property declarations")
if [len(re.findall(r"(?m)^\s*(?:rule|invariant)\s+\w+", (ROOT / "contracts/12/specs" / n).read_text())) for n in SOURCE_SHA] and sum(len(re.findall(r"(?m)^\s*(?:rule|invariant)\s+\w+", (ROOT / "contracts/12/specs" / n).read_text())) for n in SOURCE_SHA) != 26:
    fail("active property declaration count != 26")

with (ROOT / "results/spec/spec_buglabel.csv").open(newline="", encoding="utf-8") as f:
    rows = [r for r in csv.DictReader(f) if r["Project ID"] == "12"]
if len(rows) != 26 or len({int(r["Example ID"]) for r in rows}) != 26:
    fail(f"Project 12 CSV: {len(rows)} rows / {len({r['Example ID'] for r in rows})} IDs")

block_count = 0
for idx, (family, start, end) in enumerate(EXPECTED, 1):
    matches = [r for r in rows if r["Example ID"] == str(idx)]
    if len(matches) != 1:
        fail(f"example {idx}: no unique row")
        continue
    r = matches[0]
    target = "incomplete" if idx <= 9 else "complete"
    if r["Status"] != target:
        fail(f"example {idx} status={r['Status']} expected {target}")
    basename = ROOT / f"results/spec/{target}/12/{idx}"
    for extension in (".spec", ".sol", ".md") + ((".txt",) if idx <= 9 else ()):
        if not (basename.with_suffix(extension)).is_file():
            fail(f"example {idx}: missing {extension}")
    src = "\n".join(source_lines[family][start - 1:end])
    extracted = basename.with_suffix(".spec").read_text(encoding="utf-8")
    if src not in extracted:
        fail(f"example {idx}: original property body not preserved verbatim")
    if r["Original Spec"] != f"contracts/12/specs/{family}":
        fail(f"example {idx}: incorrect source attribution")
    if idx == 6 and (r["Result"], r["Detection Outcome"]) != ("VERIFIED", "NOT_STATED"):
        fail(f"example 6: conflation of historical finding with exact detector")
    excerpt = basename.with_suffix(".sol").read_text(encoding="utf-8")
    refs = list(re.finditer(r"(?m)^// Original: (contracts/12/[^\n:]+):(\d+)-(\d+)\n", excerpt))
    if not refs:
        fail(f"example {idx}: no Solidity provenance headers")
    for j, hit in enumerate(refs):
        loc, a, b = hit.group(1), int(hit.group(2)), int(hit.group(3))
        if not a or a > b:
            fail(f"example {idx}: invalid provenance line range")
            continue
        path = ROOT / loc
        if not path.is_file():
            fail(f"example {idx}: missing Solidity {loc}")
            continue
        selected = "\n".join(path.read_text(encoding="utf-8").splitlines()[a - 1:b]).strip()
        ending = refs[j + 1].start() if j + 1 < len(refs) else len(excerpt)
        actual = excerpt[hit.end():ending].strip()
        if actual != selected:
            fail(f"example {idx}: Solidity excerpt {loc}:{a}-{b} differs from snapshot")
        block_count += 1

pdf = ROOT / "resources/12/AaveV2Dec2020.pdf"
sha = subprocess.run(["git", "hash-object", str(pdf)], capture_output=True, text=True)
if sha.returncode or sha.stdout.strip() != "705d0961134f5a0b9d48c15723a5cde367c7e003":
    fail("AaveV2Dec2020.pdf Git blob differs from original")
for source, expected in (
    ("contracts", "2a239836b37faafa2d5b5d3ed7f63f8b7b624cde"),
    ("specs", "c34bd13f4ec6ab61263bfc767c6b7b2564ecb41d"),
):
    gitpath = f"HEAD:Web3Bugs-certora/contracts/12/{source}"
    sha = subprocess.run(["git", "-C", str(ROOT), "rev-parse", gitpath], capture_output=True, text=True)
    if sha.returncode or sha.stdout.strip() != expected:
        fail(f"{source} Git tree mismatch: {sha.stdout.strip()} expected {expected}")
print(f"Project 12 provenance: {len(EXPECTED)} exact source bodies, {block_count} literal Solidity excerpts; 3 spec blob hashes, 2 source tree hashes, PDF blob checked")
for error in issues:
    print("ERROR:", error)
sys.exit(1 if issues else 0)
