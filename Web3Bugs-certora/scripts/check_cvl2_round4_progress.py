#!/usr/bin/env python3
"""Validate the Round-4 CVL2 coordination ledger without touching historic data.

This is an *accounting* check, not evidence of CVL2 compilation or equivalence.
The eight unmerged research PRs must still be reviewed independently.
"""
import argparse
import csv
import json
from pathlib import Path
import sys


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def verify(catalog, ledger):
    baseline = read_csv(catalog)
    unique = {
        (row["Project ID"], row["Status"], row["Example ID"])
        for row in baseline
    }
    by_project = {}
    for project, status, example in unique:
        counts = by_project.setdefault(project, {"complete": 0, "incomplete": 0})
        counts[status] += 1

    entries = read_csv(ledger)
    errors, found, compiled, semantic, migrated = [], set(), 0, 0, 0
    for row in entries:
        project = row["project_id"]
        if project in found:
            errors.append(f"duplicate P{project} in ledger")
        found.add(project)
        if project not in by_project:
            errors.append(f"unknown P{project}")
            continue
        correct = by_project[project]
        expected_total = correct["complete"] + correct["incomplete"]
        for key, target in (
            ("catalog_examples", expected_total),
            ("catalog_complete", correct["complete"]),
            ("catalog_incomplete", correct["incomplete"]),
            ("round4_research_rows", expected_total),
        ):
            if int(row[key]) != target:
                errors.append(f"P{project} {key}: {row[key]} != {target}")
        if len(row["research_head_sha"]) != 40:
            errors.append(f"P{project}: research head is not full SHA40")
        values = {key: int(row[key]) for key in (
            "limited_cvl2_compile_ok", "semantic_equivalence_proven", "fully_migrated"
        )}
        if not (0 <= values["semantic_equivalence_proven"] <= values["limited_cvl2_compile_ok"] <= expected_total):
            errors.append(f"P{project}: inconsistent proof or compile count")
        if values["fully_migrated"] not in (0, 1):
            errors.append(f"P{project}: fully_migrated is not Boolean")
        if values["fully_migrated"] and values["semantic_equivalence_proven"] != expected_total:
            errors.append(f"P{project}: project marked migrated without all examples proven")
        compiled += values["limited_cvl2_compile_ok"]
        semantic += values["semantic_equivalence_proven"]
        migrated += values["fully_migrated"]

    if found != set(by_project):
        errors.append(f"project keys differ; missing={sorted(set(by_project)-found)}")
    result = {
        "catalog_unique_examples": len(unique),
        "catalog_buglabel_relationship_rows": len(baseline),
        "projects": len(by_project),
        "researched_examples_in_ledger": sum(int(x["round4_research_rows"]) for x in entries),
        "limited_compile_only_examples": compiled,
        "semantic_equivalence_proven": semantic,
        "projects_fully_migrated": migrated,
        "errors": errors,
    }
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", type=Path, default=Path("results/spec/spec_buglabel.csv"))
    p.add_argument("--ledger", type=Path, default=Path("docs/cvl2/coordination/ROUND4_PROGRESS.csv"))
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    try:
        result = verify(args.catalog, args.ledger)
    except (OSError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Round-4 ledger:", {k: v for k, v in result.items() if k != "errors"})
        for e in result["errors"]:
            print("ERROR:", e, file=sys.stderr)
    return bool(result["errors"])


if __name__ == "__main__":
    sys.exit(main())
