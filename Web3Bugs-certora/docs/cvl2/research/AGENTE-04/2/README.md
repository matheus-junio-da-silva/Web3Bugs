# AGENTE-04 — Project 2 / AAVE Proof of Reserve (FASE 1)

- Base Web3Bugs `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; PropertyGPT HEAD `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Exatamente **15** exemplos catalogados: **1 complete, 14 incomplete** (15 relações de Bug Label).
- Originais `contracts/2/specs/{aggregator,executorV2,executorV3}.spec`; PDF `resources/2/Aave-Proof-of-Reserve-Formal-Verification-Report.pdf`; relatório `reports/2.md`.
- Helpers (como `enableAsset`, `getAssetState`, `getAssetsLength`) faltam no snapshot; não propor reescrita como se fossem incompatibilidades CVL2.
- Faltam prova do commit upstream auditado e configuração de Prover; não promover resultados PDF agregados a invariants específicos.
- Consulte `properties.csv`, `properties/`, `patterns/`, `evidence_register.csv`, `recovery_manifest.csv`, `QA_REPORT.md`.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**

## Contrarrevisao 2026-10-19
PDF p.1 indica commit 12296ce agora resolvido integralmente. Quatro Solidity do snapshot coincidem byte-a-byte com commit auditado; tree nao contem specs/auxiliares CVL. PDF summary arbitario e invariants agregadas nao individualizadas sem origem CVL.

Dossies atualizados 15/15; entradas methods por instancia 50; nomes literais encontrados em PDF 10. Propostas report-only e condicionais; nao houve compilacao, Prover, teste CVL1 ou modificacao de fonte. Buscas negativas nao demonstram inexistencia fora da arvore examinada.
