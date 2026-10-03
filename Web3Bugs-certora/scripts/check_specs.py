import csv
import os
import re
import sys

REQUIRED_COLUMNS = [
    "Project ID", "Status", "Example ID", "Bug Label", "Property",
    "Result", "Detection Outcome", "Target Contract", "Spec", "Code",
    "Documentation", "Incomplete Reason", "Original Spec",
    "Original Spec Lines", "Original Contract", "Original Contract Lines",
    "Detection Intent",
]

VALID_STATUSES = {"complete", "incomplete"}
VALID_RESULTS = {"VERIFIED", "VIOLATED", "NOT_STATED"}
VALID_OUTCOMES = {
    "FINDING", "ACCEPTED_BEHAVIOR", "NO_FINDING", "INCONCLUSIVE", "NOT_STATED"
}


def relative_file(root, value):
    return os.path.normpath(os.path.join(root, value))


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <web3bugs_dir>")
        return 1

    root = os.path.abspath(sys.argv[1].strip())
    catalog = os.path.join(root, "results", "spec", "spec_buglabel.csv")
    contests = os.path.join(root, "results", "contests.csv")
    standard = os.path.join(root, "docs", "standard.md")

    errors = []

    with open(contests, newline="", encoding="utf-8") as f:
        project_ids = {row["ID"].strip() for row in csv.DictReader(f)}

    with open(standard, encoding="utf-8") as f:
        standard_text = f.read()
    valid_labels = set(re.findall(r"__([A-Z][A-Z0-9-]*)__", standard_text))
    valid_labels.add("UNMAPPED")

    with open(catalog, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != REQUIRED_COLUMNS:
            errors.append(
                "Unexpected spec catalog columns. Expected: " + ", ".join(REQUIRED_COLUMNS)
            )
        rows = list(reader)

    groups = {}
    referenced_files = set()

    for line_no, row in enumerate(rows, start=2):
        prefix = f"spec_buglabel.csv:{line_no}"
        project_id = row["Project ID"].strip()
        status = row["Status"].strip()
        example_id = row["Example ID"].strip()

        if project_id not in project_ids:
            errors.append(f"{prefix}: unknown Project ID {project_id}")
        if status not in VALID_STATUSES:
            errors.append(f"{prefix}: invalid Status {status}")
        if not example_id.isdigit():
            errors.append(f"{prefix}: Example ID must be numeric: {example_id}")
        if row["Bug Label"].strip() not in valid_labels:
            errors.append(f"{prefix}: invalid Bug Label {row['Bug Label']}")
        if row["Result"].strip() not in VALID_RESULTS:
            errors.append(f"{prefix}: invalid Result {row['Result']}")
        if row["Detection Outcome"].strip() not in VALID_OUTCOMES:
            errors.append(f"{prefix}: invalid Detection Outcome {row['Detection Outcome']}")

        expected_base = f"results/spec/{status}/{project_id}/{example_id}"
        expected = {
            "Spec": expected_base + ".spec",
            "Code": expected_base + ".sol",
            "Documentation": expected_base + ".md",
        }
        for column, expected_path in expected.items():
            value = row[column].strip()
            if value != expected_path:
                errors.append(f"{prefix}: {column} must be {expected_path}, got {value}")
            full_path = relative_file(root, value)
            referenced_files.add(os.path.normpath(full_path))
            if not os.path.isfile(full_path):
                errors.append(f"{prefix}: missing {column} file {value}")

        reason = row["Incomplete Reason"].strip()
        if status == "incomplete":
            expected_reason = expected_base + ".txt"
            if reason != expected_reason:
                errors.append(
                    f"{prefix}: incomplete example must reference {expected_reason}"
                )
            reason_path = relative_file(root, reason)
            referenced_files.add(os.path.normpath(reason_path))
            if not os.path.isfile(reason_path):
                errors.append(f"{prefix}: missing incomplete reason file {reason}")
        elif reason:
            errors.append(f"{prefix}: complete example must leave Incomplete Reason empty")

        key = (project_id, status, example_id)
        stable_fields = [
            "Property", "Result", "Detection Outcome", "Target Contract", "Spec",
            "Code", "Documentation", "Incomplete Reason", "Original Spec",
            "Original Spec Lines", "Original Contract", "Original Contract Lines",
            "Detection Intent",
        ]
        signature = tuple(row[field] for field in stable_fields)
        previous = groups.get(key)
        if previous is None:
            groups[key] = signature
        elif previous != signature:
            errors.append(
                f"{prefix}: rows sharing Project ID/Status/Example ID disagree on artifact metadata"
            )

    artifacts_root = os.path.join(root, "results", "spec")
    for status in VALID_STATUSES:
        status_dir = os.path.join(artifacts_root, status)
        if not os.path.isdir(status_dir):
            errors.append(f"Missing directory: results/spec/{status}")
            continue
        for current_root, _, files in os.walk(status_dir):
            for filename in files:
                if filename.startswith("."):
                    continue
                full_path = os.path.normpath(os.path.join(current_root, filename))
                if full_path not in referenced_files:
                    rel = os.path.relpath(full_path, root)
                    errors.append(f"Unreferenced spec catalog artifact: {rel}")

    if errors:
        for error in errors:
            print(error)
        return 1

    print(
        f"Check passed! {len(groups)} spec examples and {len(rows)} Bug Label relationships are structurally consistent."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
