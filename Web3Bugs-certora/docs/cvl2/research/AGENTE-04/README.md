# AGENTE-04 — Fase 1 CVL2 — Pesquisa pré-migração (Projects 15, 12, 2)

## Identidade, escopo e base
- AGENTE-04, propriedade exclusiva dos Project IDs 15, 12 e 2. **Não é fase de implementação.**
- Web3Bugs/main fixado em `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; PropertyGPT/main `687f654c679ed45ab127b7949e2a29c8f5e491b9`. HEADs conferidos em 2026-10-19.
- Branch `research/cvl2-agente-04`, criada do commit fixado. PR somente documental, destinado a revisão independente antes de qualquer migração.
- **157 instâncias distintas** (chave project/status/example), 157 dossiês e 3 índices CSV completos; os Bug Labels históricos e as diferenças entre Result e Detection Outcome foram mantidos.

| Project | Name | Complete | Incomplete | Unique examples | Research path |
|---|---|---:|---:|---:|---|
| 15 | AAVE GHO Core | 0 | 116 | 116 | [Project 15](15/README.md) |
| 12 | AAVE Protocol V2 | 17 | 9 | 26 | [Project 12](12/README.md) |
| 2 | AAVE Proof of Reserve | 1 | 14 | 15 | [Project 2](2/README.md) |
| **Total** | | **18** | **139** | **157** | |

## Main concrete findings
- **Project 15:** source-era missing `@aave/core-v3` dependencies/mocks/.conf and exact Prover setup; GHO upstream audited commit `ce49fb0c94cfebf0159222ceb288e4f9a55d305f` exists. Current pinned historical CSV is **63 VERIFIED / 53 NOT_STATED**, not the older catalog markdown's 64/52, due to main adjudication for `balance_after_burn`.
- **Project 12:** 9 StableDebtTokenHarness cases blocked by superclass constructor/getter incompatibility. Do not replace the preserved Solidity with another version. 17 complete examples are only snapshot-dependency-complete, not CVL2 verified.
- **Project 2:** missing single-asset executor helpers/harnesses (`enableAsset`, `disableAsset`, `getAssetsLength`, `getAssetState`) and no proof mapping aggregate PDF invariants to every active source instance. Preserve source-level outcomes.
- **CVL2:** conditional candidates for `sinvoke`, `invoke`, method literals with `sig:`, `methods` syntax/internal-external/receiver, summaries, numeric casts, invariants and state. A syntactic transformation is not proof of equivalent semantics or a recovered dependency.

## Audit and gaps
- GitHub base-to-branch comparison (at initial QA check): 206 changed files and **157 property dossiers**, all exclusively within this AGENTE-04 research directory. Project CSV keys verified as 15 + 26 + 116, no duplicate or missing dossier paths.
- Each Project has `properties.csv`, `README.md`, `QA_REPORT.md`, `evidence_register.csv`, `recovery_manifest.csv`, `properties/` and reusable `patterns/`.
- Remaining gaps: page-by-page PDF check, independent byte matching for external upstream dependencies, canonical CLI/solc/config, exact receiver semantics and vacuity conditions, and experimental equivalence. These are explicit blockers/limits, not concealed successes.
- **No validation scripts or `git diff --check` were run on a live checkout; desktop device offline.** GitHub diff path inspection and CSV consistency checks were performed through the connector, not actual CVL compilation.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**

Aguardar revisão independente e autorização expressa para Fase 2. Não fazer merge nesta fase.

## Contrarrevisao 2026-10-19
Cobertura 157/157 (P15 116, P12 26, P2 15). Commits auditados 15:ce49fb0c94cfebf0159222ceb288e4f9a55d305f, 12:750920303e33b66bc29862ea3b85206dda9ce786, 2:12296ce4c6f9bde6663e1baa02cf19f179c1048b. PDF 13+25+6 paginas examinados; novos B1 registros, scripts de epoca, lock npm, diferenca de constructor V2 e ausencia de helpers Por identificados sem reconstrucoes. Sem CVL1, CVL2, Prover e sem alterar specs/Solidity. Status de fonte e ferramenta ainda incompleto; PR continua Draft.

## Segunda revisao independente - gate Fase 2
157/157 com campos separados de sintaxe, ABI pendente, dependencia historica, risco semantico e phase2 readiness. Todos UNRESOLVED, inclusive os 18 DOCUMENTED_CANDIDATE (17 P12 e 1 P2). Estudos: [GHO](15/HISTORICAL_PACKAGE_CLOSURE.md); [AAVE V2](12/HISTORICAL_HARNESS_COMPARISON.md); [Proof of Reserve](2/HISTORICAL_ABI_SEARCH.md). Buscas negativas encerradas nas fontes examinadas sem inventar runtime. Sem Fase 2, sem mudar codigo original.


## Rodada 4 — 2026-10-20

- [Matriz individual dos 157 exemplos e os cinco gates](ROUND4_PROGRESS.csv).
- [Confronto histórico P12 (17 candidaturas), P2 (1 candidatura), pacote P15 e contrarrevisão read-only de #40/#46](ROUND4_REVIEW.md).
- Todas as compilações e preservações semânticas permanecem não demonstradas; PR #42 Draft, nenhum merge/Fase 2.

## Rodada 5 — evidência CVL2 de 2026-10-20

- [Matriz individual — 157 examples, SHA-256, ABI, closure, compilação, próximo gate](round5/ROUND5_PROGRESS.csv).
- [Relatório técnico e tabela de fontes/linhas](round5/ROUND5_REVIEW.md).
- [P12 — 23/25: ABI e dois erros typechecker, logs integrais](round5/P12_TARGET_ABI_AND_DIAGNOSTICS.md).
- [P15 — lockfile, SRI, patch histórico e import closure de 5 famílias](round5/P15_PACKAGE_IMPORT_CLOSURE.md).
- [P2 — hashes de quatro Solidity e buscas negativas de ABI/harness](round5/P2_ABI_AND_NEGATIVE_SEARCH.md).
- [Cross-review read-only PRs #40/#46](round5/CROSS_AUDIT_PR40_46.md).

**Dois diagnósticos CVL2 com EXIT 1; nenhum COMPILE_OK/SEMANTIC_PROVEN; não há implementação derivada.**
