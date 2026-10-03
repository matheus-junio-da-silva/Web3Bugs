# Spec to Bug Label catalog

The catalog is stored in `results/spec/spec_buglabel.csv`.

For the full project-by-project extraction procedure, dependency audit, classification rules, and review checklist, see `docs/spec_catalog_workflow.md`.

For the completed AAVE L2 Bridge catalog (Project 1), coverage counts, unresolved dependencies, and validation notes are recorded in `docs/spec_catalog_project_1.md`.

## Directory layout

Examples are grouped first by dependency status and then by `Project ID`:

- `results/spec/complete/<project-id>/`
- `results/spec/incomplete/<project-id>/`

For each example, files with the same numeric stem belong together:

- `N.spec` — extracted CVL property plus the required CVL dependencies available in the project snapshot;
- `N.sol` — relevant Solidity source excerpts;
- `N.md` — Bug Label relationship, motivation, reconstructed methodology, source references, and dependency notes;
- `N.txt` — only for incomplete examples; explains the missing dependency.

## Complete vs. incomplete

An example is `complete` when every non-built-in symbol required by the extracted property can be resolved from the included CVL content or from files present in the project snapshot.

An example is `incomplete` when an original dependency needed by the property cannot be resolved from the available snapshot. The reason must be documented in `N.txt`.

`complete` refers only to dependency completeness within the available source snapshot. Migration from historical CVL syntax to CVL2 is intentionally handled separately.

## Bug Label mapping

`Bug Label` contains the related Web3Bugs label when a technically defensible mapping exists.

Classify what the property actually asserts, not what its name or comment suggests. Read the full property body and distinguish normative security properties from diagnostic or exploratory rules before assigning a label.

If no Web3Bugs label can be defensibly assigned, use `UNMAPPED`. `UNMAPPED` is a dataset sentinel, not a Web3Bugs taxonomy label.

The same property may appear in more than one CSV row when it has a defensible relationship with more than one Bug Label.

## Result

`Result` records the formal outcome stated by the original verification report, not the execution status of the extracted file and not the security interpretation of that result.

Use:
- `VERIFIED` — the report states that the property was verified;
- `VIOLATED` — the report states that the property was violated;
- `NOT_STATED` — the final report does not state an outcome for that property.

## Detection Outcome

`Detection Outcome` records what the formal result meant in the audit context.

Use:
- `FINDING` — the property result produced or directly supported a reported security finding;
- `ACCEPTED_BEHAVIOR` — the property exposed a behavior or counterexample, but the project explicitly treated it as intended, acceptable, or not a bug;
- `NO_FINDING` — the property did not produce a reported issue, typically because it was verified;
- `INCONCLUSIVE` — the available material is insufficient to determine whether the result represents a security issue;
- `NOT_STATED` — the report does not state enough information to determine the audit outcome.

`Result` and `Detection Outcome` are intentionally separate. For example, `VIOLATED` means a formal counterexample exists, while `FINDING` means that counterexample was interpreted as a reportable security issue.

Do not derive `Detection Outcome` mechanically from `Result` or `Bug Label`. A `VIOLATED` property may be a `FINDING`, `ACCEPTED_BEHAVIOR`, or `INCONCLUSIVE` depending on the report and project response. Likewise, an `O6` classification may correspond to accepted behavior in some cases, but the report must support that interpretation.

`Detection Outcome` does not replace `Bug Label`. `Bug Label` classifies the security intent/category, while `Detection Outcome` records what happened when the property was evaluated in the original audit.

## Target Contract

`Target Contract` identifies the contract against which the extracted property is intended to be interpreted or executed. This is distinct from `Original Contract`, which records the Solidity source file containing the code excerpt related to the property.

## Validation

Run `python scripts/check_specs.py .` from the repository root to validate the catalog structure. The validator checks CSV fields, Project IDs, allowed status/result/outcome values, Bug Labels, required artifact paths, complete/incomplete file requirements, multi-label row consistency, and unreferenced artifacts.

This structural validator does not compile CVL or rerun formal verification.

## Methodology notes

The `.md` files distinguish documented facts from reconstructed methodology. They do not claim access to private auditor reasoning.
