# AGENTE-05 — Rodada 6: `sig:`, domínios de `method f`, reverts e contexto integral P7

**Escopo:** Projetos AAVE V3 P7/complete/47,73,41,63,36, confrontados com N.spec, specs CVL integrais, ABIs do snapshot solc 0.8.10 e Solidity herdado. Não há alteração em originais, `require`, `assert`, `ghost`, `hook`, cast, methods nem summary. Baseline imutável `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.

## Evidência de execução delimitada

- **Rodada 5 — efetivamente executado (não reexecutado R6):** cinco N.spec originais P7/36,41,47,63,73, CLI direto Certora 8.19.0, `--compilation_steps_only`, solc 0.8.10, cópias byte-idênticas, timeout 65 s: **EXIT 1** em todos, pela sintaxe CVL1 de literais sem `sig:`. A evidência primária continua em `7/round5_logs/ROUND5_COMMAND_MANIFEST.json` e nos stdout/stderr `.gz`, com hashes. O autofinder StableDebtToken também informou `Stack too deep` e fallback; a falha atribuída ao CVL2 é a da tipagem do literal.
- **P7/37,65 — prova anterior do coordenador:** dois recortes originais isolados **EXIT 0** no CVL2; **ambas** as specs CVL completas falharam em CVL2. Sem equivalência, sem replay 2022. P19/1,2 foram derivadas `mathint` em #46, não experiências P7.
- **Rodada 6 — proposta única de variante:** apenas P7/47 no scratch, **não houve execução de CLI** devido erro ambiental no WSL: a preparação foi interrompida inicialmente por uma asserção do script de controle que comparava uma ocorrência do nome da rule no comentário do header; ao tentar corrigir em scratch, o host passou a retornar Python `SIGBUS` (exit 135), `df: Input/output error` e escrita `EROFS`. O código do `certoraRun` não foi iniciado para essa variante. Etiqueta **`NOT_RUN_ENVIRONMENT_IO_BLOCKED`**, **não** COMPILE_ERROR/CVL2 nem PREFLIGHT_AUTH_BLOCKED. Falha de preparação não é resultado do typechecker.

## Proposta de diff `sig:` SOMENTE documental — P7/47

Trecho preservado `results/spec/complete/7/47.spec:6–12`, originário de `contracts/7/specs/StableDebtToken.spec:14–20`, assinatura `disAllowedFunctions(method f)`. A proposta insere **exatamente** `sig:` diante dos seis literais de método no lado direito de `f.selector ==`:

```diff
- f.selector == transfer(address, uint256).selector ||
+ f.selector == sig:transfer(address, uint256).selector ||
- f.selector == allowance(address, address).selector ||
+ f.selector == sig:allowance(address, address).selector ||
- f.selector == approve(address, uint256).selector ||
+ f.selector == sig:approve(address, uint256).selector ||
- f.selector == transferFrom(address, address, uint256).selector ||
+ f.selector == sig:transferFrom(address, address, uint256).selector ||
- f.selector == increaseAllowance(address, uint256).selector ||
+ f.selector == sig:increaseAllowance(address, uint256).selector ||
- f.selector == decreaseAllowance(address, uint256).selector;
+ f.selector == sig:decreaseAllowance(address, uint256).selector;
```

O corpo da rule `disallowedFunctionalities` (`StableDebtToken.spec:338–344`) fica **inteiramente intocado**, incluindo `f@withrevert(e,args)` e `assert lastReverted`. Nada é modificado ou publicado em `results/cvl2/`; não foi produzido artefato derivado compilado. O guia Certora [Changes CVL2 § Method literals require `sig:`](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html) documenta a substituição lexical, **não** a preservação do universo de `method f`, da cena, dos summaries, dos hooks ou de contraexemplos.

## Fonte/linha, ABI e risco por ID

| ID | Fonte CVL e predicado original | ABI Solidity snapshot / caminho | Semântica e risco restante |
| --- | --- | --- | --- |
| **P7/47** Stable `disallowedFunctionalities` | `StableDebtToken.spec:14–20,338–344`; `N.spec:6–21`. Filtro `f -> disAllowedFunctions(f)`; chamada **`f@withrevert(e,args)`**, assert `lastReverted`. | `StableDebtToken.sol:365–386`: os seis selectors listados existem e cada função reverte incondicionalmente com `Errors.OPERATION_NOT_SUPPORTED`. `allowance(address,address)` é `view`, mas **não** excluída pelo filtro. ABI `StableDebtToken.abi` gerada na R5 possui 33 funções. | Se o conjunto concreto de selectors matching e o dispatch CVL refletirem essa ABI, a conclusão é sustentada pelo Solidity **para esses seis caminhos**, mas `method f` não teve satisfatibilidade/coverage provada. Sob `@withrevert` os caminhos revertidos **não são podados**. `COMPILE_ERROR` original por sintaxe, sem prova de não-vacuidade/proof result. |
| **P7/73** Variable `disallowedFunctionalities` | `VariableDebtToken.spec:23–29,252–258`; filtro e `f@withrevert` análogos, target **distinto**. | `VariableDebtToken.sol:127–148`: seis selectors ABI reais e seis reverts incondicionais; `allowance` view também reverte. ABI Variable tem 30 funções. | Sem extrapolar resultado do target Stable: ABI, imports, dispatch, hierarquia, hook e run independentes. Não exclua um método view da rule que não contém `!f.isView`. |
| **P7/41** Stable `nonceChangePermits` | `StableDebtToken.spec:14–20,226–236`, `f -> !f.isView && !disAllowedFunctions(f)`. Lê `nonces(e,user)` antes/depois de `f(e,args)`. Se variar, exige selector de `delegationWithSig`. | Seis assinaturas não-view não excluídas na ABI snapshot: `approveDelegation`, `burn(address,uint256)`, `delegationWithSig`, `initialize`, `mint`, `setIncentivesController`. `DebtTokenBase.sol:43–68` atualiza nonce **após** `deadline`, digest EIP-712 e `ecrecover` válidos. | `f(e,args)` **sem** `@withrevert` poda chamadas revertidas; não assumir que a premissa permite assinatura EIP-712 válida. `mint/burn` também alcançam balanço e podem disparar hooks Sstore/Sload e summaries globais. Se nonce não muda, antecedente do assert é falso (possível vacuidade da implicação). |
| **P7/63** Variable `nonceChangePermits` | `VariableDebtToken.spec:23–29,89–99` com mesmo formato do assert. | As seis funções não-view não excluídas existem, mas `burn(address,uint256,uint256)` é diferente da Stable; `DebtTokenBase` compartilha a lógica de assinatura, com implantação/índice diferentes. | Hook Sstore `_userState.balance` e ghost `sumAllBalance` (`VariableDebtToken.spec:32–38`) podem ser relevantes a `f=mint/burn`; `gRNVB` e summaries globais não são extraídos. Não fundir os dois targets. |
| **P7/36** Stable `integrityTimeStamp` | `StableDebtToken.spec:14–20,166–174`; requer `getUserLastUpdated(e,user) <= e.block.timestamp`, chama `f(e,arg)` sem `@withrevert` e reafirma a desigualdade. | `StableDebtToken.sol:91–93` lê `_timestamps[user]`; seis não-view elegíveis, incluindo mint/burn/initialize e delegation. | Revert pruning, `onlyPool` e inicialização podem tornar parte do domínio inatingível. A `require` anterior permanece inalterada. Timestamp e hooks/summaries não têm semântica provada em recorte. |

**Atenção sobre contagem ABI:** a extração Solidity-only R5 registrou `StableDebtToken.abi` SHA-256 `ca90069b8ded4fc0bd8b9e2ce2ab01a16354ad2f3f10892284f212c915b895ce` (33 funções) e `VariableDebtToken.abi` SHA-256 `290cb7e7169196614739feb89a7324e8937847300de809b29941fb9622552ab3` (30). Os seis `disAllowed` são **existência estática** de métodos, não demonstrativo de quantificação CVL, seleção de métodos, alcance simbólico, contrato deployed, EIP-712, nem prova histórica.

## Global CVL omitido por N.spec e condições para novo gate

As specs integrais possuem `methods` legados, summaries de `handleAction` e matemática (`calculateCompoundedInterest/rayMul/rayDiv` na Stable; `getReserveNormalizedVariableDebt`, `handleAction` e balance na Variable), ghosts/axioms, hooks sobre `_userState.balance`, e invariants. Uma rule **paramétrica** pode atingir mint/burn e a instrumentação global mesmo quando uma rule direta `delegationWithSig` não a atinge. `init_state axiom` não se torna `require` automático de uma rule comum; invariantes também não viram `requireInvariant` sem referência. Para a regra com `@withrevert`, o número de métodos na ABI não é por si só certificado de que a regra foi instanciada.

**Gate individual requerido:** depois de restaurado o ambiente, executar *somente se coordenador permitir* o candidato sintático de P7/47 como variante temporária, com hash diff limitado aos seis `sig:`, target StableDebtToken, CLI 8.19.0, solc 0.8.10, `--compilation_steps_only` e timeout, sem credenciais. Even if this compiles, preserve `DOCUMENTED_CANDIDATE` until ABI exata histórica, globals, receivers, method-f satisfiability e regras de revert forem adjudicados. Não extrapolar para P7/73 ou para P7/41,63,36 sem gates separados.

Documentação consultada: [Certora Migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [Methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [Hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html), [Statements e `@withrevert`](https://docs.certora.com/en/latest/docs/cvl/statements.html).
