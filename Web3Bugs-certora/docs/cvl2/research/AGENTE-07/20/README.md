# AGENTE-07 / Project 20 — Sushi BentoBox

**Somente pesquisa documental / FASE 1 — versão preliminar para revisão independente.**

## Baseline & exact historical inventory
- Repositório Web3Bugs/main: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; tree de origem `1d98ad19b420589be5a818f3f47fa2b227c72253`.
- Repositório PropertyGPT/main: `687f654c679ed45ab127b7949e2a29c8f5e491b9`; histórico `certora_projects/sushi_benttobox/`.
- Key canônica `(Project ID, Status original, Example ID)`; 37 dossiês únicos: 0 complete e 37 incomplete; registros de labels na indexação: 37.
- PDF histórico `resources/20/SushiBentoboxFeb2021.pdf`, texto auxiliar `reports/20.md`; commits históricos relatados: `0c68f2aa38cd600b5959197416fe090baa6a2a3f` (não presumir igualdade com snapshot).

## Semântica e riscos de migração
@boringcrypto não vendorizado; MAX_INT() indefinido no original; scripts contêm reescritas/harnesses.
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

## Rodada 4 — evidência técnica (2026-10-20)

Ver [matriz combinada dos 156 exemplos](../ROUND4_MATRIX.csv) e [revisão de fontes/scripts/imports](../ROUND4_EVIDENCE.md). Classificações históricas preservadas; nenhum COMPILE_OK ou SEMANTIC_SUPPORTED demonstrado.
