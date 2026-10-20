# AGENTE-03 — RODADA 8 / QA EXECUTADO vs NÃO EXECUTADO

**Contexto:** repositório `matheus-junio-da-silva/Web3Bugs`; branch existente `research/cvl2-agente-03` / PR #36 **Draft**; HEAD antes de mudanças `d1a00b23bf74ee7a7b4ed6683a43ee3878b383d0`; baseline histórico `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Escritas desta rodada limitadas à pasta `Web3Bugs-certora/docs/cvl2/research/AGENTE-03/` pelo conector GitHub. **Nenhum processo acessou o WSL.**

## QA documental realizado (GitHub somente)

- **Leituras efetivas:** `docs/spec_catalog.md` (blob `7211e9899e406c304c4828b5d02d221b5aa52b3f`), `docs/spec_catalog_workflow.md` (`aa6fd6413c3be6487d6508f0795a08655feb84d9`), `docs/spec_catalog_project_1.md` (`fd5ed8777cd4e582e236490993f81e3285d6fb61`), `docs/standard.md` (`df4eefcc202ca5d7c441623cee81d8fdd6ec0e9a`); P1 `complete/1/1.spec`, `incomplete/1/1.spec` e `incomplete/1/1.txt`. Completude de catálogo significa dependências no snapshot, não compilação CVL2.
- **Coordenação:** PR #47 foi **integrado documentalmente** por `6f640b76cfbde49a6d76bc708799e8c4d7fb3f30`; lidos `ROUND7_DASHBOARD.md` (blob `0f4a74fbb37d9c67f1958fb6172f2fda9643791f`) e `ROUND7_PROGRESS.csv` (blob `0dbf62c8b35d6c1c29f5be8317564877cbd78c87`) da integração; documento de incidente verdadeiro chama-se **`ROUND6_WSL_IO_INCIDENT.md`**, a consulta `WSL_IO_INCIDENT.md` sem prefixo retornou 404. Incidente EIO/SIGBUS/EROFS **permanece sem recuperação comprovada**.
- **Conservação do estado original:** `ROUND7_MATRIX_164.csv` blob `33bd2b171b6384b017917f81975f6ba5f6ca06dc`, `results/spec/spec_buglabel.csv` blob `97e20443586540034a4c0305ce1db19b0d2f8cb5`. Construída a matriz `ROUND8_MATRIX_164.csv` a partir do R7, comparando em memória as 164 chaves `(project_id,original_status,example_id)` com as 164 entradas P24 do CSV canônico, incluindo `Property`, `Target Contract`, `Result`, `Detection Outcome`, `Bug Label` e `Original Spec`. **Resultado antes do commit: 164/164 distintas, 0 divergências;** 44 colunas, SHA `N.spec` pré-aferido preservado, sem alegar novo recálculo dos 164 SHA256.
- **Cobertura individual:** LEHighLevel 10; LEInProgress 3; LEPreset 1; LEValidStates 35; LEVarTran 19; LaunchEvent 76; Staking 19; sanity 1 = **164**, todos `original_status=incomplete`. **Historicamente 164 Result=NOT_STATED e 161 Detection Outcome=NOT_STATED, 3 INCONCLUSIVE**; valores canônicos preservados.
- **Consulta documental externa:** fontes Certora CVL2 Migration/Changes, Methods/Ghosts/Hooks/Statements; fonte GitHub auditada/fork para LaunchEvent/Staking/harness/scripts/patch e lock files; `round5_oz_package_provenance.csv` (blob `7059c5b3645ed24ddff29a4c02dac35ae8ed7e17`) contém **4 SRI MATCH realizados na R5**, **não refeitos** agora; `round5_import_resolution.csv` e `round6_import_closure.csv` seguem análises estáticas prévias. Buscas GitHub nessa rodada de `Owner.sol` e `staking.spec` no fork fixado retornaram 404 (paths exatos documentados no EVIDENCE), sem substituir por outro arquivo.
- **Cross-review SOMENTE LEITURA:** PR #42 HEAD `462b5f9d7c1cf1d756aa960ec975998b39938dda`; conferidos `ROUND7_EVIDENCE.md`, `ROUND7_QA.md`, notas P12 e log P15/36: dois `COMPILE_ERROR` P12/23,25 em R5, um P15/36 em R6, nenhum novo teste R8 atribuído a AG03. **Nenhuma escrita na branch de AG04.**

## Execução CVL2 e QA de filesystem (obrigatoriamente separado)

| Verificação | Executado na R8? | Resultado |
| --- | --- | --- |
| `certoraRun --compilation_steps_only` P24 | **NÃO** | `164 NOT_RUN`, `0 COMPILE_OK`, `0 COMPILE_ERROR`, `0 PREFLIGHT_AUTH_BLOCKED` |
| `solc` / compilar ABI | **NÃO** | Nenhum exit associado à R8 |
| Aplicar `patch --fuzz=0` ou `make munged` | **NÃO** | Resultados anteriores R4/R6 NÃO reexecutados |
| `python3 scripts/check_specs.py .` na raiz `Web3Bugs-certora` | **NÃO** | `NOT_RUN_INFRA_BLOCKED` |
| `python3 scripts/check_contests_csv.py .` idem | **NÃO** | `NOT_RUN_INFRA_BLOCKED` |
| `python3 scripts/check_contracts.py .` idem | **NÃO** | `NOT_RUN_INFRA_BLOCKED` |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` da raiz Git | **NÃO** | `NOT_RUN_INFRA_BLOCKED` |
| Prover completo / CVL1 / Fase 2 / merge | **NÃO** | Proibidos/não autorizados |
| Credenciais Certora / CERTORAKEY | **NÃO lidas, não usadas** | `NOT_ATTEMPTED` |

**Após commit e publicação:** a checagem dos novos arquivos, PATHS do diff inteiro contra baseline e da HEAD final deve ser feita pela API GitHub e registrada no comentário do PR #36. Caso o workflow GitHub `validate` esteja SUCCESS, registrar **separadamente** sua execução e quais steps existem: ele não comprova os comandos exatos acima, não substitui a checagem local e não comprova CVL2.

## Intervenção humana exigida

Não rodar sequer preflight no WSL instável: recuperação deverá ser comprovada pelo administrador **antes** de permitir comandos no filesystem remoto. Primeiro conferir saúde/backup/espaço, leitura e escrita em diretório temporário, Python/Git/binários, worktrees/HEAD/hashes; só depois executar os três validadores Python e `diff --check BASE...HEAD` na HEAD do PR, coletando stdout/stderr, exit, cwd e logs. Somente sob gate **individual** do coordenador proceder a scratch `P24/incomplete/164` fork-only. Sem novo `results/cvl2/` e sem afirmar replay histórico.

**Alerta: `LARANJA` documental/semântico e `VERMELHO` infraestrutura. AGENTE-03 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS.**
