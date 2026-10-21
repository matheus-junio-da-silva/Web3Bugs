# AGENTE-08 — Decisao consolidada apos segunda auditoria independente
PR #43: https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43
Revisao da segunda rodada: https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43#pullrequestreview-5577013034

**Fase 1 documentaria; 155/155 UNRESOLVED_CANDIDATE e nenhuma implementacao CVL2 autorizada.**

| Projeto | Exemplos | Historic Result indexado | Comprovado | Recuperavel sob condicao | Bloqueio efetivo |
|--|--:|--|--|--|--|
| P13 Notional | 58 | 5 VERIFIED; 53 NOT_STATED | scripts solc7.5 e Brownie; CSV/catalog divergentes #32/#34 | package lock, target Balances, ABI historica via mantenedor | 48 imports, 10 targets sem prova |
| P23 Radicle | 46 | 15 VERIFIED; 1 VIOLATED; 30 NOT_STATED | PDF formal scoped Splits.sol, #36 rounding e #38 timeout | harness, CVT generated wrappers, report run artifacts | 46 cenas nao reconstituidas; Splits2 independente |
| P14 Opyn | 34 | 19 VERIFIED; 15 NOT_STATED | scripts e patches conhecidos, 31 promotions revertidas | ABI pos-patch, solc alias por run, receiver e summaries | 34 cenas nao autenticadas |
| P5 StarkNet | 17 | 6 VERIFIED; 4 VIOLATED; 7 NOT_STATED | blobs upstream e scripts solc8.10, links, patch | import closure e tree munged da revisao auditada | 17 cenas nao integralmente reproduzidas |

**Interpretacao:** Resultado historico indexado nao prova compilacao CVL2, e ausencia de artefato em snapshot/indice publico nao prova impossibilidade de reconstruir. Bloqueio representa insuficiencia das fontes examinadas. O levantamento das buscas foi encerrado *dentro de um escopo delimitado* para evitar consultas repetitivas sem nova pista.

## Rastreabilidade
P13: 13/HISTORICAL_BLOCKERS.md, 13/historical_status.csv, 13/RECOVERY_SEARCH_LOG.md.
P23: 23/HISTORICAL_BLOCKERS.md, 23/historical_status.csv, 23/RECOVERY_SEARCH_LOG.md.
P14: 14/HISTORICAL_BLOCKERS.md, 14/historical_status.csv, 14/RECOVERY_SEARCH_LOG.md.
P5: 5/HISTORICAL_BLOCKERS.md, 5/historical_status.csv, 5/RECOVERY_SEARCH_LOG.md.

**Intervencao humana:** Coordenador/mantenedores devem fornecer execucoes historicas, ABI e versoes/hashes dos artefatos ausentes, ou aceitar registros permanentemente unresolved. Nenhuma spec, assert, assume, source Solidity, CSV historico, PDF, compile, Prover ou branch de outros agentes foi alterado. Manter PR Draft e proibicao de merge/Fase 2.
