# AGENTE-05 — Rodada 6: contabilidade de execução, QA e gates

**Data:** 2026-10-20. PR [#40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40) continua Draft, branch `research/cvl2-agente-05`. HEAD inicial confirmado `f9a9c7d8167a532b9f2b534bc38e1e9f57c035d7`. Baseline histórico imutável `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Conteúdo versionado desta rodada **somente** sob `Web3Bugs-certora/docs/cvl2/research/AGENTE-05/`.

## Inventário factual, sem inflar resultados

| Universo | COMPILE_OK limitado anterior | COMPILE_ERROR CVL2 anterior | NOT_RUN CVL2 | SEMANTIC_PROVEN |
| --- | ---: | ---: | ---: | ---: |
| AGENTE-05 P3/6/7/19/21: **148** | **4** (P7/37,65 originais extraídos, P19/1,2 derivadas `mathint`) | **5** (P7/36,41,47,63,73) | **139** | **0** |
| Painel de coordenação R5: **1.386** / 23 projetos | **4** | **11** | **1.371** | **0** |

`PREFLIGHT_AUTH_BLOCKED` observado para AGENTE-05 nesta rodada: **0**. `MIGRATED_COMPLETE` projetos: **0**. O `COMPILE_OK` de P7 fragmentado não inclui `methods/ghost/hooks` globais; P19 derivado não resolve `RCPT=0`. `COMPILE_ERROR` é typechecker CVL2 anterior e não diagnóstico de vulnerabilidade. Estes números são **de evidências anteriores, não de compilações novas R6**.

[ROUND6_MATRIX_148.csv](ROUND6_MATRIX_148.csv) reconcilia 148 chaves únicas `(project_id, original_status, example_id)`, nomes, target, Result/Detection Outcome histórico (intactos), fonte CVL, SHA256 N.spec, referência auditada de cada projeto, cena, comando/exit efetivo quando houve compilação, preflight, risco de vacuidade, blockers e próximo gate. Reconciliado programaticamente via integração GitHub com os cinco `properties.csv` existentes: **148/148 keys e SHA256 iguais**; cinco logs de COMPILE_ERROR correspondem a `7/round5_logs/ROUND5_COMMAND_MANIFEST.json` (EXIT 1).

## NOVA execução de scratch na R6: o que aconteceu e o que NÃO aconteceu

1. Ambiente WSL original: `certora-cli 8.19.0` confirmado ao invocar o executável direto `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun --version` (sem wrapper local que força `CERTORAKEY`). `solc 0.8.10` e HEAD da branch também conferidos. Docs obrigatórios (`spec_catalog`, `spec_catalog_workflow`, `spec_catalog_project_1`, `standard`) foram lidos integralmente, e complete/1/incomplete/1 comparados; o primeiro traz closures presentes e o segundo mantém helper `queue2` faltante.
2. Preparação de variante **somente P7/complete/47**: intenção de acrescentar os **seis prefixos `sig:`** na definição `disAllowedFunctions`. Primeira tentativa de script não passou uma asserção preparatória porque o nome da rule aparecia também no comentário de cabeçalho. A condição foi corrigida **somente no script de scratch**.
3. O host remoto começou a retornar **`SIGBUS`/exit 135** ao importar bibliotecas Python padrão, `df: Input/output error`, e `EROFS: read-only file system` ao tentar criar relatório. A falha não foi demonstrada como relacionada a CVL2 nem a autenticação. **A CLI de compilação da variante não foi chamada**, nenhum código de saída do typechecker foi obtido e **não há spec derivado gerado ou publicado**. Status **`NOT_RUN_ENVIRONMENT_IO_BLOCKED`** para a variante P7/47. Não atribuir a `COMPILE_ERROR` nem `PREFLIGHT_AUTH_BLOCKED`.
4. Para preservar a integridade do repositório, após `EROFS` foram interrompidas as escritas no host afetado. Os documentos foram publicados por commits da integração GitHub na própria branch autorizada, **sem reset ou force-push**. Não foi usado CLI CVL1, Prover formal, `--cloud`, migration script em lote ou credencial.

## Distinção estrita de QA realizado e QA bloqueado

**EXECUTADO nesta rodada:**
- Leitura e conferência da HEAD inicial, das revisões recentes do PR #40, do painel `ROUND5_DASHBOARD.md` de #47 e da documentação Certora atual para `sig:`, methods, ghosts, hooks, e `@withrevert`.
- Verificação da matriz via parsing de CSV em JavaScript, cotejando as cinco tabelas de pesquisa P3/P6/P7/P19/P21 e o manifesto de execução anterior. **148 registros / 148 SHA256 reconciliados**.
- Comparação GitHub `BASE...commit` para identificar caminhos modificados, com **zero caminhos fora** de `docs/cvl2/research/AGENTE-05/`. Checagem textual independente dos três novos arquivos R6 encontrou **zero** finais com espaços/tab, zero blank EOF e zero `space-before-tab`. Isto **não substitui** o comando `git diff --check`.
- Contrarrevisão somente leitura da HEAD `ad460c288729d881a8adfac212695415809fc07d` do PR #38: fonte `queue2/_mock` posterior (setembro/2022) vs auditoria junho/2022; Specify P17/8,9,39 com `havoc`, `sinvoke`, `invoke`, `static_require/assert`, reverts. Sem editar o PR #38.

**NÃO EXECUTADO na HEAD remota R6 por `EROFS/SIGBUS`:**
- `python3 scripts/check_specs.py .` em `Web3Bugs-certora/`: **NOT_RUN_ENVIRONMENT_IO_BLOCKED**.
- `python3 scripts/check_contests_csv.py .`: **NOT_RUN_ENVIRONMENT_IO_BLOCKED**.
- `python3 scripts/check_contracts.py .`: **NOT_RUN_ENVIRONMENT_IO_BLOCKED**.
- `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD`: **NOT_RUN_ON_COMMITTED_HEAD** (foi usada comparação via GitHub, não o comando literal).

**Controle alternativo sem falsa equivalência:** o ZIP `Web3Bugs.zip` anexo possui snapshot `main@4a1bea89d88aa3b6aa165e8d81b8dd523c7afb82` com **164** exemplos/169 relações, **não** a HEAD de pesquisa atual de 1.386 propriedades. Os três validadores executados sobre essa cópia independente deram EXIT 0, mas são **excluídos dos checks da HEAD R6** e não autorizam declarar QA pós-commit do PR aprovado. A própria diferença quantitativa foi observada e registrada.

**Para satisfazer o gate de QA pós-commit:** ao restabelecer checkout gravável e runtime Python íntegro, coordenador/AGENTE-05 deverá buscar a HEAD publicada sem reset, executar os três scripts na raiz `Web3Bugs-certora/`, o `git -c core.whitespace=cr-at-eol diff --check BASE...HEAD` na raiz Git, arquivar exit e logs, e vincular o workflow `validate` da mesma HEAD. Até isso, a auditoria desta rodada não deve ser chamada de verde.

## Documentos e decisão

- [P7/47,73,41,63,36 — ABI, dispatch, `@withrevert`, EIP-712, hook, diff `sig:` SOMENTE em docs](7/ROUND6_SELECTOR_SEMANTICS_AND_SCRATCH_GATE.md).
- [P3/P6/P19/P21 — proveniência e PR #38 somente leitura](ROUND6_HISTORICAL_BLOCKERS_AND_PR38_READONLY.md).
- [Matriz de 148 exemplos, status real](ROUND6_MATRIX_148.csv).

**Próximos gates individuais:** P7/47 teste compile-only temporário `sig:` após recuperação ambiental e autorização, depois P7/73 separadamente; P7/41/63/36 preservar globals e método paramétrico; P19 árvore pós-script sem modificar original; P3 runner/autoria por target sobre submodule autenticado; P6 PDF/SHAs completos; P21 harness/getter e invariante confrontada; PR #38 cena auditoria junho/2022 para `queue2` e engine Specify 2019.

**ALERTA: LARANJA — pesquisa documental e integridade de matriz preservadas, QA executável no host bloqueado.** Não houve merge, Prover, equivalência nem `MIGRATED_COMPLETE`. **AGENTE-05 — RODADA 6.**
