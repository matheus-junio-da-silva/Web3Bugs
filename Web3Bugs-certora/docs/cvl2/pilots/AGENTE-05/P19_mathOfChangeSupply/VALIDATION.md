# AGENTE-05 — Compilation-only pilot: structural validation

Execution: isolated WSL clone of Web3Bugs/main baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3.

* scripts/check_specs.py: exit 0, 1386 examples and 1390 Bug Label relationships consistent.
* scripts/check_contests_csv.py: exit 0.
* scripts/check_contracts.py: exit 0.
* git diff --cached --check: checked and passed after normalizing diagnostic log final blank lines.
* Source and target copies: cmp byte-identical; source and target SHA256 values in results.json.
* Pilot 1: COMPILE_ERROR, exit 1, 3224 ms.
* Pilot 2: COMPILE_ERROR, exit 1, 3419 ms.
* Pilot 1 environment preflight: exit 1, 2320 ms; missing solc_select from isolated HOME resolved by using preinstalled native solc.
* No formal verification, CVL1, source edits, CI Prover or CVL2 migration was executed.
