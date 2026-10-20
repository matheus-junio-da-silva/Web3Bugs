# AGENTE-07 — Rodada 9 / QA efetivamente executado e gates de compilação

**Base:** `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. **Branch:** `research/cvl2-agente-07`, PR [#41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41) Draft. HEAD inicial `dc737f6470041d1422ca86e4c4594607fdb57a28`. Novo worktree isolado `/home/mat/cvl2-agent07-round9-20261020`, branch local `research/cvl2-agente-07-round9`, checkout sem alterações anteriores; nenhum reset ou rebase. Todos os commits **somente em `Web3Bugs-certora/docs/cvl2/research/AGENTE-07/`**.

## Saúde WSL e trabalho permitido

No início do trabalho, o dispositivo WSL `DESKTOP-5E26TVU` executou `pwd`, `python3 --version` (3.14.4), `git --version` (2.53.0), `df -h /home/mat` (volume `/dev/sdd`, 915G disponíveis) e `git status --porcelain` (vazio) **sem EIO/SIGBUS/EROFS**. Uma worktree nova foi criada do **HEAD remoto exato**; não se tocou na branch/colega #43. `certoraRun` local existe em `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun`, porém **nenhum `certoraRun --compilation_steps_only` nem Prover/CVL1 foi invocado nesta R9**. A inspeção de `command -v solc5.17` e dos artefatos solc-select indicou solc5.17 indisponível no caminho consultado, bloqueando a reprodução do novo runner Keep.

## Verificações reais pré-commit da Rodada 9

Executadas em `Web3Bugs-certora/` da worktree isolada:

| Comando | Resultado real |
|---|---|
| `timeout 120 python3 scripts/check_specs.py .` | **EXIT 0**, `1386 spec examples and 1390 Bug Label relationships are structurally consistent` |
| `timeout 120 python3 scripts/check_contests_csv.py .` | **EXIT 0**, contests.csv consistente com reports |
| `timeout 120 python3 scripts/check_contracts.py .` | **EXIT 0**, contracts consistente com reports |
| `git status --porcelain` (antes da escrita) | vazio |
| Inspeção textual de whitespace dos documentos novos pré-commit | zero linhas com trailing whitespace |

**Reexecução pós-commit obrigatória:** após o commit final e push da branch de pesquisa, repetir **os três validadores** acima e `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` do root Git. Relatar o exit exato no comentário do PR e não substituir por GitHub Actions. Este relatório preserva os valores efetivamente registrados até a criação, sem inventar o status de futuras execuções.

## Reconciliação individual e hashes

`ROUND9_MATRIX_156.csv` foi produzido de `ROUND8_MATRIX_156.csv` e do CSV original `results/spec/spec_buglabel.csv`, com parser CSV que respeita aspas. **156/156 chaves distintas** `(project_id,original_status,example_id)`; P8 42, P9 61, P20 37, P11 16. Comparação por chave e todas as relações canônicas: **zero discrepâncias** de `Property`, `Target Contract`, `Result`, `Detection Outcome`, `Original Spec`, `Original Spec Lines` e Bug Label. **156/156 SHA256 de N.spec recalculados fisicamente e iguais** aos de R8; cada SHA256 e Git blob do full original `contracts/.../*.spec` também calculado em R9 e registrado por propriedade. Result histórico: **32 VERIFIED, 5 VIOLATED, 119 NOT_STATED** (não reclassificados). `ROUND9_P8_WITNESS_MAP_42.csv`: 42 entradas, 22 W1, 1 W2/W3, 19 outros, com linhas CVL, sha do full spec e contagem textual de `rule`/`invariant`/summaries; contagem de texto **não** prova scheduling do Prover. `ROUND9_KEEP_RUNNER_MANIFEST.csv`: seis fontes pinadas, quatro blobs do snapshot byte-idênticos ao upstream público, runner e package lock exclusivos da revisão externa.

## Execuções de Prover/CVL2: nenhuma

| Estado estrito da carteira AGENTE-07 | Contagem R9 |
|---|---:|
| Documentados | **156 / 156** |
| Tentativas compile-only **originais nesta rodada** | **0** |
| Tentativas compile-only **derivadas nesta rodada** | **0** |
| `COMPILE_OK` CVL2 atribuível a esta carteira | **0** |
| `COMPILE_ERROR` CVL2 atribuível a esta carteira | **0** |
| `PREFLIGHT_AUTH_BLOCKED` | **0** |
| `NOT_RUN` CVL2 | **156** |
| Equivalências semânticas provadas | **0** |
| Projetos integralmente migrados | **0** |

Globais no PR #48 são **18 tentativas distintas em 16 properties**, 6 OK restritos, 12 errors originais, com sobreposição 2; 1.370 properties sem teste; não atribuir execuções da coordenação/agentes à carteira P8/P9/P11/P20. Uma falha de infraestrutura, compilação Solidity simples, `--version` ou workflow `validate` não é resultado do parser CVL2.

## Gate e cross-review

O runner da revisão Keep `a5cd171...` está recuperado e os três harnesses e full spec do snapshot coincidem em bytes. Seu solc5.17 e o compromisso temporal do relatório `658b02f...` permanecem sem comprovação. **Um único candidato, apenas proposto:** `P11/incomplete/1` `validOperator`, N.spec SHA256 `fc3118de451ccadcfd2d4c324d707ba569eee6cefa445327a643b64ba2623450`. Autorizar eventual compile-only separado para N.spec vs full-spec em scratch com toolchain e hash completos, timeout e nenhum Prover; não gerar mock ou import falso. Outra prioridade documental é **P9/complete/6**, verificar fase/selector (`authorizeSignerWithSignature` existe no snapshot Accounts.sol:407 mas não na ABI phase2 isolada).

Contrarrevisão **READ-ONLY** de PR [#43](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43) HEAD `f38d9089e6ceeb85b1c54d2df07a44f7cea577ce`: produção Radicle `6fe9d38` versus branch posterior `8d1db123`; mesmos scripts `SplitsHarness` mas com `--send_only`; overrides vazios e CVT não atestado. Nenhuma edição em arquivos de outros agentes.

**AGENTE-07 — RODADA 9 / EVIDÊNCIAS, TESTES CONTROLADOS E CONTRARREVISÃO**
