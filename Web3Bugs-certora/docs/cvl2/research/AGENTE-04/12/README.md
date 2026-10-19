# AGENTE-04 — Fase 1 CVL2 / Project 12 AAVE Protocol V2

- Web3Bugs HEAD `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; PropertyGPT HEAD `687f654c679ed45ab127b7949e2a29c8f5e491b9` (confirmados 2026-10-19).
- **26** instâncias: **17 complete**, **9 incomplete**, sem multi-label duplicates. StableDebtToken 9 incomplete, VariableDebtToken 9 complete, UserConfiguration 8 complete.
- Relatório `reports/12.md` / PDF `resources/12/AaveV2Dec2020.pdf`. Último commit mencionado no PDF `750920303e33b66bc29862ea3b85206dda9ce786` (blobs upstream ainda não verificados independentemente).
- São 26 instâncias individualizadas com as fontes CVL extraídas, hashes de Git blob e planos locais CVL2; 9 N.txt examinados.
- StableDebtTokenHarness superclass incompatível (construtor/getIncentivesController), não resolver com source version arbitrária; ✔* indica prova com arredondamento simplificado. Não associar defeito de rounding à assert específica sem causalidade do PDF.
- Arquivos: `properties.csv`, `properties/`, `patterns/`, `evidence_register.csv`, `recovery_manifest.csv`, `QA_REPORT.md`; `batches/` trilha dos lotes lidos.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**
