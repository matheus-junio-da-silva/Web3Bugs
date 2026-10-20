# Contrarrevisão independente do coordenador — P7 / complete / {3,37,65}

**Data:** 2026-10-19. **Escopo:** pesquisa documental e inspeção estática **sem compilar CVL1/CVL2, sem Prover, sem editar originais**. Branch de pesquisa: `research/cvl2-agente-05`, baseline `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`, PR [#40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40).

## Fontes e verificações independentes

Li o protocolo `docs/spec_catalog.md`, `docs/spec_catalog_workflow.md`, `docs/spec_catalog_project_1.md`, `docs/standard.md`; as `N.spec` históricas `results/spec/complete/7/{3,37,65}.spec`; suas três rules integrais nas fontes `contracts/7/specs/{AToken,StableDebtToken,VariableDebtToken}.spec`; os respectivos dossiês AGENTE-05; e os contratos de `contracts/7/contracts/protocol/tokenization/`, suas bases herdadas e interfaces.

A análise de **imports Solidity** por caminhamento textual transitivo com Python, a partir de cada target na árvore do snapshot, contou: AToken **21** arquivos/42 arestas, StableDebtToken **20**/36, VariableDebtToken **22**/44, **zero caminhos relativos ausentes**. Isso é somente disponibilidade de arquivos: **não é build, não verifica remappings, versão efetivamente compilada, ABI pós-patch, bibliotecas linkadas nem identidade do run de auditoria**. Os contratos consultados declaram `pragma solidity ^0.8.10`; não foi recuperado `.conf` ou driver histórico individual em `contracts/7/`. Nenhum `SimpleERC20` Solidity foi localizado no snapshot de P7, apesar de `AToken.spec:7` conter `using SimpleERC20 as _underlyingAsset`; a necessidade dessa instância de cena para a rule P7/3 ainda precisa de pesquisa de config/scene.

Validação estrutural executada **independentemente** na worktree limpa `/home/mat/cvl2-agent05-isolated/Web3Bugs`: `check_specs.py` EXIT 0 (1.386 examples e 1.390 relações), `check_contests_csv.py` EXIT 0, `check_contracts.py` EXIT 0 e `git -c core.whitespace=cr-at-eol diff --check 2a03637...HEAD` EXIT 0. Nada foi alterado localmente. A amostra de três examples não equivale a auditoria semântica integral do Projeto 7.

## Matriz de closure por rule

| Item CVL global / dependência | P7 complete/3 — AToken | P7 complete/37 — StableDebtToken | P7 complete/65 — VariableDebtToken |
| --- | --- | --- | --- |
| Rule / operação | `mintArgsPositive`: `mint@withrevert(...)`; assertion `amount==0 => lastReverted` | `integrityDelegationWithSig`: `nonces`; `delegationWithSig`; `borrowAllowance` | Mesma rule textual que 37, mas outro target e `VariableDebtToken.spec` distinta |
| Função-alvo | `AToken.sol:86-93` → `ScaledBalanceTokenBase.sol:66-88` → `MintableIncentivizedERC20.sol:35-45` | `DebtTokenBase.sol:43-68` | Mesma base `DebtTokenBase.sol:43-68` |
| `onlyPool` | **DIRETO**, no `mint` e `IncentivizedERC20.sol:34-39`; assinatura da chamada pode reverter por caller, independentemente de amount | Não identificado nessa função | Não identificado nessa função |
| `methods` relevantes | `AToken.spec:12`: `handleAction(...)= > NONDET` é **POTENCIALMENTE RELEVANTE** para `_mint` via incentives controller condicional; escolher receiver CVL2 baseado na ABI é obrigatório | `StableDebtToken.spec:1-9` contém summaries para `calculateCompoundedInterest`, `rayMul`, `rayDiv`; **SEM CHAMADA IDENTIFICADA** no caminho direto `delegationWithSig`, não assumir irrelevância da cena inteira | `VariableDebtToken.spec:1-8` contém summary de `getReserveNormalizedVariableDebt` e `handleAction`; **SEM CHAMADA IDENTIFICADA** na delegação |
| `Sstore` e ghost de balanço | `AToken.spec:32-43` e `MintableIncentivizedERC20.sol:39-40`: hook sobre `_userState[].balance` **ATINGÍVEL** quando mint bem-sucedido; omissão não é comprovadamente neutra | `StableDebtToken.spec:114-123`: hooks de Sstore/Sload em balance; caminho direto escreve `_nonces` e `_borrowAllowances`, **nenhum balance Sstore/Sload identificado** | `VariableDebtToken.spec:32-38`: hook balance não identificado no caminho direto que escreve nonces/allowances |
| `ghost` e axiomas | `gRNI` e `sumAllBalance` aparecem na spec; `init_state axiom` **não é uma precondição automática da rule** (veja documentação Ghosts) | `symbolicCompundInterest` tem axiom, mas nenhuma referência na rule direta identificada; `sumAllBalance` tem init_state axiom | `gRNVB` tem axiom global, mas nenhuma referência no caminho direto identificada; `sumAllBalance` tem init_state axiom |
| `invariant` e preserved | `AToken.spec:45-55`; **não automaticamente `requireInvariant` da rule P7/3**; ainda podem impor exigências sintáticas numa compilação da spec inteira | `principalLessThanBalance` em `StableDebtToken.spec:130-132`, independente da rule salvo referência explícita; invariants não são premissas automáticas | `totalSupplyEqualsSumAllBalance` em `VariableDebtToken.spec:40-50`, idem |
| `using` / contrato adicional | `AToken.spec:7` declara `SimpleERC20`, ausência nominal da implementação no snapshot; não há chamada direta no corpo da rule, mas cena do job não foi recuperada | Nenhum `using` na spec fonte analisada | Nenhum `using` na spec fonte analisada |
| Revert e chance de prova vazia | Usa **`@withrevert`**: precisa preservar tanto o revert por `amountScaled==0` (`ScaledBalanceTokenBase.sol:72-73`) como o revert por `onlyPool`. Assertion só exige revert se `amount==0`; **não** garante sucesso para amount não zero | Chamada CVL **SEM `@withrevert`**: reverts por deadline/delegator/assinatura inválida são podados na semântica padrão; risco de vacuidade no domínio válido **NÃO medido** | Mesmo risco, mas domínio EIP712 e estado pertencem à outra implementação concreta |
| ABI e source commit do Prover histórico | Sem runner/solc exato/scene e sem demonstração de summary equivalente em CVL2 | Sem runner/solc exato, domínio EIP712 válido e sem parâmetro da cena historicamente autenticado | Idem, com target diferente |

**Nota sobre `handleAction`:** a implementação concreta `MintableIncentivizedERC20.sol:42-45` chama `IAaveIncentivesController.handleAction(address,uint256,uint256)`, que é **external** conforme `interfaces/IAaveIncentivesController.sol:18`. O `methods` CVL1 em `AToken.spec:12` usa summary `NONDET`. A documentação oficial explica que CVL1 podia aplicar summaries por assinatura a múltiplos receivers, enquanto CVL2 usa target default; logo é necessário examinar o receiver da cena original antes de converter para `internal/external` ou `_.handleAction`. **Não há aqui autorização para tal substituição.** Summaries `NONDET` também podem ser não sound para funções não-view; manter a hipótese histórica como está, com ressalva, em vez de simplificar.

## Cadeia Solidity detalhada para as duas rules de delegação

1. `DebtTokenBase.sol:43-68` implementa `delegationWithSig` como **external** com `require(delegator != 0)`, `require(block.timestamp <= deadline)`, e `require(delegator == ecrecover(digest, v,r,s))`.
2. `EIP712Base.sol:14-17,23-25,32-45,52-69`: `_nonces` é mapping herdado; o constructor captura `block.chainid`; `DOMAIN_SEPARATOR` retorna separator cacheado ou calcula, incluindo name, version, chain ID e endereço do contrato.
3. `StableDebtToken.sol:49-67` e `VariableDebtToken.sol:43-61` fornecem inicializadores específicos que definem `_domainSeparator`. Não pressupor que o job histórico reproduzia deployment/initialization real.
4. Se a assinatura for aceita, `DebtTokenBase.sol:65-67` incrementa `_nonces[delegator]` e executa `_approveDelegation` (`DebtTokenBase.sol:84-86`), que grava `_borrowAllowances` e emite evento. `borrowAllowance` é getter external `DebtTokenBase.sol:70-76`; `nonces` é getter public `EIP712Base.sol:44-46`.
5. Como P7/37 e P7/65 chamam `delegationWithSig` **sem `@withrevert`**, a documentação de CVL [Statements/Revert](https://docs.certora.com/en/latest/docs/cvl/statements.html) diz que caminhos que revertem normalmente são descartados; não inferir que assinaturas válidas sejam alcançáveis na cena simbólica **sem um teste de satisfatibilidade**.

## Fontes semânticas oficiais consultadas

- [Certora, CVL2 Migration Guide](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html) — sintaxe/semântica de `methods`, receivers, `internal/external`.
- [Certora, The Methods Block](https://docs.certora.com/en/latest/docs/cvl/methods.html) — summaries, dispatch, visibilidade; warning para certos summaries não sound.
- [Certora, Statements (Revert)](https://docs.certora.com/en/latest/docs/cvl/statements.html) — `@withrevert`, `lastReverted` e poda de reverts em chamadas normais.
- [Certora, Hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html) — hooks de Sstore/Sload executados em operações Solidity.
- [Certora, Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html) — `init_state axiom` só no passo-base de invariant, não nas regras comuns.
- [Certora, Invariants](https://docs.certora.com/en/latest/docs/cvl/invariants.html) — invariantes só assumidos explicitamente em rules com `requireInvariant`.
- [Certora, Using Statements](https://docs.certora.com/en/latest/docs/cvl/using.html) — `using` refere-se a contrato secundário na cena.

## Adjudicação e gates

**P7/3 — BLOQUEADO PARA PILOTO DE COMPILAÇÃO CONTEXTUAL:** hook sobre balance e summary de `handleAction` são ativamente atingíveis; além disso faltam identificação do `SimpleERC20` secundário, cena/runner histórico, linkings e regras de receiver CVL2. Não migrar apenas o recorte `N.spec` como se fosse equivalente à fonte integral.

**P7/37 e P7/65 — CANDIDATOS DE PESQUISA MAIS DELIMITADOS**, porque a call path herdada delega EIP712/nonces/allowance, sem referência identificada a balance hooks ou summaries de juros. Mas **não autorizar ainda compile-only** como reprodução fiel: comprovar target, ambiente/flags, domínio EIP712 e papel de elementos CVL globais no compilador. Os dois têm nome idêntico, porém targets de Solidity distintos; nunca fundir, deduplicar ou assumir resultados iguais.

**Nenhuma mudança automática em `results/cvl2`; nenhum novo `00_unchanged`; nenhum teste CVL1, Prover ou compilação CVL2 foi executado para P7 nesta análise.** As três candidaturas continuam provisórias. Fontes não encontradas no snapshot não são prova de inexistência fora dele.

**Condição de avanço:** (i) provar o runner/target e o escopo de globals necessário; (ii) definir a cena Solidity histórica sem trocar implementações; (iii) autorizar por escrito um piloto compilação-only de no máximo uma rule por target, **mantendo os bytes originais**; (iv) separar resultados de compilação de equivalência semântica. Se estas etapas permanecerem insupríveis, registrar bloqueio e explorar outros projetos com contexto mais fechado.
