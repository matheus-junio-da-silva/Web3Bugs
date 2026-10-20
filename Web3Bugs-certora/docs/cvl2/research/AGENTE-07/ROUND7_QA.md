# AGENTE-07 — Rodada 7 / QA, proveniência de execução e bloqueios

**Base histórica imutável:** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. **PR:** [#41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41), **DRAFT**, branch `research/cvl2-agente-07`. Partida R7 conferida em `104f6deef80ac95ab5fec75c3e5ebb01f075f6fe`, sem reset, rebase, merge ou modificação do WSL.

## Gate estrutural verificado por conector GitHub, sem WSL

Fonte da verdade para resultados e labels: `Web3Bugs-certora/results/spec/spec_buglabel.csv` em `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`, Git blob `97e20443586540034a4c0305ce1db19b0d2f8cb5`. Leitura via GitHub: **1390 relações**/linhas e **1386 identidades únicas**. Comparação exata, em memória, de todas as 156 chaves da matriz R6 e R7 contra a fonte canônica usando `(Project ID, Status, Example ID)`:

- **156/156 chaves únicas**; 61 P9, 42 P8, 16 P11, 37 P20; zero nomes, targets, resultados históricos, Detection Outcomes e `Original Spec` discrepantes.
- SHA-256 de cada `N.spec` preservado da matriz R6/R5, onde já haviam sido verificados frente aos arquivos originais; **NÃO** houve novo recálculo físico do SHA por filesystem local nesta R7. Não confundir Git blob SHA-1 com hash SHA-256 da source.
- `ROUND7_MATRIX_156.csv` contém 33 colunas com status e comando/exit por ID, contexto full-spec vs fragmento extraído, família e risco, `INFRA_EIO` distinto, próximo gate e proveniência.
- P8 segmentado em 22 W1, um W2/W3, 19 outros. P20 mapeado por `Original Spec`: BentoBox 8, BentoBoxCompoundStrategy 8, CompoundStrategy 6+1, Rebase 8, strategy 3+3; 37/37 conferidos no catálogo.
- Compilações novas atribuídas a P8/P9/P11/P20 nesta rodada: **zero**.

**Ressalva:** o status de `NOT_RUN` é CVL2 do N.spec; `INFRA_EIO` é causa impeditiva ambiental. Nenhum erro de parser, token/CERTORAKEY, `--version`, ABI Solidity, workflow GitHub ou input CSV equivale a `COMPILE_ERROR` ou `COMPILE_OK` de CVL2.

## Comandos locais e status real

Conforme [PR #47 / ROUND6_WSL_IO_INCIDENT.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/948121599b546d61579dc9ecb8c316f9c088e78a/Web3Bugs-certora/docs/cvl2/coordination/ROUND6_WSL_IO_INCIDENT.md), o administrador ainda não atestou recuperação do filesystem WSL. O incidente reproduzido envolve `spawn EIO`, `SIGBUS`, `EROFS` e `Input/output error`. **Por orientação explícita, NÃO tentei executar novas instruções no WSL.**

| Comando obrigatório | Executado localmente após R7? | Resultado declarado |
|---|---|---|
| `cd Web3Bugs-certora && python3 scripts/check_specs.py .` | NÃO | `NOT_RUN_INFRA_BLOCKED`; nenhum exit code |
| `cd Web3Bugs-certora && python3 scripts/check_contests_csv.py .` | NÃO | `NOT_RUN_INFRA_BLOCKED`; nenhum exit code |
| `cd Web3Bugs-certora && python3 scripts/check_contracts.py .` | NÃO | `NOT_RUN_INFRA_BLOCKED`; nenhum exit code |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | NÃO | `NOT_RUN_INFRA_BLOCKED`; nenhum exit code |

A execução GitHub Actions `validate` (quando disponibilizada) é **fonte independente CI**, não substitui os quatro comandos locais acima. As verificações já concluídas em rodadas anteriores não são apresentadas como execuções da R7. Não rodar `--compilation_steps_only` antes da recuperação, da cena autenticada e de autorização individual.

## Cross-review PR #43 — somente leitura

Revisão mais recente do coordenador em [#5590013542](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43#pullrequestreview-5590013542), HEAD `748a8e345061961faf977f78cf9bcce7739e8385` no início da investigação. Com conector GitHub, relidos `AGENTE-08/ROUND6_FINDINGS.md`, `complete/14/1.spec`, `complete/14/25.spec`, `incomplete/5/14.spec`.

- P5/14 `alwaysUnSent` usa os getters `withdrawMessageStatus` e `bridgeRewardsMessageStatus`; BridgeHarness upstream solc0.8.10 (34 funções ABI) e 11 seeds estão **apenas documentados**, sem CVL2 execute; tentativa do outro agente foi barrada por filesystem `EROFS`, e não pelo parser.
- P14/1 conserva `assert true;` na linha 10; P14/25 conserva `sinvoke settleVault(...)` na linha 31 e `assert false;` na linha 32. O patch `Controller` altera `getExcessCollateral`, acessos a arrays no índice 0, `settleVault` e `_runActions`. Os 39→42 métodos externos dizem respeito somente à ABI compilada de Solidity, não garantem universo de reverts e contraexemplos.
- P5/P14 seguem 17/34 unresolved respectivamente; nenhum `COMPILE_OK` CVL2 nem equivalência; nenhum arquivo da branch AGENTE-08 alterado. Esta é contrarrevisão documental, não reexecução de patches ou comparação formal.

## Ação humana para fechar QA

1. Administrador deve recuperar WSL de forma controlada e comprovar saúde de leitura/gravação temporária, Python, Git, worktrees e volumes antes de qualquer compilação.
2. Em checkout isolado limpo, verificar HEAD **atual** remota do PR #41, preservar a branch sem reset, rodar os três validadores no diretório `Web3Bugs-certora` e o `git diff --check BASE...HEAD` na raiz; registrar stdout/stderr, códigos de saída e SHA.
3. Só depois, e com autorização por property/target, permitir diagnóstico limitado `certoraRun --compilation_steps_only` em cópias scratch byte-idênticas com versões e timeout. **Não há gate para Prover ou Fase 2.**

**AGENTE-07 — RODADA 7**
