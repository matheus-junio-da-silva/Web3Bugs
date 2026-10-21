# Auditoria independente de runner histórico e ABI — AAVE V3, P7/3, P7/37 e P7/65

**Data:** 2026-10-19. **Estado:** pesquisa documental com compilação **Solidity-only**; sem compilação CVL1/CVL2, sem Certora Prover e sem alteração dos arquivos históricos. **Baseline Web3Bugs:** `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Complementa [a matriz de closure previamente publicada](COORDINATOR_CLOSURE_P7_3_37_65.md).

## 1. Fontes distintas: relatório 2022 versus dataset posterior

O [relatório histórico `reports/7.md`](../../../../../reports/7.md), que reproduz o relatório Certora de AAVE V3 de janeiro de 2022, declara o commit auditado [`a87d546d57d4e49bcb450d3c46b50d6bc6e5ddee`](https://github.com/aave/aave-v3-core/tree/a87d546d57d4e49bcb450d3c46b50d6bc6e5ddee). Seu próprio cabeçalho alerta para não confundir o commit auditado com o snapshot posterior de PropertyGPT.

O repositório oficial auditado disponibiliza arquivos recuperados **no commit exato indicado no relatório**, que foram consultados diretamente pelo GitHub:

| Arquivo histórico no commit auditado | Evidência / constatação |
| --- | --- |
| [`runStableTokenCLI.sh`](https://github.com/aave/aave-v3-core/blob/a87d546d57d4e49bcb450d3c46b50d6bc6e5ddee/runStableTokenCLI.sh) | SHA blob `25a7daef12945fbd65ddd97af6f92511e10ca299`; usa `StableDebtTokenHarness`, `--solc solc6.12`, `--solc_args '--optimize'`, `--settings -assumeUnwindCond,-b=4`. |
| [`runVariableTokenCLI.sh`](https://github.com/aave/aave-v3-core/blob/a87d546d57d4e49bcb450d3c46b50d6bc6e5ddee/runVariableTokenCLI.sh) | SHA blob `6213767839b4ad7e88adf7141aba1dfa9b8779a3`; usa `PoolHarnessForVariableDebtToken`, `--link VariableDebtToken:POOL=PoolHarnessForVariableDebtToken`, `--solc solc6.12` e `-b=4,-assumeUnwindCond,-useNonLinearArithmetic`. |
| [`StableDebtTokenHarness.sol`](https://github.com/aave/aave-v3-core/blob/a87d546d57d4e49bcb450d3c46b50d6bc6e5ddee/specs/harness/StableDebtTokenHarness.sol) | Blob `69d8052fa29737b659d6f444b2c4230d3459132c`; declara `pragma solidity 0.6.12` e constructor `StableDebtToken(pool, underlyingAsset, name, symbol, incentivesController)`. |
| [`PoolHarnessForVariableDebtToken.sol`](https://github.com/aave/aave-v3-core/blob/a87d546d57d4e49bcb450d3c46b50d6bc6e5ddee/specs/harness/PoolHarnessForVariableDebtToken.sol) | Blob `c2f11c3d410cc9544ce865a144d21c2c7914e11f`; também declara `pragma solidity 0.6.12`. |
| [`specs/StableDebtToken.spec`](https://github.com/aave/aave-v3-core/blob/a87d546d57d4e49bcb450d3c46b50d6bc6e5ddee/specs/StableDebtToken.spec) | Blob `a486d335352d73d4d81495447d29be20b9916e31`; **não contém `integrityDelegationWithSig`**; apresenta regras `sinvoke` e métodos de outra revisão. |
| [`specs/VariableDebtToken.spec`](https://github.com/aave/aave-v3-core/blob/a87d546d57d4e49bcb450d3c46b50d6bc6e5ddee/specs/VariableDebtToken.spec) | Blob `cb19c8ddb62663e845c0b11cddf5144cdc7a196b`; **não contém `integrityDelegationWithSig`**, usa `using PoolHarnessForVariableDebtToken as POOL` e outra lógica de rules. |

### Incompatibilidades diretamente observáveis

1. No mesmo commit auditado, o [`StableDebtToken.sol`](https://github.com/aave/aave-v3-core/blob/a87d546d57d4e49bcb450d3c46b50d6bc6e5ddee/contracts/protocol/tokenization/StableDebtToken.sol) tem pragma `solidity 0.8.10` (blob `c8b8df3dc40634ae252f15d8801b7b9de8f15a2c`), enquanto o harness do script exige `0.6.12`. Também o [`VariableDebtToken.sol`](https://github.com/aave/aave-v3-core/blob/a87d546d57d4e49bcb450d3c46b50d6bc6e5ddee/contracts/protocol/tokenization/VariableDebtToken.sol) tem pragma `0.8.10` (blob `e31c2538327b0225c43777ebf79270a1dfe7a068`) e o runner nomeia `solc6.12`. Isto torna a **configuração textual recuperada incompatível com as fontes apontadas**, salvo transformações ou substituições históricas não demonstradas. Não se conclui que esses scripts foram efetivamente executados no job que gerou o relatório, nem se inventa adaptação de compilador.
2. Os arquivos de origem **do snapshot posterior** têm blobs diferentes: StableDebtToken `666676ea0ba160556683b88c5fd7337b44f5bb2c`, VariableDebtToken `fd935f182b4a76fa1463f5ce87375b233e2f6482`, AToken `f613b66619a03874ece83d086d6fe79198e70fd0`. As specs do snapshot também diferem das specs auditadas: StableDebtToken `fbff132d9b033fac51db9585026ae089eb2ce166`, VariableDebtToken `89afd41f9732ef3c8f487e46059a8f1154f8e013`.
3. Por conseguinte, o resultado VERIFIED de janeiro/2022 **não pode ser atribuído automaticamente** a `P7/complete/37` ou `65`, ainda que contratos e nomes gerais se pareçam. Seus dossiês já registram `NOT_STATED` para resultados individuais, o que permanece correto. A ausência da rule nas specs do commit auditado é evidência forte de que esses dois exemplos **não** foram verificados ali sob esse nome.

## 2. Compilação estática independente de Solidity no snapshot

Executada numa área temporária **fora do repositório**, `/tmp/cvl2_p7_abi_static_20261019/`, utilizando o compilador nativo `/home/mat/.solc-select/artifacts/solc-0.8.10/solc-0.8.10` (`solc 0.8.10+commit.fc410830.Linux.g++`). Para cada target, comando com `--base-path`, `--allow-paths`, `--abi`, `--overwrite`, `--output-dir` e timeout de 28 segundos. **Todos retornaram exit code 0**, com warnings de shadowing/nome, sem erros de compilação. Não se trata de compilação CVL2 nem de reprodução Certora.

| Target Solidity do snapshot | Fontes na import closure | Import edges | ABI extraída (funções) | SHA-256 do arquivo ABI gerado |
| --- | ---: | ---: | ---: | --- |
| `AToken.sol` | 21 | 42 | 34 | `6fca28b185ada4733b233b18bca90a0d8416e1870f90217053e49104d90db2de` |
| `StableDebtToken.sol` | 20 | 36 | 33 | `ca90069b8ded4fc0bd8b9e2ce2ab01a16354ad2f3f10892284f212c915b895ce` |
| `VariableDebtToken.sol` | 22 | 44 | 30 | `290cb7e7169196614739feb89a7324e8937847300de809b29941fb9622552ab3` |

Os imports acima são **arestas Solidity relativas**, sem caminhos ausentes no snapshot; não demonstram que um driver Certora seleciona os mesmos contratos, a mesma inicialização ou os mesmos linkings.

**ABIs efetivamente observadas:**
- AToken: `mint(address,address,uint256,uint256)` external ABI, `nonces(address) returns(uint256)` view; não expõe `handleAction` na sua ABI. A implementação chama externamente `IAaveIncentivesController.handleAction`, que não é função do próprio AToken.
- StableDebtToken e VariableDebtToken: ambas expõem separadamente `delegationWithSig(address,address,uint256,uint256,uint8,bytes32,bytes32)` (nonpayable), `nonces(address)` (view, `uint256`) e `borrowAllowance(address,address)` (view, `uint256`). Funções herdadas de `DebtTokenBase` e `EIP712Base`; **não são getters reconstruídos artificialmente**.
- Mesmo com ABIs equivalentes dessas três operações, os targets diferem no construtor, em métodos adicionais e na implementação econômica. Nunca deduplicar as duas regras P7/37 e P7/65.

As compilações e ABIs acima referem-se **exclusivamente ao código do snapshot**; não demonstram nem a ABI final do commit auditado nem a execução de nenhum job histórico.

## 3. Risco de vacuidade e ecrecover

O caminho de `DebtTokenBase.delegationWithSig` verifica `delegator!=0`, `block.timestamp<=deadline` e `delegator==ecrecover(digest,v,r,s)`; atualiza `_nonces` e `_borrowAllowances` **somente se todas as condições e os checks de aritmética forem satisfeitos**. Também pode reverter quando `_nonces[delegator]==2^256-1` por overflow do incremento em Solidity 0.8.10.

A [documentação oficial de statements CVL](https://docs.certora.com/en/latest/docs/cvl/statements.html) estabelece que chamadas não anotadas com `@withrevert` descartam os caminhos de revert. Portanto, uma rule `integrityDelegationWithSig` com essa chamada pode terminar `VERIFIED` por vacuidade caso a condição de assinatura nunca seja satisfeita no modelo — **a satisfatibilidade ainda não foi testada**, não é permitido dizer que houve uma prova vacuamente verdadeira. A [documentação oficial de `ecrecover` no CVL](https://docs.certora.com/en/latest/docs/cvl/expr.html#ecrecover) descreve uma modelagem por ghost; esse texto não prova, isoladamente, como o precompile Solidity foi modelado no job auditado.

Não adicionar precondições `require`, não supor que existem assinaturas válidas simbolicamente, nem converter reversões em violações automaticamente. Para avançar, seria preciso uma cena documentada e uma verificação de reachability/satisfatibilidade **especificamente autorizada**, não simplesmente confiar no typechecker.

## 4. Adjudicação de gate

- **P7/3:** permanece bloqueado para compilação contextual pela necessidade de preservar hook Sstore da `_userState.balance`, summary de `IAaveIncentivesController.handleAction` e contrato `SimpleERC20` secundário não recuperado.
- **P7/37 e P7/65:** ABI **do snapshot confirmada por `solc 0.8.10`** e Solidity import closure local confirmada, mas **runner histórico não reproduzível com os artefatos antigos encontrados**. O par de scripts do commit 2022 está ligado a specs diferentes e possui incompatibilidade de pragmas de harness/solc. A cena histórica, seus efeitos do `ecrecover` e a possibilidade de vacuidade continuam sem prova.
- **Sem promoção** a `00_unchanged` final, `01_documented` ou verificação formal; nenhuma cópia CVL2 nova. A conclusão desta fase é **progresso de reconstrução documentada**, não prova de incompatibilidade definitiva.
- Antes de qualquer piloto CVL2, precisaríamos fixar um cenário de **snapshot-only**, separado explicitamente do job auditado 2022, com configurações mínimas reproduzíveis e sem alterar regras. O primeiro experimento, se autorizado, deveria ser `--compilation_steps_only` individual, **não Prover**, e nunca chamado de repetição da auditoria histórica.

**Observação:** todos os resultados históricos e rótulos do CSV continuam intocados, inclusive `NOT_STATED` dos exemplos 37 e 65. A documentação preserva a lacuna entre a spec do relatório 2022 e os exemplos PropertyGPT posteriores.
