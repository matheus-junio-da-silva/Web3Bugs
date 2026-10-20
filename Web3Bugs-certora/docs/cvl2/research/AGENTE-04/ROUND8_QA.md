# AGENTE-04 — RODADA 8 / QA realizado, QA pendente e gates

## Estado e separação rigorosa de execuções

O PR #42 permaneceu DRAFT; a HEAD inicial `462b5f9d7c1cf1d756aa960ec975998b39938dda` foi conferida ANTES do commit. O PR de coordenação #47 foi **mesclado à main como documentação/instrumentação de QA**, não como prova de CVL2 ou autorização de merge para #42. Nenhum processo, comando de filesystem, worktree, solc, Python, patch ou Certora foi enviado a `DESKTOP-5E26TVU`: incidente WSL `spawn EIO / SIGBUS / EROFS` permanece sem recuperação atestada.

### O que foi realmente EXECUTADO nesta rodada, fora do WSL

1. GitHub: leitura dos quatro normativos e das amostras complete/incomplete P1; últimas revisões PR #42 e documentação/painel R7; fetch dos originais de P2/12/15, upstreams Git SHA fixos e interfaces/métodos.
2. GitHub Git API: commit P2 histórico `12296ce4...` e árvore Git, verificados seis **gitlinks com SHAs**; recuperação de `foundry.toml` e `.gitmodules`, interface Chainlink exata por blob, `Ownable.sol` e `ICollectorController.sol`. **Não** se afirma import closure completo do Prover por essa leitura.
3. Reconciliação **in-memory JavaScript**: linhas do CSV canônico `results/spec/spec_buglabel.csv` (1.390 relações / 1.386 chaves); comparação de HEAD e baseline: mesmo blob `97e20443586540034a4c0305ce1db19b0d2f8cb5`. Cruzamento R7 157 casos pela chave original (Property, Target Contract, Result, Detection Outcome, N.spec e Bug Label) e geração R8 157 IDs distintos P2=15, P12=26, P15=116, zero divergências históricas.
4. Conteúdo R8 auditado em memória: só arquivos novos sob `docs/cvl2/research/AGENTE-04/`, sem trailing whitespace, sem linhas em branco extras no EOF, sem espaço antes de tab. **Verificação de texto, NÃO `git diff --check`.**
5. Auditoria cruzada PRs #40 e #46 **somente leitura**. Nenhum outro PR ou branch alterado.

### Observações CVL2 antigas — não reexecutadas

| Property AG04 | Autoria e rodada do teste REAL | Target | Resultado documentado |
| --- | --- | --- | --- |
| P12/complete/23 `setBorrowing` | AG04/R5 | UserConfigurationHarness snapshot, solc0.6.12, CLI 8.19.0 | `COMPILE_ERROR` EXIT 1, methods CVL1 |
| P12/complete/25 `setUsingAsCollateral` | AG04/R5 | UserConfigurationHarness snapshot, solc0.6.12, CLI 8.19.0 | `COMPILE_ERROR` EXIT 1, methods CVL1 |
| P15/incomplete/36 `limitOnDiscountRate` | AG04/R6 | GhoDiscountRateStrategyHarness, solc0.8.10, CLI 8.19.0 | `COMPILE_ERROR` EXIT 1, methods CVL1 |
| Outros **154** | nenhum teste CVL2 observado | target do catálogo não necessariamente runner | `NOT_RUN` |

**Rodada 8: zero novos `COMPILE_OK`, zero `COMPILE_ERROR` novo, zero PREFLIGHT_AUTH_BLOCKED, zero novos logs.** `NOT_RUN_INFRA_BLOCKED` é **atributo de infraestrutura da R8**, separado do status histórico de parser. `COMPILE_OK` do solc ABI R5 não é `COMPILE_OK` CVL2. Nenhuma equivalência formal nem projeto finalizado.

### Checks históricos pós-commit — status até recuperação do WSL

| Comando exato obrigatório | Escopo | Status |
| --- | --- | --- |
| `python3 scripts/check_specs.py .` | CWD `Web3Bugs-certora/` | **NOT_RUN_INFRA_BLOCKED** |
| `python3 scripts/check_contests_csv.py .` | CWD `Web3Bugs-certora/` | **NOT_RUN_INFRA_BLOCKED** |
| `python3 scripts/check_contracts.py .` | CWD `Web3Bugs-certora/` | **NOT_RUN_INFRA_BLOCKED** |
| `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` | raiz Git | **NOT_RUN_INFRA_BLOCKED** |

**Não** usar `validate: SUCCESS` para declarar os quatro comandos locais executados. A workflow padrão do PR executa `check_contests_csv`, `check_contracts` e `check_git`, mas não contém `check_specs` nem o comando Git literal `BASE...HEAD`. Caso o workflow pós-commit R8 apareça, registrar sua run/status exatos separadamente. Não atribuir parser exit ao ambiente avariado.

### Porta humana para retomar testes

O administrador deve comprovar backup e saúde de volume Windows/WSL. Somente após autorização, verificar I/O em diretório temporário **novo** e versões Python/Git/solc/CLI, HEAD/branch/worktree limpas e hashes de inputs; executar os três validadores e diff exato com logs e exit; então obter gate individual do coordenador antes de qualquer `--compilation_steps_only` scratch. Não rodar `reset`, `rebase`, `wsl --shutdown`, reinstalações ou patch na máquina sem essa recuperação. Não tocar em `results/spec`, `contracts`, labels e reports imutáveis.

**QA R8: documentação completada 157/157, 0 compilações novas, controle textual/GitHub em memória; QA local bloqueado por infra.**

**Alerta:** técnico LARANJA (equivalência ausente) + operacional VERMELHO (intervenção humana WSL obrigatória).

**AGENTE-04 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS**
