# Project 1 — AAVE L2 Bridge Spec Catalog

This document records the completion state of the Certora property catalog for Project 1.

## Coverage

- `PolygonBridge.spec`: 32 active properties
- `Optimism_ArbitrumBridge.spec`: 32 active properties
- `complexity.spec`: 6 active properties
- Total active property instances: **70**
- Bug Label relationship rows in `spec_buglabel.csv`: **72**

The additional CSV rows come from properties that map to more than one Bug Label. The commented-out `gracePeriodChangedAffectsExecution` rule is not counted as active.

## Dependency status

- Complete examples: **36**
- Incomplete examples: **34**

`complete` means dependency-complete within the available snapshot. It does not mean CVL2-compatible or re-verified with the current Certora Prover.

Known missing/unresolved dependencies affect examples as follows. Counts overlap when one property has more than one missing dependency:

- `queue2`: 14 examples
- `_mock(env)`: 6 examples
- `getActionsSetCanceled`: 8 examples
- `getActionsSetExecuted`: 8 examples
- `getActionsSetExecutionTime`: 2 examples
- `ID2actionHash`: 4 examples
- unresolved original target/run configuration for `complexity.spec`: 6 examples

## Formal results

Across the 70 source property instances:

- `VERIFIED`: 44
- `VIOLATED`: 2
- `NOT_STATED`: 24

Audit interpretation:

- `NO_FINDING`: 44
- `FINDING`: 2
- `NOT_STATED`: 24

`independentQueuedActions` exists in both bridge specs. The final report states the named property was violated and links it to the issue `Unexpected revert of queued actions`; the catalog therefore attaches the report-level result to both source instances. This represents one reported issue, not two separate findings.

The reported issue is classified as `O1` in `results/bugs.csv`. The extracted property is mapped to `S2-3` because `S2-3` describes its technical detection intent (an ID/hash uniqueness collision). These are intentionally separate classification views.

The two `O6` findings in the report are not force-linked to a formal property because the final report does not explicitly identify a source property as their detector.

## Source integrity

The original source specs under `contracts/1/specs/` were not modified during catalog generation. Their SHA-256 fingerprints were checked against the pre-catalog values.

The temporary `.certora_internal` directory created during local type-check experiments was removed from the project snapshot.

## Validation

The catalog passes:

```text
python scripts/check_specs.py .
python scripts/check_contests_csv.py .
python scripts/check_contracts.py .
```

`check_specs.py` validates the catalog structure, allowed enum values, Project IDs, artifact paths, complete/incomplete file requirements, shared metadata for multi-label rows, and orphan artifacts.

It does not prove CVL semantics, compile historical CVL syntax, or rerun the original formal verification.

## CVL version note

The source bridge specs use historical CVL syntax. CVL2 migration is intentionally deferred. A property can therefore be dependency-complete while still requiring future syntax migration before execution with a current Certora CLI.

## Catalog locations

- Index: `results/spec/spec_buglabel.csv`
- Complete examples: `results/spec/complete/1/`
- Incomplete examples: `results/spec/incomplete/1/`
- Catalog format: `docs/spec_catalog.md`
- Reproduction workflow: `docs/spec_catalog_workflow.md`

## CERES semantic corrections — 2026-10-18

Exactly 64 generic Solidity descriptions have been rewritten: complete/1 IDs 1–36 and incomplete/1 IDs 1–28. Each now identifies the actual CVL assertion, guards, relevant preserved Solidity implementations, legal changes, a falsifying execution, target-chain differences and missing historical helpers.

The source rule whoChangesActionsSetState at complete/1/15 (Polygon) and complete/1/32 (Optimism/Arbitrum) filters only non-view f and imposes identical getCurrentState before/after. execute deliberately sets _actionsSets[id].executed=true; cancel sets _actionsSets[id].canceled=true. Both can legitimately change that computed state, so the raw unconditional equality is an over-restrictive diagnostic oracle, not a sound S3-2 classification. Both mappings changed to UNMAPPED without altering their CVL, Solidity, Result or Detection Outcome.

The six incomplete/1 IDs 29–34 from complexity.spec retain their missing target/harness evidence. The Project 1 original PDF is not present in the current snapshot; reports/1.md remains its historical transcript. The requested instrucoes-obrigatorias.txt is also absent from this Git tree. These limitations are documented, not fabricated.
