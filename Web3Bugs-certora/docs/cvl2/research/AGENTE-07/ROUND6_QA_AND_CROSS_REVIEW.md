# AGENTE-07 — Rodada 6 / QA, execução e cross-review

**PR de pesquisa exclusivo:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41 (Draft). Baseline fixo `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Branch `research/cvl2-agente-07`. Nenhuma alteração em `results/spec`, `contracts`, `reports`, `resources`, CSV original ou `.env`.

## Matriz e integridade de escrita

- `ROUND6_MATRIX_156.csv` foi produzida a partir de `ROUND4_MATRIX.csv` e `ROUND5_MATRIX_156.csv`, mantendo `Project ID`, status original, Example ID, `property`, target, Result, Detection Outcome, SHA-256 da source N.spec, origem auditada, blocker, família, risco/vacuidade, gate e evidência. O parser CSV identificou **156 linhas e 156 chaves únicas**: P9 61, P8 42, P20 37, P11 16.
- Estado observado exclusivamente no escopo deste agente em R6: `COMPILE_OK=0`, `COMPILE_ERROR=0`, `PREFLIGHT_AUTH_BLOCKED=0`, `NOT_RUN=156`. O campo `cvl2_command=NOT_EXECUTED`, `cvl2_exit_code=N_A_NOT_EXECUTED` e `cvl2_log=NONE` impede interpretar ausência de execução como erro de parser. Solc Solidity da Rodada 5 permanece anotado como evidência anterior, não CVL2 e não reexecutado em R6.
- Todos os 156 SHA-256 foram transportados sem alteração do cadastro R5 que já os havia conferido contra N.spec; **não se afirma nova leitura física de SHA depois que o WSL sofreu erros de I/O**. Os Result/Outcome históricos estão preservados na matriz.

## Ambiente local — impedimento real e comandos executados

- Após criar worktree isolado com HEAD inicial `a4a9a32d0c320189ffbab0faf05fd0a506e10a32` e worktree **detached** read-only do PR #43, o WSL `DESKTOP-5E26TVU` começou a apresentar erros intermitentes de filesystem: `python3 -c ...` e `python3 -V` encerram por **Bus error**, `/usr/bin/df -h` por **Input/output error**, e Git alerta sobre `.git/objects/info/alternates` inacessível. Por segurança não se escreveu, removeu, resetou ou fez push diretamente no worktree defeituoso.
- O CLI direto `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun --version` **foi consultado** e reportou `certora-cli 8.19.0`. Isso é um `--version`, não prova, compilação nem preflight auth.
- **Não executados localmente após os commits nesta rodada:** `python3 scripts/check_specs.py .`, `python3 scripts/check_contests_csv.py .`, `python3 scripts/check_contracts.py .` e `git -c core.whitespace=cr-at-eol diff --check BASE...HEAD`. Os erros do runtime tornam indevido declarar `EXIT 0` ou `EXIT 1` dessas verificações. Devem ser repetidas em WSL restaurado ou worktree saudável antes de usar o gate de QA local.
- Os documentos desta rodada foram enviados à branch Draft exclusivamente por conector GitHub, sem alterar a branch de outro agente; nenhum novo Prover, CVL1, CVL2 `--compilation_steps_only`, Solidity compilation, npm install, patch, deploy, token ou credencial.

## QA automatizado em GitHub Actions — não substitui todos os comandos locais

- O workflow `validate` da branch, após a atualização da matriz nesta rodada, executou `integrity_validation` com conclusão **SUCCESS**: [run #39473181478](https://github.com/matheus-junio-da-silva/Web3Bugs/actions/runs/39473181478). As etapas reportadas explicitamente são `check_contests_csv=success`, `check_contracts=success` e `check_git=success`. **Não há etapa independente `check_specs` indicada nessa listagem**; não atribuir a esse workflow um comando ausente.
- As conclusões acima são **de CI**, não de processos invocados pelo agente no WSL depois de commit; o parser CVL2, semântica e axiomas não foram testados. O coordenador ainda precisa do diff CLI completo `BASE...HEAD` e dos três validadores conforme o protocolo, quando o runtime estiver íntegro.

## Revisão cruzada PR #43 — leitura, não alteração

- **PR:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43, HEAD conferida `97924c06366bacc260a8adebfa0c3754887248c2`, permanece Draft. Checkout WSL detached para leitura foi criado mas ficou sujeito aos mesmos erros de I/O; a contrarrevisão desta rodada usou **leitura remota via conector GitHub**, não invocou shell, patch, branch reset ou compilador na branch AGENTE-08.
- `ROUND5_MATRIX_155.csv` tem 155 linhas, cada uma com `UNRESOLVED_CANDIDATE`, sem `COMPILE_OK`. P5 representa 17 exemplos, P14 34; nenhum foi promovido.
- **P5:** `ROUND5_EVIDENCE_AND_GATES.md` reporta compilação Solidity `solc 0.8.10` do BridgeHarness pós-patch com 34 funções ABI e SHA de ABI `4f74e2f892107a4d39768c4ac969cd7f5d6d4449bf008c16375ef2b5c562ca4b`; `solc exit 0` pertence ao agente-08, **não** a esta contrarrevisão, e não demonstra `certoraRun --compilation_steps_only` ou versão do Prover histórico. Documenta também uma primeira tentativa exit 1 por symlink, não ocultada, e divergência de bytes frente ao snapshot.
- **P14:** `ROUND5_EVIDENCE_AND_GATES.md` registra `solc 0.6.10` para Controller original e pós-`applyHarnesses.sh`: 39 funções externas originais, 42 pós-script (+3 getters de state) e mutações internas em `getExcessCollateral`, `settleVault` e `_runActions`; essas alterações podem modificar comportamento mesmo quando outros selectors continuam iguais. É compilação **Solidity** em scratch pelo agente-08, não prova CVL2, e não reconstrói automaticamente o runner auditado.
- **Assertions preservadas no repositório:** `results/spec/complete/14/1.spec:10` contém literalmente `assert true;` dentro do controle de fluxo da rule; `results/spec/complete/14/25.spec:31–32` mantém `sinvoke settleVault(...)` e `assert false;`. Mudar/remover estes termos para facilitar parsing ou provar sucesso mudaria o universo de propriedades, portanto não autorizado.
- **Parecer limitado:** nenhum rebaixamento indevido ou promoção foi visto nessas evidências; os 155 continuam unresolved, e hashes/ABI compilados em scratch não aprovam equivalência. Não é auditoria formal de todas as 155 regras. Gate para P5: scene/links históricos; para P14: ABI pós-mutação e efeito dos ramos/reverts no verdadeiro run.

## Sinalização e ação seguinte

- **VERMELHO P8** (risco de modelo inconsistente, requer autorização de estudo de satisfatibilidade e alcance); **LARANJA P9 e P20** (ABI/imports/patch e semântica de exceções); **AMARELO na closure textual P11 / LARANJA no run histórico**.
- **AMARELO no QA desta rodada**: matriz publicada com integridade de contagem e CI parcial de GitHub, porém os quatro comandos CLI pós-push obrigatórios estão pendentes por erro de I/O do WSL. Se o dispositivo não recuperar, pedir execução independente do coordenador; não fabricar outputs.
- PR #41 e #43 permanecem Draft. Sem merge, sem migração concluída, sem equivalência demonstrada.

**AGENTE-07 — RODADA 6**
