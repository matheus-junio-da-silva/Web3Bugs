#!/usr/bin/env python3
"""Audit recorded Certora compilation events; no claims of formal equivalence.

A property can have multiple attempts: CVL1-original, derived scratch, repeated
runner variants, or a failed import preflight. Count each property once in the
unique-tested denominator and never treat a setup error as a CVL2 parse error.
"""
import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parents[1]
CAT=BASE/"results/spec/spec_buglabel.csv"
EVENTS=BASE/"docs/cvl2/coordination/ROUND9_ATTEMPT_EVENTS.csv"
EXPECTED={
    "catalog_relationships":1390, "catalog_unique":1386,
    "events":33, "properties_tested_or_setup":20,
    "parser_or_compile_ok_events":11, "parser_or_compile_error_events":21,
    "environment_setup_errors":1, "properties_with_compile_ok":11,
    "properties_with_compile_error":16, "properties_with_both_outcomes":7,
    "properties_not_tested":1366,
}
def read(path):
    with Path(path).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))
def check(catalog,events):
    canonical_rows=read(catalog)
    keys={(r["Project ID"],r["Status"],r["Example ID"]) for r in canonical_rows}
    attempts=read(events)
    errors=[];per_property=defaultdict(set);count=Counter();seen=set()
    for row in attempts:
        k=(row["project_id"],row["original_status"],row["example_id"])
        if k not in keys:errors.append("noncanonical property: "+"/".join(k))
        if row["event_id"] in seen:errors.append("duplicate event ID: "+row["event_id"])
        seen.add(row["event_id"])
        result=row["observed_status"]
        if result not in ("COMPILE_OK","COMPILE_ERROR","SETUP_ERROR"):
            errors.append("bad outcome: "+repr(result))
        if row["semantic_equivalence"]!="NOT_DEMONSTRATED":
            errors.append("unsupported semantic promotion: "+"/".join(k))
        if result=="SETUP_ERROR" and row["exit_code"]!="1":
            errors.append("setup error must record nonzero exit")
        if result=="COMPILE_OK" and row["exit_code"]!="0":
            errors.append("compile ok without exit0")
        if result=="COMPILE_ERROR" and row["exit_code"]!="1":
            errors.append("compile error without exit1")
        for col in ("executor","target","evidence","input_kind"):
            if not row[col].strip():errors.append("missing "+col+": "+"/".join(k))
        for col in ("source_sha256","candidate_sha256"):
            s=row[col]
            if len(s)==64 and any(ch not in "0123456789abcdef" for ch in s):
                errors.append("invalid sha256: "+col+" "+row["event_id"])
        count[result]+=1
        per_property[k].add(result)
    ok={k for k,v in per_property.items() if "COMPILE_OK" in v}
    fail={k for k,v in per_property.items() if "COMPILE_ERROR" in v}
    metrics={
        "catalog_relationships":len(canonical_rows),
        "catalog_unique":len(keys),
        "events":len(attempts),
        "properties_tested_or_setup":len(per_property),
        "parser_or_compile_ok_events":count["COMPILE_OK"],
        "parser_or_compile_error_events":count["COMPILE_ERROR"],
        "environment_setup_errors":count["SETUP_ERROR"],
        "properties_with_compile_ok":len(ok),
        "properties_with_compile_error":len(fail),
        "properties_with_both_outcomes":len(ok&fail),
        "properties_not_tested":len(keys-set(per_property)),
    }
    for k,expected in EXPECTED.items():
        if metrics[k]!=expected:errors.append(f"{k}: expected {expected}, got {metrics[k]}")
    if (len(ok|fail)!=len(per_property)):
        errors.append("setup-only property incorrectly counted as CVL2 tested")
    if (len(ok|fail)!=len(ok)+len(fail)-len(ok&fail)):
        errors.append("inclusion/exclusion mismatch")
    return {"metrics":metrics,"errors":errors,"semantic_equivalences":0,"fully_migrated_projects":0}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--catalog",type=Path,default=CAT)
    p.add_argument("--events",type=Path,default=EVENTS)
    a=p.parse_args()
    try: result=check(a.catalog,a.events)
    except (OSError,ValueError,KeyError,csv.Error) as e:
        print(f"Input error: {e}",file=sys.stderr);return 2
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 1 if result["errors"] else 0
if __name__=="__main__":
    sys.exit(main())
