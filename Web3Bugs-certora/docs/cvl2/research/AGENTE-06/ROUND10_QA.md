# AGENTE-06 — Rodada 10: QA e estado de execução

**PR #38:** Draft; HEAD inicial confirmada c07432f9c81843be532eec5c4f792143aaabde59. Baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. Pasta exclusiva AGENTE-06. Nenhum dado histórico modificado.

## Controles realmente efetuados

- Leitura completa dos quatro documentos obrigatórios e exemplos complete/incomplete de P1 via GitHub.
- Comparação por chave de ROUND9_MATRIX_159.csv com results/spec/spec_buglabel.csv canônico: **159 chaves distintas (70 P1, 27 P4, 41 P17, 21 P22)**, zero discrepâncias em Property, Target, Result, Detection Outcome, Original Spec/Lines ou conjuntos Bug Label. Os SHA-256 dos 159 N.spec foram verificados fisicamente na R9 e **não recalculados na R10**.
- Comparação textual das regras complete/22/1–3 com FullMathWrapper.spec: **18, 17 e 13 linhas idênticas** respectivamente. Sem bloco methods no global.
- Leitura de ROUND9_P4_ABI_RESULT.json: contém ABI e methodIdentifiers, **nenhum bytecode**; sucesso Solidity da R9 não implica compilação CVL2.
- Auditoria read-only PR #41 na HEAD 3fcbf9d64af93ef9453abbbb7bee09a8c0dba0f5: 244 caminhos exclusivamente AGENTE-07; nenhuma alteração naquela branch.

## Preflight WSL R10

O dispositivo respondeu a pwd, Python 3.14.4 e Git 2.53.0. Entretanto, os comandos de leitura HEAD e status na worktree /home/mat/agente06-round9-20261020 retornaram **fatal: error reading .../.git**. Outras leituras simples passaram a devolver saída vazia. Isso não permite afirmar saúde da worktree nem obter exit confiável de todos os comandos. Não houve diagnóstico explícito de errno EIO, EROFS ou SIGBUS nesta rodada. Por segurança foram suspensas novas operações naquele computador; documentos publicados pela API GitHub.

## Resultado de testes atribuível ao AGENTE-06 nesta rodada

| Métrica | Resultado |
| --- | ---: |
| Exemplos documentados | **159** |
| CVL2 original compile-only executado | 0 |
| CVL2 derivado compile-only executado | 0 |
| COMPILE_OK CVL2 | 0 |
| COMPILE_ERROR CVL2 | 0 |
| NOT_RUN CVL2 | **159** |
| Equivalência semântica provada | 0 |
| Projetos integralmente migrados | 0/4 |
| Novas execuções Solidity R10 | 0 |

Os dois TypeErrors Solidity de PoolActionsWrapper são evidência da R9, não resultados CVL2 nem novas execuções R10. Os 33 eventos globais do painel PR #49 pertencem a outros experimentos e não foram atribuídos à carteira.

## Checks obrigatórios pós-commit

**NOT_RUN_INFRA_BLOCKED nesta rodada** para os quatro comandos locais: python3 scripts/check_specs.py ., python3 scripts/check_contests_csv.py ., python3 scripts/check_contracts.py . (dentro de Web3Bugs-certora) e git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD na raiz Git. Eles haviam passado na R9, não nesta HEAD. Inspeção GitHub e CI remoto são verificações distintas; não substituem execuções locais.

**Ação humana:** recuperar e verificar filesystem/worktree WSL; repetir os quatro checks; obter scene/ABI/bytecode original de P4 e runner auditado FullMath P22 antes de autorizar diagnóstico CVL2. PR segue Draft sem merge.

**AGENTE-06 — RODADA 10.**
