# AGENTE-04 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS

**20/10/2026.** PR de pesquisa [#42](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/42) — `research/cvl2-agente-04`, **Draft, não mergear**. HEAD conferida antes de editar: `462b5f9d7c1cf1d756aa960ec975998b39938dda`. Baseline imutável de catálogo `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; snapshot upstream PropertyGPT `687f654c679ed45ab127b7949e2a29c8f5e491b9` (referência de proveniência; não confundir com runner histórico). Responsabilidade exclusiva P2=15, P12=26, P15=116, **157 instâncias**.

## 1. Gate de qualidade e origem

Antes da edição, lidos integralmente pelo GitHub `docs/spec_catalog.md` (blob `7211e989...`), `docs/spec_catalog_workflow.md` (blob `aa6fd641...`), `docs/spec_catalog_project_1.md` (`fd5ed877...`) e `docs/standard.md` (`df4eefcc...`). Comparados `results/spec/complete/1/1.spec` (usa methods e method f, dependências do snapshot) e `results/spec/incomplete/1/1.spec` (queue2 ausente). `complete` indica **fechamento no snapshot**, não CVL2 nem prova. Lidas a revisão de coordenação R7 mais recente em #42 e [ROUND7_DASHBOARD.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/docs/cvl2/coordination/ROUND7_DASHBOARD.md), `ROUND7_PROGRESS.csv` e `ROUND6_WSL_IO_INCIDENT.md` integrados em `main` após merge **somente do PR de coordenação #47**. Esse merge não altera autorização do PR #42.

**Reconciliação original, feita nesta rodada somente em memória via conector GitHub:** o CSV `results/spec/spec_buglabel.csv` tem **1.390 relações, 1.386 chaves**; seu blob `97e20443586540034a4c0305ce1db19b0d2f8cb5` foi confirmado idêntico no baseline e na HEAD de pesquisa. `ROUND7_MATRIX_157.csv` foi cotejado por chave contra **todas** as relações no CSV (Project ID, Status, Example ID, Property, Target Contract, Result, Detection Outcome e path N.spec): **157/157 válidas, 0 divergências**. A matriz R8 acrescenta os Bug Labels canônicos e três campos **separados** `source_or_report_fact`, `inference`, `missing_proof`. Os 157 hashes SHA-256 N.spec/source foram copiados da matriz R7 já auditada, **sem novo cálculo de hash** de todos os bytes nesta rodada.

**Painel GLOBAL R7 (não são execuções AG04):** 4 `COMPILE_OK` restritos / 12 `COMPILE_ERROR` / 1.370 sem execução CVL2 / 0 equivalências / 0 projetos migrados. **AG04:** 0 OK, 3 erros observados anteriores, 154 NOT_RUN, 0 casos semanticamente provados. A Rodada 8 executou **ZERO** compile-only, Prover, CVL1, solc ou testes no WSL.

## 2. P15/incomplete/36 — prova de correspondência ABI, receiver e mutabilidade

**Sources Git SHA40/linhas:** [aave/gho-core@ce49fb0c94cfebf0159222ceb288e4f9a55d305f](https://github.com/aave/gho-core/tree/ce49fb0c94cfebf0159222ceb288e4f9a55d305f):
- `certora/harness/GhoDiscountRateStrategyHarness.sol` L1–9, **blob Git** `d652c32bcd6b34d072cec0048baafbf305061e56`: herda strategy, importa WadRayMath; `wadMul(uint256,uint256)` implementado no próprio harness como **external view** que executa uma chamada de biblioteca Solidity.
- `src/contracts/facilitators/aave/interestStrategy/GhoDiscountRateStrategy.sol` L12–54, blob `3998efa11f622bc52c50a50f580a952a044f3e3c`: `calculateDiscountRate(uint256,uint256)` **external pure**, quatro `public constant` com getters; math via `WadRayMath.wadMul`, condições de limites e cálculo final.
- `certora/specs/ghoDiscountRateStrategy.spec` L1–91, blob `809aed55ed67807a88544a3375868ef460bdf641`: **6 methods envfree**, 2 CVL helper functions, **5 regras ativas**. N.spec `results/spec/incomplete/15/36.spec`: **6 métodos + 1 regra**, fonte catalogada `contracts/15/ghoDiscountRateStrategy.spec`; rule `limitOnDiscountRate` invoca somente duas entries.
- `certora/scripts/verifyGhoDiscountRateStrategy.sh` L3–20, blob `2af609c05d5d03516b39a90c609a462ec63c7d8d`: verifica target **GhoDiscountRateStrategyHarness** (e não somente a target nominal GhoDiscountRateStrategy do CSV), `--solc solc8.10`, `--loop_iter 2`, `--optimistic_loop`, `--settings -t=500,-mediumTimeout=20,-depth=10`, `--cloud`. **Esses flags históricos não foram usados para executar Prover nesta rodada.**

| Entrada CVL1 exatamente da N.spec | ABI SOLC 0.8.10 já extraída na R5 | Declaração Solidity / contrato definidor | Chamada da regra `limitOnDiscountRate` | Hipótese de tratamento CVL2 — NÃO aprovada |
| --- | --- | --- | --- | --- |
| `calculateDiscountRate(uint256,uint256) returns(uint256) envfree` | external **pure** | GhoDiscountRateStrategy (herdada na target Harness) L38–54 | **SIM**, computa `discountRate` | Declaração não-summary **external**, envfree a verificar |
| `MIN_DISCOUNT_TOKEN_BALANCE() returns(uint256) envfree` | **view** | getter público de `constant`, definido na Strategy L25–29 | NÃO | **external** getter, envfree a verificar |
| `MIN_DEBT_TOKEN_BALANCE() returns(uint256) envfree` | **view** | getter público de `constant`, Strategy L30–34 | NÃO | **external** getter, envfree a verificar |
| `DISCOUNT_RATE() returns(uint256) envfree` | **view** | getter público de `constant`, Strategy L20–24 | **SIM**, limite no `assert` | **external** getter, envfree a verificar |
| `GHO_DISCOUNTED_PER_DISCOUNT_TOKEN() returns(uint256) envfree` | **view** | getter público de `constant`, Strategy L15–19 | NÃO | **external** getter, envfree a verificar |
| `wadMul(uint256,uint256) returns(uint256) envfree` | **view** | método definido no Harness L7–9 | NÃO | **external**, envfree a verificar |

**Evidência versus inferência:** arquivo R5 `round5/evidence/solc_compiled_abi_signatures.csv` comprova as seis assinaturas **da compilação Solidity em scratch da R5**, não o parser CVL2. Os seis métodos são ABI externa na target selecionada; não são seis métodos `internal` para CVL2 por simples declaração de biblioteca. Os `public constant` possuem wrappers Solidity gerados e chamadas externas; para qualquer **summary**, `internal` e `external` podem atingir call-sites diferentes, conforme [Methods — visibility](https://docs.certora.com/en/latest/docs/cvl/methods.html#visibility-modifiers). Neste caso não há summary declarado na N.spec. O uso de `envfree` do CVL1 não deve ser silenciosamente removido; a documentação exige verificação de `envfreeFuncsStaticCheck` e `envfreeFuncsAreNonpayable` em cena real. **Pure/view não equivale à aprovação desses checks**.

**Receiver / dispatch:** a target selecionada pelo runner é Harness; cinco funções são herdadas da Strategy, apenas `wadMul` é implementada diretamente no Harness. Métodos exatos CVL2 sem qualifier usam `currentContract`, mas [CVL2 Changes — receivers](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#summaries-only-apply-to-one-contract-by-default) exige que resumos explícitos indiquem o contrato definidor de funções herdadas. NÃO introduzir receiver `GhoDiscountRateStrategyHarness` para resumos de métodos definidos na Strategy sem inspeção de call resolution. A rule tem chamada direta da target; a library Solidity WadRayMath **não é** um summary arbitrário de outra target CVL. A escolha de `external` para **declaração sem summary** é uma proposta de correspondência ABI, **não** conclusão executada.

**Patch, fecho real e risco:** `certora/applyHarness.patch` da mesma revisão, blob `fe67506275c5605425c3119a60bab1cf16558271`, altera `.gitignore`, `GhoToken.sol`, `IGhoToken.sol` (introduz `isLabelNonempty`, novos `require` em três operações e muda getters de `external` para `public`). Não há hunk aplicado diretamente à Strategy/Harness. A closure anterior específica do script contém **4 import edges**, incluindo `@aave/core-v3@1.17.2` e WadRayMath SHA256 `fae5b995ec613cc213050c99ea6352c9c18ceebba106d03b1726cfa8f1f0124e`, sem import direto de GhoToken. Isso **reduz** o risco de patch nesta regra, mas NÃO prova independência de todo job auditado, e não libera automaticamente as outras 115 properties GHO.

**Status operacional conservado:** P15/incomplete/36 teve na R6 `certora-cli 8.19.0 --compilation_steps_only`, solc0.8.10, cópia byte-idêntica, **exit 1**, seis entries methods sem `function` / `;` L7–12; log original `round6/P15_36_CVL2_COMPILE_LOG.txt`. **Nenhum novo teste R8.** O [diff lexical restrito, SOMENTE DOCUMENTAL](ROUND8_METHODS_DIFF_PROPOSAL.md) mantém `envfree`, `assert`, `rule` e assinaturas, mas não certifica sintaxe/receiver válido na cena.

## 3. P12/complete/23 e /25 — duas cenas não equivalentes automaticamente

Commit histórico [aave/protocol-v2@750920303e33b66bc29862ea3b85206dda9ce786](https://github.com/aave/protocol-v2/tree/750920303e33b66bc29862ea3b85206dda9ce786), harness `specs/harness/UserConfigurationHarness.sol` L12–43, blob `38ca2686ac3652f3d64847acfd7921ca56ae94bc`; spec global `specs/UserConfiguration.spec` L1–66, blob `14fce3a67db1c5b40aa8b1c1e898a669ddbc69ea`.

| Aspecto | Auditoria / source histórica | Snapshot do dataset | Conclusão |
| --- | --- | --- | --- |
| P12/23 setBorrowing | `setBorrowing(address user,uint256,bool)` | `setBorrowing(uint256,bool)` | ABI e domínio formal distintos |
| P12/23 getter | `isBorrowing(address user,uint256)` | `isBorrowing(uint256)` | Selector distinto |
| P12/25 setter | `setUsingAsCollateral(address user,uint256,bool)` | `setUsingAsCollateral(uint256,bool)` | ABI e domínio formal distintos |
| P12/25 getter | `isUsingAsCollateral(address user,uint256)` | `isUsingAsCollateral(uint256)` | Selector distinto |
| Storage/caller | Harness histórico tem `DataTypes.UserConfigurationMap internal usersConfig`; `user` **não é referenciado no corpo** desses setters/getters | Mesmo mapa singular `usersConfig`; wrappers públicos acessam biblioteca **internal** | O argumento extra não seleciona storage por usuário nesses corpos, **mas** continua quantificado na spec histórica. Nenhuma igualdade de contraprovas demonstrada |
| Fonte global | 7 methods com `address user`, 4 invariants, 4 rules | 7 methods sem user, 4 invariants, 4 rules | Fonte CVL global de épocas diferentes |
| Fragmentos 23/25 | Rules históricas incluem user | `results/spec/complete/12/{23,25}.spec` contêm **exatamente a rule do snapshot** e duas entries dependentes, com `require reserveIndex < 128` e asserts conservados | Extração do snapshot não equivale ao replay histórico |

Os arquivos `N.spec` P12/23 blob `926c53e4a4b53084c9859b380137eef37da15e1a`, e /25 blob `85abfcddeec6f530eb00198a85be4b103c8de0d4`, permanecem intactos. Classificação **COMPILE_ERROR R5**, apenas métodos CVL1 sem `function`/terminadores `;`; sem novo teste. A falta de uso de `user` como índice de storage sugere uma possível projeção de estados para operação bitwise, porém é **inferência**, não prova: será preciso reconciliar quantificação, environment/caller, ramos de revert, invariants global, seleção de target e bibliotecas exatas. Não inserir address artificial nem redefinir `user` como `msg.sender` sem evidência.

P12 complete/10–18 VariableDebtToken: apenas 10/16 preservam tokens do corpo versus auditoria, sem POOL/execução global. 7/9 divergem. Nove StableDebtToken incompletos dependem de superclass/construtor histórico de cinco argumentos em vez de initializer snapshot. Não modificar Solidity.

## 4. P2 — nova proveniência exata de Chainlink, controlador e remappings

**DESCOBERTA R8, leitura direta do Git tree auditado** [Certora/aave-proof-of-reserve@12296ce4c6f9bde6663e1baa02cf19f179c1048b](https://github.com/Certora/aave-proof-of-reserve/tree/12296ce4c6f9bde6663e1baa02cf19f179c1048b). A árvore Git contém os seguintes **gitlinks `mode=160000`**, que fixam material fonte, ainda que não provem que os submódulos foram efetivamente instalados pelo job Prover:

| Dependência historicamente pinada | Commit gitlink SHA40 | Referência |
| --- | --- | --- |
| `lib/chainlink-brownie-contracts` | `1d301b43d374a23524eca878ffc4f9b1cf8a93d7` | [smartcontractkit/chainlink-brownie-contracts@SHA](https://github.com/smartcontractkit/chainlink-brownie-contracts/tree/1d301b43d374a23524eca878ffc4f9b1cf8a93d7) |
| `lib/solidity-utils` | `723cf9a0dbc11486910594327178b9501e646c20` | [bgd-labs/solidity-utils@SHA](https://github.com/bgd-labs/solidity-utils/tree/723cf9a0dbc11486910594327178b9501e646c20) |
| `lib/aave-address-book` | `a75e2044531136c45c6ce3cd54cda54da1102ce4` | AAVE Address Book fixado; ABI interna de `AaveV2.sol` não autenticada nesta rodada |
| `lib/protocol-v2` | `c74bceb2ffeafebf84d7c93f0a28a431a45a7a5b` | upstream `bgd-labs/protocol-v2`, branch `proof-of-reserve` |
| `lib/aave-helpers` | `2df998d6b7543f044644be5a389a590903495778` | Sem prova de uso no runner Certora |
| `lib/forge-std` | `1c418a04f6f6b002a1631838da5761641391858b` | ferramenta Foundry, não parser CVL |

**Manifesto de remappings exato:** `foundry.toml` L1–14, blob `8255763df6ab3a6a6d1e0f794c4a709b366ff106`, define `chainlink-brownie-contracts/=lib/chainlink-brownie-contracts/contracts/src/v0.8/`, `solidity-utils/=lib/solidity-utils/src/`, `aave-address-book/=lib/aave-address-book/src/`, `@aave/core-v2=lib/protocol-v2/`. O arquivo `.gitmodules`, blob `fe194854dea3f7a41821f11b94a61bc82051c930`, autentica URLs dos submódulos. **Remappings Foundry NÃO são automaticamente os --packages/--link de uma execução Certora**.

**Fonte Chainlink já recuperada por commit+blob:** `smartcontractkit/chainlink-brownie-contracts@1d301b43.../contracts/src/v0.8/interfaces/AggregatorV3Interface.sol`, blob `cd72a0c0b928f23e0d40fe1d5db985099e15c810`, L1–32. Define `latestRoundData() external view returns (uint80 roundId,int256 answer,uint256 startedAt,uint256 updatedAt,uint80 answeredInRound)`. `src/contracts/ProofOfReserveAggregator.sol` no SHA histórico, blob `c3c79998b5d5801457ba26d007aa75df9de947df`, chama `AggregatorV3Interface(feedAddress).latestRoundData()` **na feed externa** L108–113; também chama `IERC20(totalSupplyAddress).totalSupply()` L115–118. Sua target local possui getters e `enableProofOfReserveFeed` / `disableProofOfReserveFeed` **onlyOwner**. O `Ownable.sol` recuperado por gitlink solidity-utils (`e1f2ad83b7ee6d5bb269a7e19c857e9fa34cca40`) restringe por `owner` e `msg.sender`.

**Controlador/interface, cuidadosamente separado:** arquivo real `src/dependencies/ICollectorController.sol`, blob `2fde9ec75fd403928858f44f247b0418b82eb236`, L1–12, contém somente **interface** `transfer(IERC20,address,uint256)` e importa IERC20 de solidity-utils; **não** foi localizado um contrato controlador instanciado ou mapeado à target das propriedades por essa informação. ExecutorV2 importa `aave-address-book/AaveV2.sol` e interage com `_pool`, `_configurator` e o Aggregator; gitlink não fornece configuração do Prover da época, nem comprova AaveV2.sol instalado. Evitar inventar controlador/mock. Até aqui, **6 SHAs gitlink recuperados**, uma interface Chainlink exata e Ownable exato; continua inexistente o arquivo de spec/conf/harness CVL na árvore auditada (busca no tree).

**Summary/receiver:** CVL1 `contracts/2/specs/aggregator.spec` L9–12 tem `latestRoundData() => NONDET` sem receiver; CVL2 `currentContract` é apenas a target corrente, **não** o `feedAddress`. Wildcard `_.latestRoundData` sem prova de universo original poderia incluir outros contratos. A interface histórica estabelece que `latestRoundData` é `view`, o que é condição importante de validade de NONDET, mas não identifica o receiver realmente ligado nem as regras de summary do CVL1 para esse job. Além disso, `PoRFeedChange` L17–54 tem `method f` e `call_f_with_params`: permissões `onlyOwner`, chamadas genéricas/reverts e funções da cena precisam ser preservadas. **Não construir getter, mock ou summary especulativo.**

## 5. Contrarrevisão read-only: PRs #40 e #46

- [PR #40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40), HEAD `5a50cd43a56add63d91e2476b3d0460e991cdacc`, Draft. P7/37,65 têm **apenas fragmentos** compilados, P7/36,41,47,63,73 são cinco parser errors históricos. Variante documental `sig:` P7/47 **não foi compilada** por EIO. Seletores ABI presentes não demonstram quantificação não-vazia de `method f`, e `@withrevert` difere de `f(e,args)`; nenhuma equivalência. Sem edição.
- [PR #46](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/46), HEAD `62754c10e3e9dc23d122aad3333eac2ec60f817d`, Draft. Dois derivados `divPrecisely(mathint,mathint)` obtiveram `COMPILE_OK` restrito. `RCPT=0` continua possível, a segunda chamada divide por zero, e a semântica operacional `mathint/0` versus CVL1 não foi demonstrada. A relação matemática entre assertions sob `RCPT>0` **não** é equivalência entre versões. Preservar `02_unresolved`, sem alterar asserts/requires ou branch.

## 6. Gates propostos — por maior viabilidade, sem execução R8

**Experiência 1 (P15/incomplete/36):** após recuperação do host e gate individual do coordenador, testar **uma só variante scratch** que modifique exclusivamente as seis declarações methods com `function`, `external`, `;`, mantenha `envfree`, 1 rule e assert, compare N.spec SHA/cmp, target real Harness e hashes da closure; `--compilation_steps_only`, timeout, stdout/stderr e exit. Registrar separadamente envfree static checks e scene globals; mesmo EXIT 0 não prova equivalência.

**Experiência 2 (P12/complete/23):** depois da primeira decisão humana quanto à época/ABI (`user` auditado vs sem `user` snapshot), autorizar **um teste individual** do fragmento byte-idêntico num cenário declarado, sem trocar Solidity ou restringir `reserveIndex < 128`, com relatório da divergência dos domínios; depois /25 separadamente. Se a cena histórica não fechar, manter `NOT_RUN`, não forçar compilação com mudança de wrapper.

**Bloqueio de P2:** reconstruir source closure em scratch **somente** após WSL recuperado e documentação dos novos gitlinks, mas sem compilação CVL antes do runner original, receiver, configuração de summary e executor wrappers serem autenticados.

**Não houve neste PR:** alteração de `results/spec`, `contracts`, relatórios e CSV original, `results/cvl2`, novas specs derivadas, Prover/CVL1, `certoraRun`, correção de `assert/require`, mock inventado nem merge.

**AGENTE-04 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS**
