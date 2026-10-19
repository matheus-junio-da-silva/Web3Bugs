# AGENTE-04 — FASE 1 / PESQUISA CVL2 — Project 15 AAVE GHO Core

## Fixed inputs and inventory
- Web3Bugs main fixed at `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` and PropertyGPT main at `687f654c679ed45ab127b7949e2a29c8f5e491b9` on 2026-10-19.
- Audited upstream AAVE GHO commit [ce49fb0](https://github.com/aave/gho-core/commit/ce49fb0c94cfebf0159222ceb288e4f9a55d305f). Commit existence and tree verified; catalog states original 22/22 Solidity blobs and 8/9 spec blobs match, with shortened ghoDiscountRateStrategy.spec. The external package dependency closure was **not** established.
- **116** unique examples indexed, **0 complete / 116 incomplete** in the historic catalog. Source specs by family:
- `contracts/15/flashMinter.spec`: 6
- `contracts/15/ghoAToken.spec`: 7
- `contracts/15/ghoDiscountRateStrategy.spec`: 1
- `contracts/15/ghoToken.spec`: 28
- `contracts/15/ghoVariableDebtToken.spec`: 25
- `contracts/15/set.spec`: 27
- `contracts/15/VariableDebtToken.spec`: 22
- Historical outcomes of the current pinned CSV: **63 VERIFIED / 53 NOT_STATED**, 0 VIOLATED. This supersedes the older Project 15 catalog markdown's 64/52 counts after the Web3Bugs `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` semantic adjudication, which set `balance_after_burn` NOT_STATED due to PDF/source conflict.
- Original report: `resources/15/Aave_Gho_Formal_Verification_Report.pdf` (published 2023-03-07); text transcript `reports/15.md`. Historical PDF SHA256 documented in catalog: `ced8ba5de87ae727c0df889d5e916f32a759394465acf1ce83b1afddf832df06`. No page-by-page reinspection in this dossier batch; the original PDF is the canonical source.

## Organization and decision boundaries
- `properties.csv` = exactly 116 source instances by `(Project ID, original_status, example_id)`, not Bug Label rows.
- `properties/incomplete/<N>.md` = individual CVL, local assertions, original Result / Detection Outcome, N.txt provenance, risk and conditional migration plan.
- `patterns/` = shared language changes with explicitly listed applicable example IDs. `evidence_register.csv` = source hierarchy/URLs; `recovery_manifest.csv` = missing-dependency groups with uncertainties; `QA_REPORT.md` = reconciliation and outstanding work. `batches/` = audit trace of inputs and intermediate CSV aggregation.
- The source snapshot's shared family mocks, `@aave/core-v3` transitive imports, original Solidity compiler/remappings and Certora Prover run configuration remain unresolved. A syntax migration would not repair that missing provenance.
- The official guide warns about in-place scripts, method receiver changes and `require_` casts suppressing counterexamples; therefore only candidates, no automatic source rewrite. Summaries, ghost/hook state, preserved invariants, quantification and WAD/RAY/BPS bounds require independent proof of preserved meaning.
- Independent report-to-source mismatches (including absent timelock rule) are carried as historical context only, never reclassified as an active source instance.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**

## Contrarrevisao 2026-10-19
O commit auditado fornece npm lock @aave/core-v3@1.17.2 com integridade SHA512, cinco scripts Certora de epoca e harnesses de GHO; .conf/CLI/binarios de epoca, pacote realmente instalado e munged execution nao foram reproduzidos. CSV fixo 63 VERIFIED versus 64 do catalogo antigo mantido sem mudanca.

Dossies atualizados 116/116; entradas methods por instancia 1251; nomes literais encontrados em PDF 64. Propostas report-only e condicionais; nao houve compilacao, Prover, teste CVL1 ou modificacao de fonte. Buscas negativas nao demonstram inexistencia fora da arvore examinada.
