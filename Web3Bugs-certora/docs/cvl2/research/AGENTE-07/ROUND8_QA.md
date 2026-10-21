# AGENTE-07 — Rodada 8 / QA, reconciliação e bloqueio de execução

**PR existente:** [#41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41), branch `research/cvl2-agente-07`, DRAFT. **Partida verificada:** `b2a7dfa04c65a995c30649d7e1acd03f6c06934c`. **Baseline histórico imutável:** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Nenhuma alteração em contratos, specs originais, sources, labels, reports ou CSV original. Nenhum PR/branch externo atualizado.

## O que realmente foi executado — GitHub connector, memória

1. Reabertos os quatro documentos metodológicos `docs/spec_catalog.md`, `docs/spec_catalog_workflow.md`, `docs/spec_catalog_project_1.md`, `docs/standard.md` na `main`, além dos recortes de referência `results/spec/complete/1/1.spec`, `incomplete/1/1.spec`; painel integrado `docs/cvl2/coordination/ROUND7_DASHBOARD.md`, `ROUND7_PROGRESS.csv` e incidente `ROUND6_WSL_IO_INCIDENT.md`.
2. **Fonte do catálogo:** `results/spec/spec_buglabel.csv` do baseline, blob Git `97e20443586540034a4c0305ce1db19b0d2f8cb5`, **1.390 registros** de Bug Labels referentes a **1.386 chaves individuais**. Reconciliadas por parser CSV (suporta aspas e vírgulas) todas as 156 chaves `(Project ID,Status,Example ID)` contra a fonte canônica: **zero divergências** em `Property`, `Target Contract`, `Result`, `Detection Outcome`, `Original Spec` e `Original Spec Lines`. Os labels foram agregados das linhas canônicas por chave; não houve propriedade com múltiplos labels **neste conjunto de 156**, embora existam quatro relações excedentes no conjunto global.
3. **Matriz `ROUND8_MATRIX_156.csv`:** leitura independente de volta pelo conector após commit, **156 linhas, 156 chaves distintas**, **38 colunas**, todas com status de compilação CVL2 `NOT_RUN`. Contagens: P9 `50 complete + 11 incomplete = 61`; P8 `42 incomplete`; P20 `37 incomplete`; P11 `16 incomplete`. Result históricos preservados: **32 VERIFIED**, **5 VIOLATED**, **119 NOT_STATED** (não reinterpretados). Grupos de risco por fórmula P8: **22 W1, 1 W2/W3 e 19 outros**. Mapa P20 totaliza 8 + 8 + 6 + 1 + 8 + 6 = **37**.
4. **Hash `N.spec`:** são 156 SHA-256 carregados das matrizes R5–R7 auditadas anteriormente, não recálculo novo dos bytes `N.spec` na R8. Os Git blobs identificados por conector para as fontes **não equivalem** a SHA-256 de artefatos compilados. `source_or_report_fact`, `inference` e `missing_proof` são colunas distintas, e `cvl2_executor`, `cvl2_command`, `cvl2_exit_code`, `cvl2_stdout_stderr` impedem confundir dados históricos com diagnóstico de parser.
5. **Cross-review READ-ONLY PR #43:** HEAD observado `fe0c25ae89835616a8b36f86cb067c4ab6a5fcf1`, branch `research/cvl2-agente-08`. `Certora/drips-contracts@8d1db123de7fb4e1c3536bdddfd10a085aa36095` — conferidos diretamente via GitHub os blobs de `SplitsHarness.sol`, `runSplits.sh`, `runSplits2.sh`, `splitsjob.conf`, `Splits.spec` e `Splits2.spec`. Scripts com `--send_only` e harness com overrides vazios não são prova de execução original, CVT ou equivalência. Nenhuma operação de escrita/patch no PR43.

## O que NÃO foi executado por risco de infraestrutura

O dispositivo WSL `DESKTOP-5E26TVU` segue **sem recuperação explicitamente atestada**. O incidente registrado pelo coordenador envolve `spawn EIO`, `SIGBUS`, `EROFS` e falhas de leitura/escrita. **Não fiz chamada ao Remote Desktop Commander nem executei comandos shell nesse WSL nesta R8**.

| Comando/ação local obrigatório | Execução na R8 | Código de saída |
|---|---|---|
| `cd Web3Bugs-certora && python3 scripts/check_specs.py .` | `NOT_RUN_INFRA_BLOCKED` | inexistente |
| `cd Web3Bugs-certora && python3 scripts/check_contests_csv.py .` | `NOT_RUN_INFRA_BLOCKED` | inexistente |
| `cd Web3Bugs-certora && python3 scripts/check_contracts.py .` | `NOT_RUN_INFRA_BLOCKED` | inexistente |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | `NOT_RUN_INFRA_BLOCKED` | inexistente |
| `certoraRun --compilation_steps_only`, `solc`, qualquer CLI/Prover, CVL1, patches e scripts de build | **NÃO EXECUTADOS** | inexistente |

`INFRA_EIO` em coluna própria da matriz indica bloqueio para **novo teste**, não `COMPILE_ERROR`, `PREFLIGHT_AUTH_BLOCKED`, nem resultado de `--version`. A leitura de ABI `solc` feita em R5 permanece resultado **histórico de Solidity**, não reexecução nem `COMPILE_OK` CVL2.

## Evidência de GitHub Actions versus execução local

O workflow `validate` do commit intermediário da R8 `7583e3447a65746cf1efdf6a1dfb931c1849968d` retornou **SUCCESS**, execução [#39498096337](https://github.com/matheus-junio-da-silva/Web3Bugs/actions/runs/39498096337). Uma **nova** execução de CI poderá ser criada no commit final contendo este arquivo; sua conclusão será reportada separadamente na resposta ao PR, após verificação da HEAD. O workflow verifica integridade estrutural, não parser, consistência do modelo ou equivalência de contraexemplos. Ele **não substitui** os quatro comandos locais acima. A checagem de whitespace baseada em leitura dos três documentos deve ser registrada como verificação textual remota, **não** `git diff --check BASE...HEAD` executado.

## Status e intervenção humana

- **AGENTE-07, Rodada 8:** 156 propriedades documentadas, **0 compile-only executados**, **0 COMPILE_OK**, **0 COMPILE_ERROR**, **0 PREFLIGHT_AUTH_BLOCKED**, **156 NOT_RUN**, **0 SEMANTIC_PROVEN**, **0 MIGRATED_COMPLETE**.
- **Universo global** no painel R7: 4 `COMPILE_OK` limitados, 12 `COMPILE_ERROR` reais e 1.370 sem teste, todos **fora da carteira AGENTE-07**. Nenhum novo resultado contabilizado.
- **Riscos vermelhos:** P8 W1/W2/W3 se assumidos num modelo; P20 remoção de catches no patch/semântica de revert e `MAX_INT` ausente na spec Additional; WSL não íntegro. ABI Celo sem gitlink autenticado e runner Keep ausente continuam laranja.
- **Gate 1:** coordenador autorizar estudo **derivado** do alcance/satisfatibilidade dos axiomas P8, sem alterar originais e sem interpretar `VERIFIED` do relatório até restituir job/flags.
- **Gate 2:** recuperar gitlink e pacote Mento exato da fase auditada de Celo, preparar cenário `AccountsHarness` e **apenas após recuperar WSL** fixar hashes/solc/ABI e discutir `--compilation_steps_only` restrito; sem stubs.
- Após recuperação humana: atestar backups/saúde do WSL, criar scratch novo **somente depois de aprovação**, verificar HEAD/worktree limpos, executar três scripts e diff CLI; coletar logs e exit sem inferir equivalência.

**AGENTE-07 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS**
