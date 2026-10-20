#!/usr/bin/env python3
"""Check CVL2 compilation *attempts* without implying formal equivalence.

One extracted property may have an original parser failure and a separately
derived candidate that compiles. Such cases must never be counted as two distinct
catalog examples, nor is COMPILE_OK a verification or semantic proof.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1]
C = BASE / "results/spec/spec_buglabel.csv"
LEDGER = BASE / "docs/cvl2/coordination/ROUND8_COMPILATION_ATTEMPTS.csv"
EXPECTED = {
    "catalog_unique": 1386, "catalog_relations": 1390,
    "attempts": 18, "properties_with_attempts": 16,
    "compile_ok": 6, "compile_error": 12,
    "properties_with_both_outcomes": 2,
    "untested": 1370,
}

def read(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def analyze(catalog, observations):
    rows = read(catalog)
    records = read(observations)
    source_keys = {
        (r["Project ID"], r["Status"], r["Example ID"]) for r in rows
    }
    per_property = defaultdict(set)
    seen_attempts = set()
    errors = []
    counts = Counter()
    for r in records:
        key = (r["project_id"], r["original_status"], r["example_id"])
        variant = r["variant_kind"]
        attempt_key = key + (variant,)
        if key not in source_keys:
            errors.append("not in original catalog: " + "/".join(key))
        if attempt_key in seen_attempts:
            errors.append("duplicate attempt: " + "/".join(attempt_key))
        seen_attempts.add(attempt_key)
        outcome = r["cvl2_compile_only_observed"]
        if outcome not in ("COMPILE_OK", "COMPILE_ERROR"):
            errors.append("invalid compile status: " + "/".join(key))
        if r["semantic_equivalence"] != "NOT_DEMONSTRATED":
            errors.append("unsupported semantic promotion: " + "/".join(key))
        if not r["executor"].strip() or not r["provenance"].strip() or not r["target"].strip():
            errors.append("missing execution attribution/evidence: " + "/".join(key))
        if variant == "DERIVED_SIX_SIG_PREFIXES":
            if key not in {("7", "complete", "47"), ("7", "complete", "73")}:
                errors.append("unexpected six-sig variant: " + "/".join(key))
            if outcome != "COMPILE_OK":
                errors.append("six-sig test unexpectedly failed")
            for field in ("source_sha256", "candidate_sha256"):
                digest = r[field].strip()
                if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
                    errors.append("missing SHA256: " + field + " " + "/".join(key))
            if r["source_sha256"] == r["candidate_sha256"]:
                errors.append("derived variant identical to source unexpectedly")
        per_property[key].add(outcome)
        counts[outcome] += 1
    metrics = {
        "catalog_unique": len(source_keys),
        "catalog_relations": len(rows),
        "attempts": len(records),
        "properties_with_attempts": len(per_property),
        "compile_ok": counts["COMPILE_OK"],
        "compile_error": counts["COMPILE_ERROR"],
        "properties_with_both_outcomes": sum(len(x) == 2 for x in per_property.values()),
        "untested": len(source_keys - set(per_property)),
    }
    for metric, value in EXPECTED.items():
        if metrics[metric] != value:
            errors.append(f"{metric}: expected {value}, got {metrics[metric]}")
    if not {("7", "complete", "47"), ("7", "complete", "73")} <= {
        k for k, statuses in per_property.items() if len(statuses) == 2
    }:
        errors.append("both original failures and derived successes must be present for P7/47 and P7/73")
    return {"metrics": metrics, "errors": errors, "semantic_proven": 0, "fully_migrated_projects": 0}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", type=Path, default=C)
    p.add_argument("--attempts", type=Path, default=LEDGER)
    args = p.parse_args()
    try:
        result = analyze(args.catalog, args.attempts)
    except (OSError, ValueError, KeyError, csv.Error) as exc:
        print("Input validation failed:", exc, file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["errors"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
