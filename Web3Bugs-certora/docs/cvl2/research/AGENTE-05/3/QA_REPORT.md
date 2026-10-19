# AGENTE-05 QA REPORT — Project 3

## Inventory reconciliation at 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3
- GitHub directory listing: 3 numbered .spec files: 0 complete and 3 incomplete.
- Proper CSV parse with double-quoted comma/newlines: 3 Bug Label relationships reduced to 3 unique keys (Project ID, original Status, Example ID). Dossiers created: 3, with mandatory .spec, .md and .txt for incomplete all read directly from HEAD.
- There are 8 missing-source manifest records (one aggregate entry per incomplete plus independently traced historic assets where present).
- Count of candidate syntax flags: {"SEMI":3,"METH":3,"INVARIANT":2}. Risk distribution: {"HIGH":2,"CRITICAL":1}.

## Critical decisions
- Specs coincidem com Certora Review 33c1aeca; Solidity de PropertyGPT é master posterior. O relatório também cita mitigação c905eaf; não há versão única demonstrada para todos os resultados.
- Historical BGD-Labs commit 33c1aeca28d6d61659c1b28775ad2644b7e2ac6e and five blob hashes of scripts/harnesses independently confirmed; recovery classification is separate from original incomplete status.
- Textual edits are conditional and can alter receiver scope, revert paths or bounds; original Solidity excerpts are documentary and not stand-alone compile units.

## Executed vs not executed
**Executed:** GitHub read-only queries for both repository HEADs, per-project contents inventories, full individual spec/md/txt documents, historical CSV parsing, deduplication by canonical key, current official CVL2 guidance research. Write: only documents in this AGENTE-05/3 directory, separate research branch.

**Not executed:** `python3 scripts/check_specs.py .`, `python3 scripts/check_contests_csv.py .`, `python3 scripts/check_contracts.py .`, `git diff --check` on a current checkout; no relevant synced workstation was online and the user-provided ZIP is older than main. No compiler/solc/Certora Prover/CVL1 test, no in-place converter. Do not invent exit codes or equivalence/verification.

**Independent review still needed:** full ABI/method receiver audit; audited-source hash and historical scripts; actual CVL2 errors and same-counterexample reasoning in a subsequently authorized Phase 2.
