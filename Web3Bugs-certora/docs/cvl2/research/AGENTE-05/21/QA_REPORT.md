# AGENTE-05 QA REPORT — P21 / Final source-read audit

## Reconciliation
- Project ID 21 contains 2 exactly unique source-indexed examples, including 0 complete and 2 incomplete. No duplicate (Project ID, Status, Example ID) key.
- Full original .spec files read and property declarations located at source coordinates: 2/2. Full numbered N.spec, N.md, N.sol read: 2 each; numbered N.txt read: 2/2 applicable incomplete.
- Individual property reports present: 2/2. Original Results, Detection Outcomes and Bug Labels copied without semantic reclassification; 148-project total is checked separately.
- CVL1→CVL2 source-specific candidate snippets with line and A1 citations stored in dossiers. For methods-only cases with receiver ambiguity, candidate state stays unresolved. All future buckets are provisional.
- Research statuses: {'UNRESOLVED_CANDIDATE': 2}. Every property retains some form of untested ABI/semantic equivalence uncertainty.

## PDF and historical evidence
- Historical PDF bytes hashed SHA256, and reports/21.md transcript searched for matching exact property names. Official web PDF pages checked visually: 2. Public PDF identity with archived resource is NOT proven.
- The two DSM rules do not match the 18 named PDF properties. Harness/getGuardianLength absent and authorized quorum may exceed guardian count.

## Observed structural validation in WSL
- CWD Web3Bugs-certora: python3 scripts/check_specs.py . returned exit 0, 1386 examples / 1390 Bug Label relationships.
- CWD Web3Bugs-certora: python3 scripts/check_contests_csv.py . returned exit 0.
- CWD Web3Bugs-certora: python3 scripts/check_contracts.py . returned exit 0.
- CWD Web3Bugs: git diff --check returned exit 0 after documentary formatting changes, without modifying historical sources.
- Staged diff check to be performed immediately before the Git commit.

## Outstanding limitations
- No Certora Prover, CVL1, CVL2 compilation, source reconversion, or experimental same-counterexample checks. No verified snapshot-to-reviewed-commit ABI or complete dependency reconstruction from source hashes. Direct original PDF pages for Projects 7 and 19 were not renderable; transcript is not a direct page check.
- Strictly documentation-only changes under AGENTE-05/21/. Independent semantic and version/ABI review remains necessary before any merger or Phase 2.
