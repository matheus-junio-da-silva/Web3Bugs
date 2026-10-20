# AGENTE-05 — Rodada 5: cinco diagnósticos P7 com ABI, `method f` e CVL2

**Data:** 2026-10-20. **Baseline:** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. **Execução:** scratch fora do Git, sem Prover nem CVL1. As três análises `COORDINATOR_CLOSURE_P7_3_37_65.md`, `COORDINATOR_HISTORICAL_RUNNER_AND_ABI_P7.md` e `COORDINATOR_CVL2_COMPILATION_DIAGNOSTIC_P7.md` foram confrontadas com os arquivos locais. Nenhum `N.spec`, CVL integral, contrato, `require`, `assert`, `ghost`, `hook`, `methods` ou summary foi editado.

## Reprodutibilidade e evidência de execução

Todos os cinco `N.spec` originais foram copiados com `shutil.copyfile` para `/tmp/cvl2_agente05_round5_compile_20261020/<ID>/specs/property.spec`. Cópias dos 128 arquivos presentes sob `contracts/7/contracts/` foram comparadas por mapa de SHA-256 relativo ao snapshot. Digest SHA-256 do mapa serializado: `097bbb8b5d7f76c92b748e1d476da0f1f407140d01e28f0215d03c71241053ef`, idêntico nos cinco cenários. Hashes individuais de fonte/cópia `N.spec`, comandos, cwd, timeout, exit code, stdout e stderr estão em [round5_logs/ROUND5_COMMAND_MANIFEST.json](round5_logs/ROUND5_COMMAND_MANIFEST.json).

Ferramentas: `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun` (**certora-cli 8.19.0**, invocado diretamente, sem wrapper local que exige token), `/home/mat/.solc-select/artifacts/solc-0.8.10/solc-0.8.10` (**solc 0.8.10**), `--compilation_steps_only`, `--solc` explícito, `timeout` de processo controlado via subprocess Python (`65s`), `HOME` temporário e variáveis de credenciais removidas. O processo nunca recebeu token; nenhuma chamada de verificação formal, `--cloud` ou compilação CVL1.

Comando por alvo, executado no cwd do ID:
`certoraRun contracts/protocol/tokenization/{StableDebtToken|VariableDebtToken}.sol:<TARGET> --verify <TARGET>:specs/property.spec --compilation_steps_only --solc /home/mat/.solc-select/artifacts/solc-0.8.10/solc-0.8.10`.

| ID | Fonte `N.spec` SHA-256 | Solc target | CLI exit / diagnóstico de fragmento | Stdout original |
| --- | --- | --- | --- | --- |
| P7/complete/41 | `205a0ea773b419500bf520f298d09d3b792da4c895bdccc63c06f306bd43f3b6` | StableDebtToken | **1 / `SNAPSHOT_FRAGMENT_CVL2_COMPILE_ERROR`**, `sig:` em definição e selector final | `round5_logs/41_stdout.log.gz` |
| P7/complete/63 | `10b938fdc91aa8fbb3f0eb6666eb2ab10b9f4e40a013c633eedc968581770fee` | VariableDebtToken | **1 / COMPILE_ERROR**, `sig:` em definição e selector final | `round5_logs/63_stdout.log.gz` |
| P7/complete/36 | `d9283f4ac712abd16d21e8b2f16b83fc3488767feeed40fb658122a51ae66da9` | StableDebtToken | **1 / COMPILE_ERROR**, `sig:` na definição | `round5_logs/36_stdout.log.gz` |
| P7/complete/47 | `0cf2150c11cfb9926d3e24eecc1fb7ce0c9ffeb956ec3553dab606d026a8416e` | StableDebtToken | **1 / COMPILE_ERROR**, `sig:` na definição | `round5_logs/47_stdout.log.gz` |
| P7/complete/73 | `c82afdd9a07a75c9c6cad9b20eee201cb212017cc4cd01c6266bc90b42c8a76b` | VariableDebtToken | **1 / COMPILE_ERROR**, `sig:` na definição | `round5_logs/73_stdout.log.gz` |

**Log completo:** todos os cinco stdout e cinco stderr foram copiados sem alteração em `7/round5_logs/` (os stderr estão vazios). Os três diagnósticos de StableDebtToken 41/36/47 incluem um aviso auxiliar `Stack too deep` no autofinder, seguido por fallback ao original; a saída **continua 1 por erro CVL2 nos selectors**. Não confundir o aviso auxiliar com o código de saída do CLI. Nenhuma das cinco rules pode ser chamada `COMPILE_OK`.

## ABI concreta extraída no mesmo snapshot

Compilação **Solidity-only** por `solc 0.8.10 --abi` em scratch: StableDebtToken retorna 33 funções (ABI SHA-256 `ca90069b8ded4fc0bd8b9e2ce2ab01a16354ad2f3f10892284f212c915b895ce`); VariableDebtToken retorna 30 funções (ABI SHA-256 `290cb7e7169196614739feb89a7324e8937847300de809b29941fb9622552ab3`). Arquivos gerados byte-a-byte preservados em `round5_logs/abi/`.

Em **ambas** as ABIs, o conjunto disallowed da definição CVL compreende **exatamente seis selectors reais**: `transfer(address,uint256)`, `allowance(address,address)`, `approve(address,uint256)`, `transferFrom(address,address,uint256)`, `increaseAllowance(address,uint256)` e `decreaseAllowance(address,uint256)`. Todos constam das ABIs, e todos revertem com `Errors.OPERATION_NOT_SUPPORTED` no Solidity do snapshot: `StableDebtToken.sol:365–386`, `VariableDebtToken.sol:127–148`. `allowance` é `view`, mas **também reverte**. Portanto, o filtro de P7/47 e 73 **não é vazio como conjunto de funções ABI**; isto **não** é uma prova de satisfatibilidade do domínio simbólico usado pelo Prover.

Entre as funções de ABI há 11 `nonpayable` por target, das quais cinco estão nos selectors excluídos. Logo a aproximação por ABI de `!f.isView && !disAllowedFunctions(f)` deixa **seis assinaturas** de cada contrato: `approveDelegation`, `burn`, `delegationWithSig`, `initialize`, `mint`, `setIncentivesController`. Esta contagem é **ABI-only**, não enumeração de todo o universo CVL (fallback, cenas múltiplas, proxies, `method` dispatch, inicialização e linkings podem diferir). Stable e Variable têm variantes distintas de `burn` e remain targets separados.

## Diagnóstico por example ID, recorte vs spec integral

| ID / regra | CVL preservado | Relevância da spec global e Solidity | Risco / próximo gate |
| --- | --- | --- | --- |
| **41** `nonceChangePermits` | `StableDebtToken.spec:226–236`, definição `:14–20`; `N.spec` contém só definição e rule | O filtro `method f` pode atingir `mint/burn` e assim hooks Sstore/Sload de `_userState.balance` da spec integral `:114–123`. Summaries globais de `calculateCompoundedInterest`, `rayMul`, `rayDiv` (spec `:1–9,22–103`) podem afetar caminhos quando `f` não é `delegationWithSig`. Se `f` for delegation, `DebtTokenBase.sol:43–68` usa EIP712/ecrecover, `_nonces` e `_borrowAllowances`. | `f(e,args)` sem `@withrevert` poda reverts; não declarar que a implicação abrange todos os métodos sem satisfatibilidade. Precisa preservar global methods, hook e domínio ABI. |
| **63** `nonceChangePermits` | `VariableDebtToken.spec:89–99`, definição `:23–29` | `f` também permite mint/burn e seus efeitos na spec global `gRNVB` (`:13–15`), hook `sumAllBalance` `:32–38` e invariant `:40–50` (não `requireInvariant` automaticamente). Summaries `:1–8` de reserve index, balance e `handleAction` podem alterar trajetórias chamadas por `f`. | Não tratar como clone semântico de 41: target é VariableDebtToken e `burn` tem ABI distinta. Poda por revert, receiver e impacto indireto de summaries ainda pendentes. |
| **36** `integrityTimeStamp` | `StableDebtToken.spec:166–174`, `N.spec` definição `:14–20` | `getUserLastUpdated(address)` existe e lê `_timestamps[user]` em `StableDebtToken.sol:91–93`. A rule assume timestamp pré-call `<= e.block.timestamp`, chama `f(e,arg)` sem `@withrevert`, e faz assert com o mesmo `e.block.timestamp`. Há seis `f` não-view elegíveis na ABI. | Não alegar monotonicidade em qualquer histórico sem modelar `initialize`, mint/burn e efeitos do `f`; os reverts descartados são risco de vacuidade. Global methods/hooks podem alterar trajetórias. |
| **47** `disallowedFunctionalities` | `StableDebtToken.spec:338–344`, definição `:14–20` | `f@withrevert(e,args)` preserva caminhos com revert; as seis assinaturas escolhidas existem e todas têm `revert(Errors.OPERATION_NOT_SUPPORTED)` no contrato do snapshot `:365–386`. | Evidência **Solidity direta** favorece a intenção da assertion `lastReverted`, mas nenhum Prover verificou o conjunto; `sig:` e contexto de dispatch requerem migração/gate. Não reclassificar como VERIFIED ou SEMANTIC_PROVEN. |
| **73** `disallowedFunctionalities` | `VariableDebtToken.spec:252–258`, definição `:23–29` | Mesmo padrão do caso 47, porém implementações `VariableDebtToken.sol:127–148`. Todas seis funções inclusive `allowance view` lançam revert; há `@withrevert` explícito. | Não fundir targets nem equiparar snapshot com commit auditado `a87d546`; closure global, receiver/ABI histórica e prova formal ainda faltam. |

### Fronteiras semânticas

- A fonte CVL global contém `methods` e summaries sem receiver concreto, além de ghosts/hooks/invariants que não estão no `N.spec`. Para rules paramétricas 41/63/36, a ausência dos globals é especialmente perigosa: `f` pode selecionar funções de mint/burn, não apenas delegation, e acionar hooks que não ocorreriam na chamada direta de P7/37/65.
- `f@withrevert` de 47/73 é distinto de `f(e,args)` de 41/63/36. Nenhuma condição extra foi inserida para suprimir um revert ou contraexemplo. `f.selector` requer `sig:` em CVL2 segundo documentação oficial, **sem** demonstrar que a substituição é suficiente para equivalência de versões.
- O histórico de janeiro de 2022 em `aave/aave-v3-core@a87d546` seleciona specs/harnesses e flags distintos do snapshot posterior. Os cinco diagnósticos são exclusivamente `SNAPSHOT_FRAGMENT`; as specs CVL completas já falharam no checker, conforme relatório COORDINATOR. Não inferir `HISTORICAL_REPLAY`, equivalência ou garantia de não vacuidade.

**Gate solicitado ao coordenador:** evidência de runner e cena específica por target (versão, ABI, deployment, métodos elegíveis, linkings, summaries/receivers) e autorização individual antes de qualquer spec CVL2 derivada. O diagnóstico original só justifica `DOCUMENTED_CANDIDATE` de sintaxe `sig:`, não aprova edição nem novo bucket.

**Fontes:** [CVL2 Migration Guide](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [Changes Introduced in CVL2](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), docs Certora de `methods`, `statements`, `hooks` e `ghosts`. CVL e Solidity nas linhas da tabela, hashes e logs em `round5_logs`.
