# AGENTE-04 — RODADA 7 / Evidência CVL2 orientada a ABI e semântica

**Escopo fixo:** P2=15, P12=26, P15=116; baseline imutável main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. Branch research/cvl2-agente-04, PR #42 Draft. Rodada 7 **somente pesquisa documental** pelo GitHub após incidente WSL EIO; zero execuções CVL2 novas, zero Prover/CVL1, zero mudanças de código/CI historical, zero specs derivadas.

## 1. Fontes, prova de identidade e painel

| Ref / objeto | Localização e faixa | Constatação |
| --- | --- | --- |
| SHA Git histórico | PR #42 head 3cd8f72c35d94b4a48cb6155628cba4bea378c67, main@2a03637 | Branch conferida antes de editar, Draft |
| CSV imutável | results/spec/spec_buglabel.csv, blob Git 97e20443586540034a4c0305ce1db19b0d2f8cb5 | **Mesmo blob** no baseline e na HEAD; 1390 relações e 1386 chaves |
| Quatro normas | docs/spec_catalog.md, spec_catalog_workflow.md, spec_catalog_project_1.md, standard.md | Critérios de original complete/incomplete separados de CVL2, Bug Label distinto de Result/Outcome |
| Controle externo | PR #47/ROUND6_DASHBOARD.md, blob 71490ebb4dfcbba848472ab0ab4c2a6394aa9a95 | R6 global 4 compile OK limitados, 12 compile errors, 1370 não testadas e 0 equivalência |
| Incidente | PR #47/ROUND6_WSL_IO_INCIDENT.md, blob cbf7ad62740e09d4f9cc9d11cf039977c0f44757 | spawn EIO/SIGBUS/EROFS: proibido rodar WSL até gate humano de recuperação |

Reconciliação nesta rodada executada **em memória via conector GitHub**: 157 linhas únicas em ROUND6_PROGRESS.csv para AG04, confrontadas com TODAS as relações do CSV canônico nos campos Project ID, Status, Example ID, Property, Target Contract, Result, Detection Outcome e caminho N.spec: **zero mismatches**, inclusive casos com vários Bug Labels. Na matriz R7, SHA-256 de N.spec e source são **provenance documentada herdada do ledger R6**, não uma alegação de recálculo dos 157 hashes em WSL nesta rodada. Amostras P1: complete/1/1 (closure do snapshot) versus incomplete/1/1 (queue2 ausente); 'complete' não significa compilável CVL2.

## 2. P15/incomplete/36 — seis métodos: ABI, mutabilidade, receiver e envfree

**Evidência Solidity versionada:** aave/gho-core@ce49fb0c94cfebf0159222ceb288e4f9a55d305f, certora/harness/GhoDiscountRateStrategyHarness.sol L1-9 e src/contracts/facilitators/aave/interestStrategy/GhoDiscountRateStrategy.sol L10-54. Script histórico certora/scripts/verifyGhoDiscountRateStrategy.sh L3-20 verifica **GhoDiscountRateStrategyHarness**, não a target nominal GhoDiscountRateStrategy do CSV. Métodos originais: contracts/15/ghoDiscountRateStrategy.spec L1-8 e N.spec incomplete/15/36 L6-13. Todos os métodos são declarados envfree na spec CVL1.

| Método em N.spec | ABI SOLC 0.8.10 anteriormente obtida | Local da definição | Uso nesta rule | Hipótese CVL2 (NÃO testada) |
| --- | --- | --- | --- | --- |
| calculateDiscountRate(uint256,uint256) returns uint256 | pure | GhoDiscountRateStrategy L38-54, external pure | **Sim**, rule L24 | methods entry **external**; envfree necessita checagem independente |
| MIN_DISCOUNT_TOKEN_BALANCE() returns uint256 | view | constant public na strategy L25-29 | Não diretamente | getter **external**, envfree hipótese |
| MIN_DEBT_TOKEN_BALANCE() returns uint256 | view | constant public na strategy L30-34 | Não diretamente | getter **external**, envfree hipótese |
| DISCOUNT_RATE() returns uint256 | view | constant public na strategy L20-24 | **Sim**, assert L25 | getter **external**, envfree hipótese |
| GHO_DISCOUNTED_PER_DISCOUNT_TOKEN() returns uint256 | view | constant public na strategy L15-19 | Não diretamente | getter **external**, envfree hipótese |
| wadMul(uint256,uint256) returns uint256 | view | GhoDiscountRateStrategyHarness L7-9, external view | Não diretamente | **external**, envfree dependente do corpo/lib |

O arquivo round5/evidence/solc_compiled_abi_signatures.csv contém **6/6 assinaturas comprovadas** para essa target, mas é somente compilação ABI Solidity antiga, não execução CVL2 atual. A estratégia base declara calculateDiscountRate external pure, chama **WadRayMath.wadMul** via biblioteca Solidity (não um contrato receiver secundário de CVL). O harness declara wadMul external view e encaminha a library. Os outros quatro métodos são getters externos gerados por variáveis **public constant**. Portanto, a evidência favorece **external** na interface CVL de chamadas externas; **internal** representa outra classe de entrada e não pode ser escolhido por intuição. Como o corpo pure e os getters constant não consultam env explicitamente, envfree é **plausível**, mas só passa a ser comprovado com checks estáticos envfree da cena real; não declarar aprovação apenas pelo mutability ABI ou por um eventual parser exit 0.

**Receiver:** chamadas diretas CVL em P15/36 devem visar a target de verificação GhoDiscountRateStrategyHarness, que herda cinco entradas definidas na strategy; ao escrever eventual summary, a documentação oficial exige distinguir o contrato **onde o método é definido** (superclass) e o receiver. Não há summary ou wildcard no methods original do caso; adicionar um seria alteração de semântica. Não há ghost, hook, invariant ou using CVL global nessa source específica. O CVL integral auditado certora/specs/ghoDiscountRateStrategy.spec L1-91 tem **6 methods, 2 functions e 5 rules ativas**; o N.spec recorta só o rule limitOnDiscountRate. As funções auxiliares não são chamadas diretamente pelo rule, mas equivalência das cenas não está estabelecida.

**Dependência e patch por alcance real:** R5/evidence/gho_import_closure_edges.csv registra **quatro import edges** nessa família: harness -> GhoDiscountRateStrategy.sol, harness -> @aave/core-v3/WadRayMath.sol, strategy -> WadRayMath, strategy -> IGhoDiscountRateStrategy. Todos quatro destinos estavam presentes nos pacotes scratch SRI; source WadRayMath SHA256 fae5b995ec613cc213050c99ea6352c9c18ceebba106d03b1726cfa8f1f0124e. O patch histórico certora/applyHarness.patch da mesma HEAD modifica **somente** .gitignore, GhoToken.sol e IGhoToken.sol, com requires novos e mudança external→public. **Não há modificação direta do patch à strategy nem ao harness P15/36; tampouco dependência direta de GhoToken nessa cena dos quatro imports**. Esta delimitação é específica desse example ID, **não** autoriza declarar patch inofensivo nas outras 115 properties GHO.

**Reverts e vacuity:** calculateDiscountRate tem branches de threshold, return 0, return DISCOUNT_RATE e divisão de inteiros após WadRayMath.wadMul; erros de arithmetic/revert da biblioteca e semântica de saturação/arredondamento não podem ser eliminados por novo require/cast. A rule original tem parâmetros livres uint256 de debt e discount e **não** adiciona require que exclua inputs. O baseline de certificação do report é VERIFIED histórico, não prova atual. A última execução efetiva R6 P15/36 foi CLI 8.19.0/solc0.8.10 compilation-only **EXIT 1** por seis methods CVL1 L7-12 sem function/semicolon; log integral round6/P15_36_CVL2_COMPILE_LOG.txt. **Rodada 7: NOT_RUN_INFRA_BLOCKED; nenhum novo log.**

**Gate específico:** após administrador recuperar WSL, confirmar SHA da target compilada e das quatro import edges, ABI 6/6, script/prover settings históricos, receiver herdado, mutabilidade e envfree static checks; só então submeter variante **individual** de sintaxe methods, sem mudar premissas/assert/solidity e sem confundi-la com replay histórico.

## 3. P12/23 e 25 — domínio de address user, sem modificar wrappers

Commit auditado aave/protocol-v2@750920303e33b66bc29862ea3b85206dda9ce786, specs/harness/UserConfigurationHarness.sol L12-43 e specs/UserConfiguration.spec L1-65. Wrapper da auditoria tem setBorrowing(address,uint256,bool), isBorrowing(address,uint256), setUsingAsCollateral(address,uint256,bool), isUsingAsCollateral(address,uint256); snapshot contracts/12/specs/harness/UserConfigurationHarness.sol L15-32 remove o argumento address user nas funções correspondentes. O wrapper auditado **não utiliza user no corpo**: opera sobre usersConfig único, porém isso não remove o parâmetro formal de ABI/call domain no CVL histórico. Mesmo resultado de operação bitmap para um conjunto de inputs não equivale a igualdade dos universos de quantificação, filtros de revert ou selectors.

Na versão snapshot, setters da target public invocam funções **internal** da biblioteca UserConfiguration.sol; as entries methods para a target de verificação devem ser apreciadas como wrappers externos, não como resumo de função de biblioteca. Source CVL global snapshot possui 7 methods, 4 invariants, 4 rules; N.spec/23 e /25 guardam só dois methods e a rule selecionada. Invariant proofs possuem contexto de outras funções e possíveis reverts; o Prover não assume invariants arbitrariamente dentro da rule. Não adicionar requireInvariant, endereço fictício ou cast para sintetizar equivalência. Ambos são COMPILE_ERROR do R5 por function e ; em methods, **não retestados**.

**P12 VariableDebt complete/10-18:** /10 e /16 semelhantes apenas no corpo lexical após normalização; outras 7 rules divergem. using LendingPoolHarnessForVariableDebtToken as POOL, index getter, signatures de mint/burn, sinvoke/invoke e universo method f exigem confronto de época. Nove StableDebtToken incomplete ficam com superclass constructor/getters incompatíveis, sem inventar adaptação.

## 4. P2 — latestRoundData pertence à feed externa, não ao Aggregator

ProofOfReserveAggregator.sol commit Certora/aave-proof-of-reserve@12296ce4c6f9bde6663e1baa02cf19f179c1048b, snapshot contracts/2/contracts/ProofOfReserveAggregator.sol L1-124, já confirmado byte-identical em R5. L4-8 importa solidity-utils, Chainlink AggregatorV3Interface e interface local; getters da target L23-36; onlyOwner e require de enable/disable L39-86. areAllReservesBacked L89-122 executa AggregatorV3Interface(feedAddress).latestRoundData() na **feedAddress** de um contrato externo; tipo Chainlink retorna tuple (uint80,int256,uint256,uint256,uint80), diferente de getter local da target. Source CVL1 aggregator.spec L1-13 declara summary **latestRoundData() => NONDET** sem receiver; PoRFeedChange L17-54 possui helper call_f_with_params e quantifica method f, com seletores e caminhos de revert.

Na migração CVL2, um method entry sem receptor default é currentContract, que **não modela automaticamente** o feed externo; wildcard _.latestRoundData pode afetar conjunto maior de contratos/UNRESOLVED vs ALL, com política diferente do summary global CVL1. O NONDET é classificado como sound somente sob hipóteses view específicas; sem ABI Chainlink auditada, links e target contratado, não declarar seu escopo. Além disso, o método f do rule inclui chamadas alternativas e onlyOwner; um revert pode tornar ramos vacuous. Audit tree com 99 arquivos sem specs/.conf/harness; executar substitutos inventados seria inválido. 15 cases P2 permanecem sem compilação CVL2 observada.

## 5. Revisão cruzada somente leitura, PRs #40 e #46

**PR #40, HEAD 31ce9c427e5aed759c1b04932ed9ebdd76cbe959:** cinco COMPILE_ERROR históricos P7/36,41,47,63,73 por sig:; variante de seis sig: em P7/47 foi somente proposta, não executada devido a SIGBUS/EIO. P7/37,65 foram só dois fragmentos COMPILE_OK; as CVL globais hooks/ghosts/methods e universe method f não foram aprovadas. Identidade de seis selectors ABI não assegura ausência de vacuity. Nenhuma promoção indevida observada.

**PR #46, HEAD 62754c10e3e9dc23d122aad3333eac2ec60f817d:** dois derivados P19/1,2 mudaram uint,uint para mathint,mathint e tiveram COMPILE_OK restrito; RCPT=0 é permitido e segunda divisão por zero permanece sem semântica operacional CVL1→CVL2 demonstrada; RC*10^18 pode exceder intermediário uint256. V1 contido em V2 no modelo matemático RCPT>0 compara **duas assertions**, não prova equivalência entre versões. Manter 02_unresolved e Draft; sem edição alheia.

**Decisão final R7:** nenhuma família possui autorização de SEMANTIC_PROVEN ou MIGRATED_COMPLETE, nenhum novo compile-only sem recuperação humana. Propostas methods/summaries/receiver aqui são **somente documentais**, sem arquivo .spec derivado nem patch.

### Documentação oficial consultada

- https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html
- https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html
- https://docs.certora.com/en/latest/docs/cvl/methods.html
- https://docs.certora.com/en/latest/docs/cvl/hooks.html
- https://docs.certora.com/en/latest/docs/cvl/ghosts.html
- https://docs.certora.com/en/latest/docs/cvl/invariants.html
- https://docs.certora.com/en/latest/docs/cvl/statements.html

AGENTE-04 — RODADA 7
