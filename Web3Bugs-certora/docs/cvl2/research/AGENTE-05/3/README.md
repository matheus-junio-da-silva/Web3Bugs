# AGENTE-05 / Project 3 — AAVE Rescue Mission / PHASE 1 RESEARCH

- Web3Bugs/main confirmed: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; PropertyGPT/main confirmed: `687f654c679ed45ab127b7949e2a29c8f5e491b9` on 2026-10-19.
- Original inventory: **3 unique examples**, **0 complete**, **3 incomplete**; 3 relationship rows with Bug Labels (not deduplicated by property name).
- Original source: `Web3Bugs-certora/contracts/3/`; PropertyGPT `certora_projects/aave_rescue_mission/`; PDF `resources/3/ (PDF histórico, consulte reports/3.md)`; catalog `docs/spec_catalog_project_3.md`.
- PDF audited version: `4c59da8d165751d053136f1711517cfa687c54c4 (relatório; múltiplas revisões)`, treated as historical claim, not matching evidence of every source file.
- **Historical blockers:** Specs coincidem com Certora Review 33c1aeca; Solidity de PropertyGPT é master posterior. O relatório também cita mitigação c905eaf; não há versão única demonstrada para todos os resultados.
- Per-case semantic risk counts: {"HIGH":2,"CRITICAL":1}; CVL2 candidate change markers: {"SEMI":3,"METH":3,"INVARIANT":2}. These are documentary triage tallies, not compile results.

## Files
`properties.csv` contains exactly one row per canonical key. `properties/{complete,incomplete}/N.md` are 3 individual source-linked dossiers. `patterns/` records specific official CVL2 rules, `evidence_register.csv` tracks direct evidence and URLs, `recovery_manifest.csv` historical dependencies, and `QA_REPORT.md` counts and checks.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.** Neither complete nor historical VERIFIED means a new proof.
