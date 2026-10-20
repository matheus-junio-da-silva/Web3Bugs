#!/usr/bin/env python3
"""Validate Round 7 progress against original property IDs and observed CLI outputs.

This is a structural accounting validator, NOT a CVL2 typechecker or proof.
Never promote documentation or solc ABI results to CVL2 COMPILE_OK.
"""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys

ALLOWED = {"COMPILE_OK", "COMPILE_ERROR"}

def load(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def analyze(catalog_path, ledger_path, observations_path):
    catalog, ledger, observations = map(load, [catalog_path, ledger_path, observations_path])
    history = {(x["Project ID"], x["Status"], x["Example ID"]) for x in catalog}
    ccounts = Counter((p, s) for p, s, _ in history)
    projects = {p for p, _, _ in history}
    errs = []
    tally = Counter()
    seen = set()
    heads = set()
    if len(history) != 1386 or len(catalog) != 1390:
        errs.append(f"Unexpected catalog size: {len(history)} unique, {len(catalog)} relations")
    for x in observations:
        k = (x["project_id"], x["original_status"], x["example_id"])
        if k in seen:
            errs.append("duplicate compilation observation: " + "/".join(k))
        seen.add(k)
        if k not in history:
            errs.append("observation absent from immutable catalog: " + "/".join(k))
        status = x["cvl2_compile_only_observed"]
        if status not in ALLOWED:
            errs.append("invalid status: " + repr(status))
        if not x["evidence"].strip() or not x["snapshot_target"].strip():
            errs.append("missing target/evidence: " + "/".join(k))
        tally[(x["project_id"], status)] += 1
    rows = set()
    sums = Counter()
    for r in ledger:
        p = r["project_id"]
        if p in rows:
            errs.append("duplicated project ledger row: " + p)
        rows.add(p)
        if p not in projects:
            errs.append("project absent from catalog: " + p)
            continue
        complete, incomplete = ccounts[p, "complete"], ccounts[p, "incomplete"]
        total = complete + incomplete
        expected = {
            "catalog_examples": total,
            "catalog_complete": complete,
            "catalog_incomplete": incomplete,
            "round7_research_rows": total,
            "limited_cvl2_compile_ok": tally[p, "COMPILE_OK"],
            "round7_compile_only_errors": tally[p, "COMPILE_ERROR"],
        }
        for k, value in expected.items():
            try:
                actual = int(r[k])
                if actual != value:
                    errs.append(f"P{p} {k}={actual}; expected {value}")
            except (KeyError, ValueError) as e:
                errs.append(f"P{p} {k} invalid: {e}")
        try:
            not_run = int(r["round7_compile_only_not_run"])
            if not_run != total - tally[p, "COMPILE_OK"] - tally[p, "COMPILE_ERROR"]:
                errs.append(f"P{p} not_run count inconsistent")
            if r["round7_semantic_status"] != "NOT_DEMONSTRATED":
                errs.append(f"P{p} semantic evidence not in validated dataset")
            if int(r["semantic_equivalence_proven"]) != 0 or int(r["fully_migrated"]) != 0:
                errs.append(f"P{p} premature semantic/fully migrated promotion")
        except (KeyError, ValueError) as e:
            errs.append(f"P{p} invalid status: {e}")
        if len(r["research_head_sha"]) != 40:
            errs.append(f"P{p} invalid git HEAD SHA40")
        heads.add((r["agent"], r["research_head_sha"]))
        sums["not_run"] += int(r["round7_compile_only_not_run"])
    if rows != projects:
        errs.append("ledger project IDs differ from immutable catalog")
    if len(heads) != 8:
        errs.append(f"expected 8 distinct pinned agent heads, got {len(heads)}")
    result = {
        "catalog_examples": len(history),
        "catalog_relations": len(catalog),
        "projects": len(projects),
        "research_agent_heads": len(heads),
        "observed_cvl2_compile_ok": sum(v for (p, status), v in tally.items() if status == "COMPILE_OK"),
        "observed_cvl2_compile_error": sum(v for (p, status), v in tally.items() if status == "COMPILE_ERROR"),
        "untried_unique_examples": sums["not_run"],
        "semantic_equivalence_proven": 0,
        "projects_fully_migrated": 0,
        "errors": errs,
    }
    if result["observed_cvl2_compile_ok"] + result["observed_cvl2_compile_error"] + result["untried_unique_examples"] != len(history):
        errs.append("compiled/failed/untried partition does not sum to the catalog")
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", default="results/spec/spec_buglabel.csv")
    ap.add_argument("--ledger", default="docs/cvl2/coordination/ROUND7_PROGRESS.csv")
    ap.add_argument("--observations", default="docs/cvl2/coordination/ROUND7_COMPILATION_OBSERVATIONS.csv")
    opts = ap.parse_args()
    try:
        result = analyze(opts.catalog, opts.ledger, opts.observations)
    except (OSError, KeyError, UnicodeError, csv.Error) as e:
        print(f"Input error: {e}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
