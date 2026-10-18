# Project 18 — 181-row per-target Solidity / CVL evidence matrix

Machine-readable evidence table: docs/spec_catalog_project_18_semantic_matrix.csv. Each of its 181 rows records the original CVL source lines, observable calls, literal predicate, actual Solidity method/modifier/declaring file and line, storage, absent harness, and historical result scope. Original N.sol excerpts now copy those concrete source locations verbatim; N.md contains the per-property call sequence, source-line-specific preconditions, runtime branch and counterexample interpretation. A cited base method does not replace unavailable historical harnesses.

The four VIOLATED/FINDING outcomes refer only to revisions described on PDF p. 2, not verified failures on the latest reviewed revision. Timelock has no broken rule in the report. No imported/unfinished Governor rule is promoted to VERIFIED. Original Certora scripts, proof settings and harness munging remain absent.

Literal closing-brace trailing spaces restored where the original source line includes them. Original Solidity snapshots and PDF remain untouched.
