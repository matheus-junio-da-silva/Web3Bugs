# AGENTE-05 QA REPORT — P19 / Final source-read audit

## Reconciliation
- Project ID 19 contains 37 exactly unique source-indexed examples, including 2 complete and 35 incomplete. No duplicate (Project ID, Status, Example ID) key.
- Full original .spec files read and property declarations located at source coordinates: 37/37. Full numbered N.spec, N.md, N.sol read: 37 each; numbered N.txt read: 35/35 applicable incomplete.
- Individual property reports present: 37/37. Original Results, Detection Outcomes and Bug Labels copied without semantic reclassification; 148-project total is checked separately.
- CVL1→CVL2 source-specific candidate snippets with line and A1 citations stored in dossiers. For methods-only cases with receiver ambiguity, candidate state stays unresolved. All future buckets are provisional.
- Research statuses: {'UNCHANGED_CANDIDATE': 2, 'UNRESOLVED_CANDIDATE': 35}. Every property retains some form of untested ABI/semantic equivalence uncertainty.

## PDF and historical evidence
- Historical PDF bytes hashed SHA256, and reports/19.md transcript searched for matching exact property names. Official web PDF pages checked visually: 0. Public PDF identity with archived resource is NOT proven.
- Original lockfile pins @openzeppelin/contracts 2.5.0 and upgrades 2.8.0, not recovered. Scripts modify OUSD harness and not all targets are interchangeable.

## Observed structural validation in WSL
- CWD Web3Bugs-certora: python3 scripts/check_specs.py . returned exit 0, 1386 examples / 1390 Bug Label relationships.
- CWD Web3Bugs-certora: python3 scripts/check_contests_csv.py . returned exit 0.
- CWD Web3Bugs-certora: python3 scripts/check_contracts.py . returned exit 0.
- CWD Web3Bugs: git diff --check returned exit 0 after documentary formatting changes, without modifying historical sources.
- Staged diff check to be performed immediately before the Git commit.

## Outstanding limitations
- No Certora Prover, CVL1, CVL2 compilation, source reconversion, or experimental same-counterexample checks. No verified snapshot-to-reviewed-commit ABI or complete dependency reconstruction from source hashes. Direct original PDF pages for Projects 7 and 19 were not renderable; transcript is not a direct page check.
- Strictly documentation-only changes under AGENTE-05/19/. Independent semantic and version/ABI review remains necessary before any merger or Phase 2.
