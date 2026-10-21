# AGENTE-02 — RODADA 7 / QA e portões de execução

**Data:** 2026-10-20. PR [#37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37), branch `research/cvl2-agente-02`, base catalogada `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`, HEAD de partida R6 `2477787fe3f4cddb650cb4f1a08760bdbd1fde13`. Não houve alterações nos originais ou em branches de outros agentes.

## 1. Validação que foi REALMENTE executada via conector GitHub

Após publicar `ROUND7_N_SPEC_SHA1_MANIFEST.csv`, `ROUND7_MATRIX_181.csv` e `ROUND7_EVIDENCE.md`, um reconciliador em memória **efetivamente executado** leu cada arquivo remoto e o CSV canônico `results/spec/spec_buglabel.csv` nas refs do PR e do baseline. A comparação por Git blob do CSV canônico em ambas as refs deu `97e20443586540034a4c0305ce1db19b0d2f8cb5`, **identidade dos bytes**.

| Controle por dados via GitHub | Resultado observado |
| --- | ---: |
| Matriz R7, `project_id,original_status,example_id` únicos | **181/181**, sem duplicatas |
| Chaves canônicas P18 distintas | **181** |
| `N.spec` hashes de blob Git (40 caracteres hex), ref fixa `2477787fe3f4cddb650cb4f1a08760bdbd1fde13` | **181/181** |
| Pareamento matriz↔manifest SHA por chave | **181/181** |
| Pareamento canônico Property, Target Contract, Result, Detection Outcome e Spec path | **181/181**, 0 divergências |
| Complete/incomplete | **69/112** |
| Candidatos DOCUMENTED_CANDIDATE apenas lexicais | **50** |
| Upstream specs ausentes/diferentes na auditoria por instância | **157/24** |
| Compilações CVL2 P18 anteriores observadas | **0 COMPILE_OK, 2 COMPILE_ERROR (coordenador), 179 NOT_RUN** |
| Execuções CVL2 R7 locais | **0** |
| SEMANTIC_UNRESOLVED | **181** |
| Trailing whitespace nos 3 artefatos R7 conferidos | **0** |

**Blobs Git verificados no fim da reconciliação:** matriz `4db04cf895943de3005c3c2027b11ca2580fa677`, manifesto `5eca00c12ee5eb20062668d309a0a525484a7dbf`, relatório de evidências `9038d4b8d3e309d00a5326d73cee1125f3b6c83b`. SHA-1 de objeto Git não é SHA-256 do N.spec; os N.spec com SHA-256 previamente obtido conservam esse campo separado na matriz. Não inferir SHA-256 onde não foi calculado. O manifesto foi elaborado por leitura individual via GitHub dos 181 arquivos imutáveis no commit fixo; não por hashes de specs globais.

## 2. Bloqueio de infraestrutura: comandos históricos EXIGIDOS mas NÃO EXECUTADOS na R7

O coordenador registrou `spawn EIO`, `EROFS` e `SIGBUS` em [ROUND6_WSL_IO_INCIDENT.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/948121599b546d61579dc9ecb8c316f9c088e78a/Web3Bugs-certora/docs/cvl2/coordination/ROUND6_WSL_IO_INCIDENT.md). **Por instrução de segurança do processo, não foi iniciada sequer uma chamada de health-check nem criado worktree/scratch novo naquele WSL na R7.** Consequentemente:

| Comando local após commit | Resultado real R7 |
| --- | --- |
| `cd Web3Bugs-certora && python3 scripts/check_specs.py .` | **NOT_RUN_INFRA_BLOCKED** |
| `cd Web3Bugs-certora && python3 scripts/check_contests_csv.py .` | **NOT_RUN_INFRA_BLOCKED** |
| `cd Web3Bugs-certora && python3 scripts/check_contracts.py .` | **NOT_RUN_INFRA_BLOCKED** |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | **NOT_RUN_INFRA_BLOCKED** |
| `certoraRun --compilation_steps_only` P18/4,46,53 com CLI direto | **NOT_RUN_INFRA_BLOCKED**, nenhum stdout/stderr/log de parser gerado |

As verificações em memória acima **não substituem** os três validadores ou o check do diff commitado. Sucessos da CI ou dos scripts em R5/R6 não serão atribuídos como comandos executados em R7. Não há novos `COMPILE_OK` ou `COMPILE_ERROR`. P18/3 e P18/23 permanecem os **dois erros de parser antigos, executor COORDENADOR**, e os nove preflights por `CERTORAKEY` da R5 permanecem erros ambientais segregados.

## 3. Aceitação documental e QA remoto complementar

Verificar no GitHub após a HEAD final a comparação `2a03637b...HEAD` e aceitar **somente** arquivos sob `Web3Bugs-certora/docs/cvl2/research/AGENTE-02/`; confirmar o PR **Draft**, e o status do workflow `validate`. O workflow histórico `validate` executa `check_contests_csv`, `check_contracts` e `check_git`, mas não equivale ao pedido dos quatro comandos acima nem valida semântica CVL. Se o workflow ainda estiver pendente, informar estado real sem inventar sucesso.

## 4. Dependência de intervenção humana e retomada controlada

O administrador deve restabelecer FS/WSL preservando worktrees e confirmar leitura+escrita em diretório descartável, disponibilidade de Python/git, status limpo, versões `certora-cli 8.19.0` e solc `0.8.6`, hashes dos inputs, sem tocar secrets. Apenas depois executar os três validadores e `git diff --check BASE...HEAD`, registrar stdout/stderr/exit codes. Retomar um N.spec original por vez (**/4, /46, /53**), uma cena/target, CLI direto (sem wrapper de autenticação), `--compilation_steps_only`, timeout 60s, hashes de todas as fontes e logs. A spec global exige diagnóstico separado; não modificar `require`, `assert`, casts, summaries, handlers, ghosts, hooks ou ABI Solidity. Ainda será necessário gate histórico independente para comprovar equivalência de contraexemplos.

**Não há evidência de equivalência CVL1→CVL2 nem projeto integralmente migrado. PR DRAFT sem merge.**

**AGENTE-02 — RODADA 7.**
