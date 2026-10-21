# AGENTE-03 — RODADA 7 / QA, integridade e execução

**Status de infraestrutura:** `INFRA_BLOCKED` por [incidente operacional documentado pela coordenação](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/948121599b546d61579dc9ecb8c316f9c088e78a/Web3Bugs-certora/docs/cvl2/coordination/ROUND6_WSL_IO_INCIDENT.md). Durante a R7 **NENHUM comando remoto foi enviado ao WSL**: sem `ls`, `git`, Python, solc, Certora, scratch, patch, reinstalação, worktree ou build. Publicação apenas pelo conector GitHub, somente arquivos em `Web3Bugs-certora/docs/cvl2/research/AGENTE-03/`.

## Leituras obrigatórias e fonte dos comparativos — executadas via API GitHub

| Material | Commit/ref ou blob Git | Evidência lida |
| --- | --- | --- |
| `docs/spec_catalog.md` | blob `7211e9899e406c304c4828b5d02d221b5aa52b3f` | `complete` é completude de dependências, não migração/compilação CVL2 |
| `docs/spec_catalog_workflow.md` | blob `aa6fd6413c3be6487d6508f0795a08655feb84d9` | Regra de fechamento e integridade do CSV, N.spec, N.sol, N.md e N.txt |
| `docs/spec_catalog_project_1.md` | blob `fd5ed8777cd4e582e236490993f81e3285d6fb61` | P1: 36 complete, 34 incomplete, CVL2 intencionalmente pendente |
| `docs/standard.md` | blob `df4eefcc202ca5d7c441623cee81d8fdd6ec0e9a` | critérios e ambiguidade de Bug Labels; sem alterar labels |
| `results/spec/complete/1/1.spec` vs `incomplete/1/1.spec` + `.txt` | blobs `97c6fab42b4b842a6295aecd8fe114fdaf492f93`, `aa1dfa06333017605c084183c1a0ba08527be26c`, `5532f7655504754fad73aa1a6c69795c9f42df8e` | A primeira pode ser completa no catálogo com `methods` CVL1; a segunda tem `queue2` historicamente não resolvido |
| Painel PR #47 | `948121599b546d61579dc9ecb8c316f9c088e78a` — `ROUND6_DASHBOARD.md`, `ROUND6_PROGRESS.csv`, `ROUND6_COMPILATION_OBSERVATIONS.csv`, `ROUND6_WSL_IO_INCIDENT.md` | 4 compilações CVL2 limitadas, 12 erros reais, 1.370 sem teste no universo global; EIO/SIGBUS/EROFS externos ao parser |
| R6 AG03, base para R7 | `b5b00c683395e5277f4bd2c7e380ebe42db5575a`, `round6_evidence_matrix.csv` blob `195f5bd5280654f812cbde5f0abfda824166b066` | 164 registros; hashes N.spec herdados e canônicos preservados |
| CSV catalogado histórico | `results/spec/spec_buglabel.csv` blob `97e20443586540034a4c0305ce1db19b0d2f8cb5` no ref original da branch | Fonte canônica de Status, Property, Target, Bug Label, Result e Detection Outcome |

As fontes CVL2 oficiais foram consultadas: [migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html) e [hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html). CVL2 exige `function` e `;` no `methods` e cuidado específico com receiver, summary, visibilidade e contexto global; o documento não presume equivalência por gramática.

## QA R7 **realmente executado**, sem WSL

- **GET GitHub** da HEAD inicial PR #36 `b5b00c683395e5277f4bd2c7e380ebe42db5575a` e `draft=true`, `merged=false`: **OK**. Branch existente, sem reset, rebase ou branch duplicada.
- **GET GitHub dos 8 arquivos CVL completos** (`LEHighLevel`, `LEInProgress`, `LEPreset`, `LEValidStates`, `LEVarTran`, `LaunchEvent`, `Staking`, `sanity`) em snapshot e fork `dba90f9`, conferência byte a byte das strings retornadas e blob Git: **8/8 coincidências**. Os arquivos `N.spec` são extratos e não foram confundidos com as specs completas.
- **Reconciliação via parser CSV em JavaScript in-memory** (executada no conector, não WSL) de `ROUND7_MATRIX_164.csv` contra `results/spec/spec_buglabel.csv`: **164 linhas, 164 chaves únicas, 33 colunas, 164 linhas originais correspondentes, 0 mismatches** nos campos `Property`, `Target Contract`, `Result`, `Detection Outcome`, `Bug Label`, `Original Spec`. Checagem do formato do SHA256 `N.spec` e blob da source em todas as linhas: **164/164**. Os hashes SHA256 de `N.spec` vêm dos artefatos R5/R6 já aferidos; **NÃO** foram recalculados contra os bytes de cada `N.spec` nesta rodada.
- **Grupos:** LEHighLevel 10; LEInProgress 3; LEPreset 1; LEValidStates 35; LEVarTran 19; LaunchEvent 76; Staking 19; sanity 1. Total = **164**.
- **Estados individuais:** `runtime_compilation_status=NOT_RUN` em **164/164**, `infrastructure_status=NOT_RUN_INFRA_BLOCKED_WSL_EIO_SIGBUS_EROFS` em **164/164**; `COMPILE_OK=0`, `COMPILE_ERROR=0`, `PREFLIGHT_AUTH_BLOCKED=0`, `SEMANTIC_PROVEN=0`. Nenhum resultado do PDF transportado ao CSV.
- **Comparação GitHub** inicial `b5b00c6...HEAD` após criar matriz e parecer: dois caminhos novos, ambos exclusivamente em `AGENTE-03/24`; **scope OK** por comparação de paths. Isso **não** é `git diff --check` local.
- **Fontes/linhas do Solidity e scripts recuperadas via GitHub:** LaunchEvent auditado/fork e Hunk #7, LaunchEventHarness override; Staking auditado/fork e `withdraw`; scripts `sanity.sh`, `verifyStaking.sh`, `stakingRule.sh`, `verifyLEVarTran.sh`; resposta 404 verificada nos paths específicos `certora/harness/Owner.sol`, `certora/spec/staking.spec`, `certora/specs/Staking.spec`, `certora/specs/staking.spec`, `certora/specs/sanity.spec`. Falta localizada **não equivale** a prova de inexistência em todo GitHub.
- **Contrarrevisão PR #42** HEAD `3cd8f72c35d94b4a48cb6155628cba4bea378c67`, read-only, P12/23–25 e P15/36, com fontes/linhas e resultados de compilação atribuídos ao próprio AG04. **0 alterações** na branch alheia.

## Comandos obrigatórios pós-commit — todos NÃO executados na R7

| Comando exato / cwd | Estado | Razão |
| --- | --- | --- |
| `python3 scripts/check_specs.py .` / `Web3Bugs-certora` | **NOT_RUN_INFRA_BLOCKED** | WSL não recuperado |
| `python3 scripts/check_contests_csv.py .` / `Web3Bugs-certora` | **NOT_RUN_INFRA_BLOCKED** | WSL não recuperado |
| `python3 scripts/check_contracts.py .` / `Web3Bugs-certora` | **NOT_RUN_INFRA_BLOCKED** | WSL não recuperado |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` / raiz Git | **NOT_RUN_INFRA_BLOCKED** | WSL não recuperado |
| `certoraRun --compilation_steps_only`, `solc`, CVL1, Prover completo | **NOT_RUN** | Segurança, infra e gates individuais não satisfeitos |

As fases WSL exigem **intervenção humana** antes de qualquer nova tentativa e devem registrar a HEAD efetivamente testada, stdout, stderr, exit code, cwd e eventuais hashes. Não se deve usar histórico de exit 0 de R4/R5 nem sucesso futuro de GitHub Actions para declarar esses quatro comandos **EXECUTADOS** na R7. CI é estrutural e separada.

**Estado de alerta:** `LARANJA` histórico, `VERMELHO` operacional; PR #36 **DRAFT**, sem merge/Prover/CVL1/Fase 2. **AGENTE-03 — RODADA 7.**
