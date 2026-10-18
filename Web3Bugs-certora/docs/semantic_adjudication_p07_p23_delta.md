# DELTA — adjudicação semântica dos Projects 7 e 23

Data: 2026-10-18. Base: `main` commit `80f551f23bbd86d7901c6a28e7f44c68aebae8fd`. Branch exclusiva: `fix/semantic-p07-p23-delta`.

## Método e natureza da mudança

Comparação direta dos oito corpos CVL selecionados, suas dependências incluídas no `N.spec`, correspondentes snippets e implementações Solidity originais sob `contracts/7` e `contracts/23`, documentação de catalogação e taxonomia de `docs/standard.md`. Os `N.md` recebem análise individual; o CSV `results/spec/spec_buglabel.csv` e as matrizes de documentação dos Projects 7 e 23 foram reconciliados. **Não se altera property CVL, Solidity, PDF, resultado histórico ou detection outcome.** A disponibilidade de símbolos do snapshot não é reprodução do Prover, e a presença de Solidity contextual não substitui os wrappers CVT ausentes do Radicle.

Categorias pertinentes de `standard.md`: `S3-1` = falta de atualização de estado, `S3-2` = atualização de estado incorreta, `S5-2` = invocação de função em um momento/contexto que não deveria ser permitido, `S6-2` = valor retornado inesperado, `S6-4` = outros erros de accounting, `L8` = revert **causado por low-level call ou biblioteca externa**, `SC` = peculiaridade do contrato não enquadrável nas demais classes. `NOT_STATED` não implica sucesso e `VERIFIED` histórico não é novo replay.

## Matriz de decisões

| Project / Exemplo | Assertion e precondições efetivas | Solidity / storage / contraexemplo lógico | Label anterior → decidido | Resultado / outcome | Decisão |
| --- | --- | --- | --- | --- | --- |
| 7 / #6 AToken `additiveMint` | `require(balanceOf(a)==balanceOf(b) && a!=b)`; `mint(a,x)`, `mint(a,y)`, depois `mint(b,x+y)`; `assert bounded_error_eq(balanceScenario1,balanceScenario2,3)`. Index `gRNI=7*ray`, env comum; `initialStorage` é comentário. | `AToken.mint`→`ScaledBalanceTokenBase._mintScaled` converte por `rayDiv`, grava `_userState[onBehalfOf].additionalData` e `_mint`. `balanceOf` faz `rayMul` do índice. Falsifica se leituras subsequentes dos dois usuários divergem além da tolerância; não pressupor universos independentes, nenhum `require(c != a/b)`. | S6-4 → **S6-4** | NOT_STATED / NOT_STATED | **Manter label; corrigir explicação** |
| 7 / #68 VariableDebtToken `additiveMint` | `require(user1!=user2 && balanceOf(user1)==balanceOf(user2))`; três **mint** sequenciais, igualdade dentro de `bound()*3`, `gRNVB=7*ray`. A string literal da assertion diz `burn is not additive` incorretamente. | `VariableDebtToken.mint` pode reduzir borrow allowance e chama `_mintScaled` (saldo escalado, índice, additionalData). Falsifica se `balanceOf(user1)` após as duas mints e `balanceOf(user2)` após terceira excedem limite; não testa burn. | S6-4 → **S6-4** | NOT_STATED / NOT_STATED | **Manter label; corrigir explicação** |
| 7 / #47 StableDebtToken `disallowedFunctionalities` | `filtered f -> disAllowedFunctions(f)`; `f@withrevert(e,args); assert lastReverted`, sem require adicional. | Se uma das seis funções ERC20 de transferência/aprovação retorna normalmente, viola a assertion. `StableDebtToken.sol:365-387` reverte `OPERATION_NOT_SUPPORTED` nos seis entrypoints; nenhum storage update é observado. | SC → **SC** (S5-2 não sustentado) | NOT_STATED / NOT_STATED | **Manter label; explicitar predicado** |
| 7 / #73 VariableDebtToken `disallowedFunctionalities` | Mesmo `filtered` e `assert lastReverted` sem caller/fase/tempo. | `VariableDebtToken.sol:127-149` tem seis entrypoints que revertem `OPERATION_NOT_SUPPORTED`. Sucesso inclusive do getter `allowance` falsifica. | SC → **SC** (S5-2 não sustentado) | NOT_STATED / NOT_STATED | **Manter label; explicitar predicado** |
| 7 / #74 Pool `getReserveNormalizedVariableDebtCheck` | `require asset != _aToken`; lê index com `calldataarg args`, lê debt por `asset`, chama `supply(asset,...)`; `assert totalDebtBefore != 0 => newIndex >= oldIndex`. `args` **não é vinculado** a `asset`; `args2` sem uso. | `Pool.supply`→`SupplyLogic.executeSupply`; `Pool.getReserveNormalizedVariableDebt`→`_reserves[asset].getNormalizedDebt()`; `ReserveLogic` lê/atualiza `variableBorrowIndex`, timestamps e juros. Contraexemplo: getter retorna índice menor após supply sob antecedente verdadeiro. Isso não isola storage write incorreta nem necessariamente mesma reserva. Missing `getCurrScaledVariableDebt` do target. | S3-2 → **S6-2** | NOT_STATED / NOT_STATED | **Corrigir label; manter incomplete** |
| 23 / #27 Splits `integrityOfCollect` | Sem requires na rule; `collect(e,userId,assetId)`; depois `collectable(e,userId,assetId)`; `assert collectableAfter == 0`. | `Splits._collect` (`185-190`) lê e faz `balance.collectable = 0` no mapping `_splitsStorage().splitsStates[userId].balances[assetId]`; `_collectable` lê esse campo. Falsifica se collect executa e o saldo collectable permanece não zero; trata-se de write ausente, não equação ampla de conservação. | S6-4 → **S3-1** | VERIFIED / NO_FINDING | **Corrigir label; manter resultado histórico individual** |
| 23 / #28 Splits `revertCharacteristicsOfCollect` | `require e.msg.sender != 0`; `require e.msg.value == 0`; `collect@withrevert`; `assert !lastReverted`. | Revert sob esse ambiente falsifica. `Splits._collect` manipula collectable e evento; CVL não demonstra revert causado por low-level call ou biblioteca externa. Target CVT histórico ausente. | L8 → **SC** | VERIFIED / NO_FINDING | **Corrigir label; sonda normativa de não-revert** |
| 23 / #46 Splits2 `revertCharacteristicsOfSplit` | `hashSplits`, `assertSplitsValid`, `setSplits`; `require splittableBefore + collectableBefore < 2^128`; primeiro `split`, depois `split@withrevert`; `assert !lastReverted`. | `_setSplits` valida receivers; `_split` confere hash, zera splittable, distribui entre receivers e credita collectable. Se a **segunda** split reverte, falsifica; nenhuma causa low-level é codificada. CVT da Splits2 ausente, não há prova histórica transferível. | L8 → **SC** | NOT_STATED / NOT_STATED | **Corrigir label; sonda específica, não mero assert sanity** |

O seletor filtrado em **ambas** as regras #47/#73 é **exatamente**: `transfer(address,uint256)`, `allowance(address,address)`, `approve(address,uint256)`, `transferFrom(address,address,uint256)`, `increaseAllowance(address,uint256)` e `decreaseAllowance(address,uint256)`. Embora a regra proíba funcionalidades a qualquer instante, não contém condições temporais/caller/autoridade requeridas para justificar especificamente **S5-2** pela definição do standard. Permanece `SC`.

## Resultados históricos que devem permanecer isolados

| Radicle | Property | Result | Detection Outcome | Limite |
| --- | --- | --- | --- | --- |
| #27 | integrityOfCollect (Splits.spec) | VERIFIED | NO_FINDING | Célula individual histórica, não replay atual |
| #28 | revertCharacteristicsOfCollect (Splits.spec) | VERIFIED | NO_FINDING | Célula individual histórica, não causalidade L8 |
| #36 | splitReceiverShouldGetMoneyUponSplit | VIOLATED | FINDING | Rounding informacional reportado |
| #38 | cannotFrontRunSplitGeneralCase | NOT_STATED | INCONCLUSIVE | Timeout; não VERIFIED |
| #39–41 | variantes restritas de cannotFrontRunSplit (Splits.spec) | VERIFIED | NO_FINDING | Cada variante tem sua própria verificação |
| #46 | revertCharacteristicsOfSplit (Splits2.spec) | NOT_STATED | NOT_STATED | Sem transferência de provas de Splits.spec |

## Limites de proveniência e de validação

P7 reporta commit histórico `a87d546`; o código de `contracts/7` é snapshot posterior. P23 reporta commit histórico `6fe9d38` e depende dos wrappers CVT internos ausentes, como documentado no catálogo. Esses fatores não autorizam mudar Result ou Outcome. Os comandos estruturais e whitespace devem ser reportados com **exit codes reais**, não inferidos pelo sucesso de gravação do GitHub. Qualquer execução CI é separada dos comandos locais requeridos.

Este documento é uma adjudicação documental reviewable; nenhum `certoraRun`, merge ou modificação de fontes históricas foi executado.
