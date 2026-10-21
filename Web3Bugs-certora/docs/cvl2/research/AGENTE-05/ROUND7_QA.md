# AGENTE-05 — ROUND7_QA: status real, integridade e bloqueio WSL

**Data:** 20/10/2026. **PR:** [#40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40) Draft, branch `research/cvl2-agente-05`, sem merge. **HEAD inicial confirmada:** `31ce9c427e5aed759c1b04932ed9ebdd76cbe959`. **Original imutável:** `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Somente arquivos em `docs/cvl2/research/AGENTE-05/` acrescentados.

## QA da matriz R7 — realmente executado através de consultas GitHub / computação em memória

[`ROUND7_MATRIX_148.csv`](ROUND7_MATRIX_148.csv) foi construída por parsing independente de:
- `results/spec/spec_buglabel.csv` canônico **no baseline**;
- `ROUND6_MATRIX_148.csv` da HEAD inicial, sem apagar nenhum status de compilação;
- cinco `{3,6,7,19,21}/properties.csv` desta mesma pesquisa;
- `7/round5_logs/ROUND5_COMMAND_MANIFEST.json` publicado anteriormente, para os cinco `COMPILE_ERROR`.

**Regras efetivamente checadas:** exatamente **148 chaves únicas** `(project_id,original_status,example_id)`; cinco índices de pesquisa também com exatamente 148; **149 relações históricas com Bug Labels** dessas 148 instâncias, incluindo duplicação legítima de uma chave. Comparadas 148/148 vezes `Property`, `Target Contract`, `Result`, `Detection Outcome` entre CSV canônico, índice do projeto e matriz anterior, sem divergência. Conferidos 148/148 hashes de `N.spec` **contra os `extracted_spec_sha256` dos cinco índices** (estes hashes já haviam sido verificados contra bytes originais no dossiê das rodadas anteriores; **não** afirmar rehash direto de 148 arquivos em R7). Cada um dos cinco `COMPILE_ERROR` foi vinculado ao manifesto anterior com target e **exit code 1**; para as duas P7/37,65 e duas derivadas P19/1,2 preservou-se **exit 0 anterior** com provenance, sem fabricar comando exato não registrado na matriz. Nenhuma coluna histórica canônica foi alterada.

### Contabilidade por propriedade

| Projeto | Total | `COMPILE_OK` restrito anterior | `COMPILE_ERROR` anterior | `NOT_RUN` CVL2 | Execuções R7 |
| --- | ---: | ---: | ---: | ---: | ---: |
| P7 AAVE V3 | 74 | 2 (complete/37,65; **somente N.spec**) | 5 (complete/36,41,47,63,73) | 67 | 0 |
| P19 OUSD | 37 | 2 (complete/1,2; **somente derivadas mathint**) | 0 | 35 | 0 |
| P6 Static aToken | 32 | 0 | 0 | 32 | 0 |
| P3 Rescue | 3 | 0 | 0 | 3 | 0 |
| P21 Lido DSM | 2 | 0 | 0 | 2 | 0 |
| **Total AGENTE-05** | **148** | **4** | **5** | **139** | **0** |

**Causas e classificação:** `PREFLIGHT_AUTH_BLOCKED` = **0** observado nesta carteira. Na R7, todos os casos permaneceram `NOT_RUN` por proibição de operar o WSL durante `INFRA_EIO/SIGBUS/EROFS`, **não** devido a erro CVL2. A variante `sig:` de P7/47 **não foi executada**, não acrescenta `COMPILE_OK` nem `COMPILE_ERROR`. A compilação Solidity `solc`/ABI anterior de P7 não deve somar a esses números. `SEMANTIC_PROVEN=0`; `MIGRATED_COMPLETE=0`. `DOCUMENTED_CANDIDATE` e `UNCHANGED_CANDIDATE` continuam hipóteses, não gates finais.

**Comparação com o painel oficial [ROUND6_DASHBOARD](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/948121599b546d61579dc9ecb8c316f9c088e78a/Web3Bugs-certora/docs/cvl2/coordination/ROUND6_DASHBOARD.md):** **23 projetos, 1.386 exemplos / 1.390 relações, 4 COMPILE_OK limitados, 12 COMPILE_ERROR, 1.370 sem teste**, 0 equivalências e 0 projetos completos. Esses números são **globais**, e os outros 7 erros de parser não pertencem ao AGENTE-05. O painel `ROUND6_COMPILATION_OBSERVATIONS.csv` registra 16 propriedades com evidência; 4 OK+12 ERROR. A infra está marcada `INFRA_BLOCKED` no `ROUND6_WSL_IO_INCIDENT.md` e o coordenador confirmou `spawn EIO`.

## Pré-condições de segurança da execução

**Nenhum comando foi enviado nesta R7 ao host WSL `DESKTOP-5E26TVU`**, mesmo os de leitura, pois a recuperação não foi atestada. Nenhum `certoraRun`, Prover, CVL1, `--compilation_steps_only`, `solc`, patch, setup/instalação, teste de filesystem ou script de migração foi executado nesta rodada. Nenhuma variável `CERTORAKEY`, token ou `.env` foi acessada.

**Scripts obrigatórios solicitados, explicitamente NÃO EXECUTADOS na HEAD R7:**

| Comando na árvore correta | Resultado real |
| --- | --- |
| `cd Web3Bugs-certora && python3 scripts/check_specs.py .` | **NOT_RUN_INFRA_BLOCKED** |
| `cd Web3Bugs-certora && python3 scripts/check_contests_csv.py .` | **NOT_RUN_INFRA_BLOCKED** |
| `cd Web3Bugs-certora && python3 scripts/check_contracts.py .` | **NOT_RUN_INFRA_BLOCKED** |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` (raiz Git) | **NOT_RUN_INFRA_BLOCKED** |

A reconciliação de CSVs e a checagem de nomes, escopo e whitespace pelo conector GitHub são verificações alternativas **não equivalentes** ao comando literal `git diff --check`. O workflow `validate`, caso fique verde, não executa `check_specs.py` nem o `git diff --check BASE...HEAD` exigido; não atribuir aos comandos não executados o EXIT 0 do CI.

## QA estrutural remota adicional (sem shell, se disponível)

A comparação da branch contra o baseline pode ser feita por `compare_commits` da API GitHub, verificando que **todos** os paths modificados começam com `Web3Bugs-certora/docs/cvl2/research/AGENTE-05/`, sem alteração em originais; a leitura das três publicações R7 permite checar whitespace textual (trailing spaces/tabs, blank EOF). Esses resultados serão reportados no comentário de entrega **após o último commit**, e **não** como execução do diff exato no WSL.

## Controle de retomada a cargo de administrador/coordenador

O incidente `ROUND6_WSL_IO_INCIDENT.md` determina que o administrador verifique backup e saúde do volume Windows/WSL. Somente após confirmação explícita de recuperação, em diretório temporário **novo** testar leitura/escrita, Python, Git e worktree limpa/HEAD, conferir hashes, executar os três validadores e diff exato sobre a mesma HEAD versionada. Registrar comandos, stdout/stderr, exit codes e SHA da HEAD. Nada de reset/rebase/patch/solc ou CLI antes do gate. Para P7/47, a variante lexical de exatamente seis `sig:` requer aprovação **individual** adicional da coordenação e cópias byte-idênticas em scratch, sem derived PR ou mudança de premissas.

**Alerta: 🟠 semântico não demonstrado / 🔴 infraestrutura WSL bloqueada para testes e QA local.** Não há novos logs/manifestos de R7, porque não houve execuções. **AGENTE-05 — RODADA 7.**
