# AGENTE-05 — Rodada 4: pertinência dos globals P7/37 e P7/65

Data: 2026-10-20. Baseline: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
Escopo: inspeção independente das fontes integrais preservadas, do caminho Solidity e das evidências de compilação de 2026-10-19. Nenhuma spec CVL1/CVL2 foi alterada. Sem Prover nem execução CVL1.

## Distinção obrigatória de resultados

- `results/spec/complete/7/37.spec` / `StableDebtToken` e `65.spec` / `VariableDebtToken` **compilaram apenas como fragmentos** em CVL2 CLI 8.19.0, `--compilation_steps_only`, conforme `COORDINATOR_CVL2_COMPILATION_DIAGNOSTIC_P7.md`. Hashes dos recortes: `f31e464ce0d28c1ea71dafde572d9b83cf6d82826ebdcb02c3d493e9016edbbd` e `ce1539d8bab260852c124f54df56cd78f7758bfc0a26b4c35c912084281c2fe9`.
- `contracts/7/specs/{StableDebtToken,VariableDebtToken}.spec` integrais **falharam em CVL2**, exit 1. O parser/typechecker registrou métodos sem `function` e `;`, hooks `STORAGE` antigos, expressão `if (x==0) || (y==0)` na Stable e `invoke burn(...)` na Variable. Isso não é evidência de que o conjunto de mudanças esteja completo.
- Na Stable, o autofinder auxiliar emitia `Stack too deep` e recorria ao arquivo original; o resultado final ainda foi exit 0 **do fragmento**. Esse fallback é parte obrigatória da interpretação, não erro da rule ou compilação integral.
- Nenhuma tentativa nova de compilação foi realizada nesta rodada. Os resultados citados são evidência pré-existente do coordenador, não execução independente do agente.

## Blocos da spec StableDebtToken original — original source e efeito

| Linhas | Bloco | Pertinência à execução P7/37 | Conclusão conservadora |
| --- | --- | --- | --- |
| 1–10 | `methods`: `calculateCompoundedInterest`, `additionalData`, `getAverageStableRate`, `handleAction`, `rayMul`, `rayDiv` | Sem referência direta no corpo da rule 176–181. Caminho `DebtTokenBase.delegationWithSig` não chama juros, incentivos nem ray math. | **Ausência de pertinência direta demonstrada**, não irrelevância universal: a cena/dispatch pode afetar chamadas indiretas e a tipagem da spec integral. Receivers/internal/external e política wildcard não foram autenticados. |
| 12 | `definition RAY` | Sem uso direto na rule; usada em summaries matemáticos. | Sem dependência direta identificada no caminho de delegação. |
| 14–20 | `definition disAllowedFunctions` | Rule P7/37 não possui parâmetro `method f`/filtered e não chama a definição. | Irrelevância lexical **para o predicado extraído** demonstrada, não licença para eliminar do programa integral de verificação. |
| 22–103 | Ghost mappings e summaries `calculateCompoundedInterestSummary`, `rayMulSummariztion`, `rayDivSummariztion` | Sem uso direto. `rayMulSummariztion` linha 47 tem sintaxe CVL1 rejeitada no teste integral. | Sem efeitos no caminho direto de delegation reconhecidos, mas dependem dos summaries globais para outros caminhos e afetam possibilidade de compilação. |
| 106–108 | `symbolicCompundInterest` + axiom | Não referenciado em delegation/nonces/borrowAllowance. | Axiom não equivale automaticamente a `require` desta rule; distinguir condições globais do ghost de precondições locais. |
| 114–123 | `sumAllBalance` + `init_state axiom`; hooks Sstore/Sload em `_userState[].balance` | `delegationWithSig` escreve `_nonces` e `_borrowAllowances`, não `_userState.balance` em caminho observado. | Não há trigger direto de hook de balanço na transição examinada; isso **não prova** que toda instrumentação ou cena seja independente. |
| 130–132 | `principalLessThanBalance` e filtered | Rule não invoca `requireInvariant` nem essas variáveis. | Não é premissa automática da regra; sua sintaxe ainda integra build da spec completa. |
| 176–181 | Rule `integrityDelegationWithSig` | Chama `nonces(e,delegator)`, `delegationWithSig`, `borrowAllowance`. | Dependência Solidity direta nas funções herdadas de `EIP712Base` e `DebtTokenBase`. |

## Blocos da spec VariableDebtToken original

| Linhas | Bloco | Pertinência à execução P7/65 | Conclusão conservadora |
| --- | --- | --- | --- |
| 1–8 | `methods`: `getReserveNormalizedVariableDebt`, `setAdditionalData`, `handleAction`, `scaledBalanceOfToBalanceOf`, `balanceOf` | Rule 111–116 não chama essas funções e o caminho observado em `DebtTokenBase` não acessa pool, scaled balance ou incentives. | Não identificado uso direto. Não converter summaries para `currentContract` nem wildcard sem provar receiver e política, pois são requisitos de cena e syntax-check da spec integral. |
| 10–19 | `ray`, `bound`, `bounded_error_eq`, ghost `gRNVB` com axiom | Nenhuma referência no predicado `integrityDelegationWithSig`. | Sem dependência lexical direta; podem ser essenciais a outras rules. |
| 23–29 | `disAllowedFunctions` | Nenhuma chamada ou filtro na rule 65. | Não é dependência direta do fragmento, mas continua na spec integral. |
| 32–38 | `sumAllBalance` init_state e hook Sstore de `_userState[].balance` | O caminho de assinatura altera nonce e borrow allowance, sem gravação de `_userState.balance` identificada. | Sem acionamento direto de hook; a ausência de hook no fragmento não autoriza conclusão geral de equivalência. |
| 40–50 | `totalSupplyEqualsSumAllBalance` + preserved mint/burn | Não invocada pela rule, sem `requireInvariant`. | Não é precondição automática da rule. |
| 111–116 | Rule `integrityDelegationWithSig` | Mesmo texto assertivo de 37, porém outro target/construtor. | Preservar identidades distintas, aliases e cenário Solidity. |

## EIP-712, inicialização e execução real

1. No snapshot, `contracts/7/contracts/protocol/tokenization/base/DebtTokenBase.sol:43–68` testa `delegator != 0`, `block.timestamp <= deadline`, constrói digest EIP-712 com `DOMAIN_SEPARATOR()`, obtém `ecrecover` e exige assinatura correspondente. Só então grava `_nonces[delegator] = currentValidNonce+1` e `_borrowAllowances[delegator][delegatee]=value` (`_approveDelegation`, linhas 84–86).
2. `EIP712Base` computa o domínio com nome/versão, `chainid` e endereço do contrato; a construção/cache de `_domainSeparator` depende de inicialização. Stable e Variable possuem inicializadores distintos. Ausência de configuração de implantação e run completo impede atribuir o mesmo domínio a ambas.
3. Riscos de revert incluem `delegator == 0`, deadline expirado, `ecrecover` inválido, overflow no incremento de nonce sob Solidity 0.8.10. A chamada CVL não utiliza `@withrevert`; portanto execução revertida é descartada por padrão. Uma assert post-call pode parecer verdadeira se não houver caminhos de sucesso. **Vacuity é risco, não observação de Prover**.
4. O literal `oldNonce + 1` na asserção usa aritmética da spec, enquanto o contrato usa incremento Solidity 0.8.10. Para executar o `assert`, já houve sucesso (logo overflow não ocorre), mas isso não estabelece fidelidade geral CVL1↔CVL2 de casts, estados ou desdobramento de `ecrecover`.
5. ABI estática do snapshot foi gerada com solc 0.8.10: `delegationWithSig(address,address,uint256,uint256,uint8,bytes32,bytes32)`, `nonces(address)` e `borrowAllowance(address,address)` são alcançáveis por ambas as instâncias. ABI e closure locais não autenticam flags/links da execução original.

## Runner auditado vs cenário reprodutível

O relatório de janeiro de 2022 refere-se a `aave/aave-v3-core@a87d546d57d4e49bcb450d3c46b50d6bc6e5ddee`, que **não contém estas duas rules** nas specs Stable/Variable daquela revisão. Scripts históricos `runStableTokenCLI.sh` e `runVariableTokenCLI.sh` usam harnesses de pragma 0.6.12 e `solc6.12`, enquanto fontes do commit/árvore examinados exigem Solidity 0.8.10. Ausentes as transformações executadas no job. O melhor cenário **observado** é, portanto, o snapshot isolado, target Solidity efetivo, solc 0.8.10 e `--compilation_steps_only` em cada N.spec original; **não** é replay 2022, não é equivalência.

## P7/3 como controle negativo

Em `AToken.spec:7,12,32–43` há `using SimpleERC20 as _underlyingAsset`, `handleAction(...)= > NONDET` e hook Sstore de balance. `AToken.mint` → `_mintScaled` → `MintableIncentivizedERC20._mint` atinge Sstore e pode chamar `IAaveIncentivesController.handleAction`. Logo P7/3 não serve como exemplo de global irrelevante. Faltam a implementação secundária SimpleERC20 e a política autenticada de receiver/summary para chamadas externas ligadas. A assertion `amount==0 => lastReverted` não promete sucesso para amount não zero; `onlyPool` também pode reverter.

## Decisão independente

P7/37 e P7/65: `SNAPSHOT_FRAGMENT_CVL2_COMPILE_OK` **sem promoção** de `00_unchanged`; contextuais `02_unresolved` para eventual derivada. P7/3: bloqueio contextual concreto. Sem transformar hooks, `methods`, ghosts, casts, `require` ou `assert`; sem declarar `VERIFIED`, `VIOLATED` ou ausência de vacuity.

Fontes: `COORDINATOR_CLOSURE_P7_3_37_65.md`, `COORDINATOR_HISTORICAL_RUNNER_AND_ABI_P7.md`, `COORDINATOR_CVL2_COMPILATION_DIAGNOSTIC_P7.md`; [CVL2 Migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [Methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [Hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html), [Invariants](https://docs.certora.com/en/latest/docs/cvl/invariants.html), [Statements](https://docs.certora.com/en/latest/docs/cvl/statements.html).
