# AGENTE-06 — Resposta à revisão do PR #38 (pesquisa ainda bloqueada)

## Cobertura documentada

- P1 70 (36 complete/34 incomplete), P17 41 (31/10), P4 27 (0/27), P22 21 (19/2): 159/159 itens na matriz, N.spec/N.md/N.sol identificados e lidos com hashes SHA256, N.txt dos 73 incomplete registrados.
- 3 validadores oficiais rodados em worktree isolada, exit 0; git diff --check exit 0 ao final (reexecutar ao publicar).
- Originais PDF p4 (9 páginas), p17 (47), p22 (10) extraídos textualmente, SHA256 registrado; p1 binário ausente, reports/1.md consultado.
- Nenhum compiler, CVL1, CVL2, Prover ou script de migração foi executado.

## Resultado da pesquisa por projeto

- P1: O commit 303bd3 do Solidity do relatório não determina por si a configuração de cada rule. queue2/_mock e complexity.spec não receberam ABI ou runner originais demonstrados; os contratos de Polygon, Optimism e Arbitrum mantêm diferenças de autenticação.
- P17: Specify 2019 com aliases .spclnk JSON, ambientes, sinvoke/invoke, havoc local e static_assert/static_require não equivale a CVL1 usual. Falta prova da semântica histórica do engine e reversão.
- P4: Existe provenance do src auditado mas o Makefile gera munged por patch e o snapshot não contém src/munged completos. Não se fabricou harness. Os 27 incomplete permanecem incomplete.
- P22: O runner preservado fixa --verify PopsicleV3Optimizer:spec/PopsicleV3Optimizer.spec com --rule $1, --solc solc7.6, --loop_iter 1 e --link tokens/pool. Sem prova de execução de FullMathWrapper, PoolActions ou sanity. Wrapper sem getter totalSupply.

## Semântica e nível de confiança

Todos permanecem UNRESOLVED_CANDIDATE. A segunda passada agrega evidência concreta de texto da rule, da metodologia catalogada, N.sol, limites de runner, proveniência e elementos oficiais A1/A2. **Não comprova equivalência CVL1/Specify→CVL2**, fechamento de import/transitive ABI nem preservação de toda a seleção histórica de rules. A leitura PDF por texto e os matchers de símbolos são auxiliares, não revisões formais.

### Prioridade futura

1. Recuperar execução histórica por projeto com hashes de harness e configuração realmente auditados; sem sintetizar dependências.
2. Adjudicar construto Specify por semântica (P17), receiver/ABI (P1), munged/patch (P4), seleção exata de rules (P22).
3. Somente após contrarrevisão e autorização coordenadora, implementar Fase 2 em branch diferente, com equivalência e não vacuidade.

**DECISÃO: manter PR #38 DRAFT; sem merge. ALERTA: LARANJA — pesquisa documental avançada, bloqueios semânticos permanecem.**
