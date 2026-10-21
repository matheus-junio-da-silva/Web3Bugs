# AGENTE-05 — Validation log / Phase 1 documentary-only

Execution host: authorized WSL DESKTOP-5E26TVU, isolated checkout at /home/mat/cvl2-agent05-isolated/Web3Bugs.
HEAD input: e50ab590be2d521ff0dca85b837a89f2d6243f71; main baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3.

- CWD Web3Bugs-certora; python3 scripts/check_specs.py . -> exit code 0; output: Check passed! 1386 spec examples and 1390 Bug Label relationships are structurally consistent.
- CWD Web3Bugs-certora; python3 scripts/check_contests_csv.py . -> exit code 0; report/contests consistent.
- CWD Web3Bugs-certora; python3 scripts/check_contracts.py . -> exit code 0; contracts/reports consistent.
- CWD Web3Bugs; git diff --check -> exit code 0 after formatting documentary whitespace. Staged check will be run before commit and recorded in the PR discussion.
- Source research script read all individual original spec, N.spec, N.md, N.sol and N.txt (where incomplete). Source contracts never overwritten. Markdown quotes have trailing blanks and tabs normalized for git checks; preserved historical sources and their SHA256 are unchanged.
- NOT RUN: Certora Prover, CVL1 compilation/tests, CVL2 compilation, migrator, Solidity compile or historical harness replay.
