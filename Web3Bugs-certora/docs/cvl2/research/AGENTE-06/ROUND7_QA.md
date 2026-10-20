# AGENTE-06 — Rodada 7 / QA verificável e limites de execução

**Data:** 2026-10-20. PR [#38](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/38), branch \`research/cvl2-agente-06\`, HEAD de partida \`abdd7d4a9eefc4156d1c4c7d3efc717b8296754d\`. Baseline histórico imutável \`2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3\`. O coordenador marcou [ROUND6_WSL_IO_INCIDENT.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/948121599b546d61579dc9ecb8c316f9c088e78a/Web3Bugs-certora/docs/cvl2/coordination/ROUND6_WSL_IO_INCIDENT.md) como \`INFRA_BLOCKED\` após EIO, SIGBUS e EROFS, incluindo \`spawn EIO\` reproduzido em comandos triviais. **Não houve confirmação de recuperação antes deste trabalho. Por instrução, nenhum comando de shell/WSL, build, compile, patch, worktree, script Python ou escrita naquele dispositivo foi tentado na Rodada 7.**

## Fonte e integridade das 159 linhas

**Operações realmente realizadas pelo conector GitHub (sem execução de shell):**

1. Ler, antes de alterar documentação, os quatro arquivos obrigatórios: \`docs/spec_catalog.md\` (79 linhas), \`docs/spec_catalog_workflow.md\` (487), \`docs/spec_catalog_project_1.md\` (90), \`docs/standard.md\` (270), e comparar P1 \`complete/1/1.spec\`, \`complete/1/3.spec\`, \`incomplete/1/1.spec\`, \`incomplete/1/15.spec\`, \`incomplete/1/29.spec\`.
2. Ler a revisão mais recente da coordenação [#38/5590011864](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/38#pullrequestreview-5590011864), painel [ROUND6_DASHBOARD.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/948121599b546d61579dc9ecb8c316f9c088e78a/Web3Bugs-certora/docs/cvl2/coordination/ROUND6_DASHBOARD.md), \`ROUND6_PROGRESS.csv\`, \`ROUND6_COMPILATION_OBSERVATIONS.csv\` e incidente operacional da mesma SHA.
3. Reconciliar em memória [ROUND6_MATRIX_159.csv](ROUND6_MATRIX_159.csv) e [ROUND7_MATRIX_159.csv](ROUND7_MATRIX_159.csv) com os **bytes textuais da \`results/spec/spec_buglabel.csv\` histórica lidos por GitHub**. Resultado **1390 relações, 1386 identidades no catálogo, 159/159 identidades do agente únicas e presentes**, P1=70, P4=27, P17=41, P22=21. **Zero divergências** em \`Property\`, \`Target Contract\`, \`Result\`, \`Detection Outcome\` ou paths \`N.spec\` referidos na matriz prévia. \`Bug Label(s)\` preservados, inclusive 3 chaves com dois labels (P1/complete/1, P1/complete/26, P4/incomplete/4).
4. As 159 strings SHA-256 de N.spec em R7 foram **conferidas contra a R6 anterior**, cujos SHA já tinham sido reconciliados ao índice R5. **Não houve re-hash dos bytes físicos de N.spec nesta R7**, pois não se utilizou runtime/FS; não atribuir nova verificação criptográfica dos arquivos originais à R7. Todos os originais e links/targets históricos foram preservados.
5. Reabrir por GitHub os três documentos novos então disponíveis (\`ROUND7_MATRIX_159.csv\`, \`ROUND7_EVIDENCE.md\`, \`ROUND7_PR41_READONLY_AUDIT.md\`) para inspeção de texto. 159 linhas de dados, 159 chaves distintas, 159 status \`NOT_RUN\` e 159 \`infra_execution_gate=NOT_RUN_INFRA_BLOCKED_WSL_EIO_SIGBUS_EROFS\`, **nenhuma regra executada**, **zero trailing whitespace ou espaços antes de tab nesses três artefatos**. O check de arquivos por conector **não é** \`git diff --check\`.

## Categorias sem confusão

| Indicador do escopo AGENTE-06 R7 | Quantidade | Prova |
| --- | ---: | --- |
| Exemplo catalogado/documentado | **159** | CSV baseline + matrizes anteriores + ROUND7_MATRIX_159 |
| \`certoraRun --compilation_steps_only\` **COMPILE_OK** | **0** | Nenhum comando de compilação executado nesta carteira |
| \`COMPILE_ERROR\` parser/typechecker CVL2 | **0** | Não contar erros Solidity/SIGBUS |
| \`PREFLIGHT_AUTH_BLOCKED\` CVL2 | **0** | Nenhuma tentativa autenticada de CLI na R7 |
| \`NOT_RUN\` CVL2 | **159** | Status por ID na matriz |
| \`NOT_RUN_INFRA_BLOCKED\` (motivo de não execução, **não classe de erro CVL2**) | **159** | Incidente documentado; bloqueio global |
| \`SEMANTIC_PROVEN\` | **0** | Nenhuma equivalência de contraexemplos/axiomas/reverts demonstrada |
| \`MIGRATED_COMPLETE\` | **0/4** | Nenhum dos quatro projetos finalizado |

**Preexistentes, não repetidos:** R5 patch P4 fuzz=0 aplicado em scratch derivando 36→37 fontes; R6 instalação de solc-js 0.8.17 em scratch exit 0 mas extração ABI terminada em SIGBUS; R6 tentativa dos três Python local exit 135; GitHub Actions da R6 \`validate\` SUCCESS. Nenhum desses eventos conta como compilação CVL2.

## Comandos obrigatórios pós-commit — status real

| Comando exigido | Rodada 7 | Razão |
| --- | --- | --- |
| \`python3 scripts/check_specs.py .\` em \`Web3Bugs-certora/\` | **NOT_RUN_INFRA_BLOCKED** | WSL não recuperado; não tentar spawn em volume EIO |
| \`python3 scripts/check_contests_csv.py .\` | **NOT_RUN_INFRA_BLOCKED** | Idem |
| \`python3 scripts/check_contracts.py .\` | **NOT_RUN_INFRA_BLOCKED** | Idem |
| \`git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD\` no root Git | **NOT_RUN_INFRA_BLOCKED** | Não foi executado por CLI no WSL nesta rodada; GitHub compare e inspeção estática não são equivalentes |

**Importante:** na última HEAD R7, o conector \`compare_commits\` pode ser usado para comprovar que todos os arquivos alterados estão na pasta autorizada; eventual \`validate\` SUCCESS do GitHub é evidência de CI externo, **não** execução dos quatro comandos locais. Atualizar status no comentário final do PR com a HEAD exata e a observação de CI quando disponível, sem reescrever este histórico.

## Condições de retomada pelo administrador e coordenador

1. O responsável pelo computador deve confirmar integridade do volume WSL, backups e que processos básicos de leitura e **escrita apenas em scratch novo** funcionam; não tentar recuperação/destruição automática de worktrees, especialmente sem inspeção do administrador.
2. Confirmar \`python3\`, \`git\`, saúde das refs e worktrees e SHA remoto/local sem \`reset\`; em seguida rodar **exatamente** os três validadores e \`git diff --check BASE...HEAD\` a partir dos diretórios requisitados.
3. Só após o gate mecânico e evidência histórica individual de ABI+target+runner, permitir, mediante decisão do coordenador **por propriedade**, cópia byte-idêntica em scratch, SHA de todos os inputs, compilador solc versionado, timeout/log stdout/stderr e \`certoraRun --compilation_steps_only\`. Não assumir que solc/ABI ou sucesso CI valida semântica.

**Estado:** integridade documental pesquisada, QA local pós-commit **PENDENTE por infraestrutura**, sem Fase 2/Prover/CVL1/merge.

**AGENTE-06 — RODADA 7.**
