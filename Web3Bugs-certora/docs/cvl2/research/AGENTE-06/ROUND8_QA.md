# AGENTE-06 — ROUND8_QA / resultados executados, não executados e infra bloqueada

Data 2026-10-20. PR [#38](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/38), branch `research/cvl2-agente-06`, Draft. HEAD da rodada anterior `e4527033b3c2b1a6aa638f6b7c351ee996d0ae79` foi conferida no GitHub antes de qualquer commit; baseline histórico imutável `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.

## QA efetivamente realizado (GitHub connector, dados em memória; sem WSL)

1. Foram obtidos por GitHub os bytes textuais integrais do `results/spec/spec_buglabel.csv` canônico da baseline (**1.390 relações, 1.386 chaves distintas**) e de `ROUND7_MATRIX_159.csv`. Para cada chave da R7, reconciliou-se a linha original e criou-se `ROUND8_MATRIX_159.csv`; **159 chaves canônicas distintas e existentes**, P1 70, P4 27, P17 41, P22 21. **Zero diferenças** em `Property`, `Target Contract`, `Result`, `Detection Outcome`, `Original Spec`, `Original Spec Lines` e `Bug Label(s)`, inclusive três properties com múltiplos labels (P1 complete/1, P1 complete/26, P4 incomplete/4). Nenhuma fonte original foi gravada.
2. Os 159 strings de SHA-256 de `N.spec` foram **herdados** das matrizes anteriores atestadas, não recalculados nesta R8, e `R8` documenta essa distinção em `sha256_method_R8`. Hash de Git blob SHA-1 citado em pesquisa não é SHA-256 do `N.spec`.
3. `ROUND8_MATRIX_159.csv` define, para cada ID, colunas distintas `source_or_report_fact`, `inference`, `missing_proof`, cenário, links por fonte, target/ABI ou sua ausência, contexto full-spec vs fragmento, comando, código/autor/log e próximo gate. **159 status `NOT_RUN`, zero `COMPILE_OK`, zero `COMPILE_ERROR`**; `preflight_env_status=INFRA_BLOCKED_WSL_EIO_SIGBUS_EROFS_NOT_CVL2_ERROR` é indicador de ambiente, não erro de parser para nenhuma das 159.
4. Pelo GitHub, a comparação do PR em andamento verificou somente arquivos sob `Web3Bugs-certora/docs/cvl2/research/AGENTE-06/`, nenhum fora da pasta. O total de caminhos deve ser reconfirmado **após** o último commit desta rodada, em vez de atribuir a este documento contagem intermediária.
5. Auditoria cruzada read-only PR #41: HEAD observada `7583e3447a65746cf1efdf6a1dfb931c1849968d`, 238 caminhos exclusivamente AGENTE-07; relidas as fórmulas exemplares W1 em P8/incomplete/14 e W2/W3 em P8/incomplete/1, bem como novas hipóteses em `AGENTE-07/ROUND8_EVIDENCE.md`; nenhum Prover, teste derivado ou alteração de branch alheia.

**Normativa:** guias [CVL2 Migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [CVL2 Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [Methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [Hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html), [Statements/reverts](https://docs.certora.com/en/latest/docs/cvl/statements.html); essas definições modernas não são replay do Specify 2019.

## Comandos obrigatórios LOCAIS: não executados nesta rodada

A coordenação reportou WSL `DESKTOP-5E26TVU` com `spawn EIO`, `SIGBUS`, `EROFS`, falhas em comandos triviais, sem recuperação humana certificada. Vide [ROUND6_WSL_IO_INCIDENT.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/6f640b76cfbde49a6d76bc708799e8c4d7fb3f30/Web3Bugs-certora/docs/cvl2/coordination/ROUND6_WSL_IO_INCIDENT.md). Por segurança **nenhum comando, compilação, patch, worktree, escrita ou leitura de credenciais foi tentado nesse WSL na R8**.

| Comando exato requerido | R8: status | Exit/stdout/stderr |
| --- | --- | --- |
| `cd Web3Bugs-certora && python3 scripts/check_specs.py .` | `NOT_RUN_INFRA_BLOCKED` | **Não existe novo exit/log local** |
| `cd Web3Bugs-certora && python3 scripts/check_contests_csv.py .` | `NOT_RUN_INFRA_BLOCKED` | **Não existe novo exit/log local** |
| `cd Web3Bugs-certora && python3 scripts/check_contracts.py .` | `NOT_RUN_INFRA_BLOCKED` | **Não existe novo exit/log local** |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | `NOT_RUN_INFRA_BLOCKED` | **Não existe novo exit/log local** |

Qualquer CI GitHub `validate: SUCCESS`, quando concluído sobre a HEAD final, prova somente execução das **etapas realmente presentes no workflow**, não os comandos acima como executados localmente nem semântica de CVL2. O `check_specs.py` pode não ser uma etapa independente do workflow `validate`; conferir a lista de steps sem inventá-la.

## Estado real CVL2 por propriedade

| Tipo | Valor R8 | Interpretação |
| --- | ---: | --- |
| Casos documentados em matriz | **159/159** | Indexação e pesquisa, **não** migração |
| `certoraRun --compilation_steps_only` executado na R8 | **0** | Nenhum stdout/stderr CVL2 criado |
| `COMPILE_OK` | **0** | Nenhum sucesso parser/typecheck/compilação observado |
| `COMPILE_ERROR` | **0** | Nenhum erro real CVL2 observado |
| `NOT_RUN` | **159** | Não houve teste válido por property |
| `PREFLIGHT_AUTH_BLOCKED` | **0 observado** | Não confundir preflight com não execução |
| `SEMANTIC_PROVEN` | **0** | Nenhuma equivalência de domínio, revert ou contraexemplos demonstrada |
| Projetos `MIGRATED_COMPLETE` | **0/4** | P1, P4, P17, P22 ainda unresolved |

**Não repetir como execução R8:** R5 aplicou patch P4 em scratch; R6 tentou solc-js 0.8.17 e terminou em SIGBUS sem ABI (não erro CVL2). O painel R7 global (8 agentes, 23 projetos) informa **4 compilações CVL2 exit 0 limitadas, 12 parser/typechecker exit 1 e 1.370 sem teste**, mas **nenhuma** dessas 16 execuções pertence à carteira do AGENTE-06.

## Gate de intervenção humana

**Antes de qualquer compilação:** administrador validar volume/backup/saúde WSL e worktrees; conferir SHA remoto/local sem reset, verificabilidade de read/write apenas em scratch novo, `python`, `git`, `solc`/CLI e input hashes; reexecutar **quatro** comandos locais exatos com logs e exit. Se autorizados por coordenador: (A) P4 ABI Solidity do `munged` com src e munged interfaces e solc8.17, só scratch; (B) P1 Polygon complete/1–3 após bundle de junho auditado (primeiro fonte/ABI/runner, depois Certora `--compilation_steps_only` por propriedade). Esses são **experimentos propostos, NÃO executados**. Nenhum Prover formal, CVL1, implementação derivada ou merge autorizado.

**Resultado QA local:** `NOT_RUN_INFRA_BLOCKED`; **resultado de inspeção por API:** cobertura e identidade históricas preservadas. PR segue Draft.

**AGENTE-06 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS.**
