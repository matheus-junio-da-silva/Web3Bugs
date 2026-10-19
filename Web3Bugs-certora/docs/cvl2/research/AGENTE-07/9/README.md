# AGENTE-07 / Project 9 — Celo Governance

**Somente pesquisa documental / FASE 1 — versão preliminar para revisão independente.**

## Baseline & exact historical inventory
- Repositório Web3Bugs/main: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; tree de origem `1d98ad19b420589be5a818f3f47fa2b227c72253`.
- Repositório PropertyGPT/main: `687f654c679ed45ab127b7949e2a29c8f5e491b9`; histórico `certora_projects/celo_governance/`.
- Key canônica `(Project ID, Status original, Example ID)`; 61 dossiês únicos: 50 complete e 11 incomplete; registros de labels na indexação: 61.
- PDF histórico `resources/9/CeloMay2020.pdf`, texto auxiliar `reports/9.md`; commits históricos relatados: `9d2ec0d9399a6959565062f57efa037d03fd4fbc; a46ce55ebd3867fa69290bf3be040846d433525d` (não presumir igualdade com snapshot).

## Semântica e riscos de migração
Governance antiga ativa, métodos/summaries, inconsistências ABI e helpers sem ligação histórica comprovada.
Separar (a) dependência histórica ausente; (b) divergência do código realmente auditado; (c) defeito original de spec; (d) sintaxe/semântica CVL2; (e) ambiente/CLI/solc.
Sem evidência de reexecução CVL1 ou CVL2; complete histórico não significa prova compilável.

## Artefatos
- `properties.csv`: 1 linha por exemplo único, sem multiplicação por Bug Label.
- `properties/<original_status>/<N>.md`: dossiê caso a caso, com literal/extrato CVL e limitações.
- `patterns/`: notas de incompatibilidades com fontes oficiais, exigindo aplicação específica por dossier.
- `evidence_register.csv`: A1/A2 e documentação local C2, com proveniência e limites.
- `recovery_manifest.csv`: uma linha por incomplete, sem inventar hash ou commit.
- `QA_REPORT.md`: reconciliação, fontes ausentes e validações efetivamente realizadas.

SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.

## Full-source follow-up
See full_spec_audit.csv and the integral-source appendix in each property dossier. It records full extracted source hashes, exact lines, and conditional CVL2 candidates without altering originals.
