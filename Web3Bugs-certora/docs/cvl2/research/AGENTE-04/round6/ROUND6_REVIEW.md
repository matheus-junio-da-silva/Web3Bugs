# AGENTE-04 — RODADA 6 / Pesquisa e QA CVL2

Base imutável: main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. Branch exclusiva research/cvl2-agente-04, PR #42 DRAFT. HEAD de partida dd957753ac06d6e899d44cb7caf952de8e3e0916. Nenhum merge, edição de fontes originais ou implementação derivada.

## Governança e denominadores

Foram lidos os quatro documentos normativos docs/spec_catalog.md, spec_catalog_workflow.md, spec_catalog_project_1.md e standard.md. Comparados exemplos do Project 1 nas pastas complete/1 (36 exemplos) e incomplete/1 (34): complete é fechamento de dependências no snapshot, nunca compatibilidade CVL2; incomplete explicita funções auxiliares ausentes como queue2. Lida a quinta revisão do PR #42, painel e CSV ROUND5_DASHBOARD.md do PR #47. Consultadas as fontes oficiais [Migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [Methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [Hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html), [Statements/reverts](https://docs.certora.com/en/latest/docs/cvl/statements.html).

A nova matriz ROUND6_PROGRESS.csv preserva as 157 chaves únicas (project_id, original_status, example_id), os nomes, targets, SHA-256 das sources e N.spec, Result/Detection Outcome, candidato documental e blockers herdados. Adiciona origem auditada, cena, globais CVL, comando/exit comprovados, risco de vacuity e gate individual. P15=116, P12=26, P2=15. Permanecem 18 DOCUMENTED_CANDIDATE como hipótese (17 P12, 1 P2), 0 SEMANTIC_PROVEN e 0 projetos MIGRATED_COMPLETE.

## Execuções reais versus herdadas

| ID | Cena e observação | Gate |
| --- | --- | --- |
| P12/complete/23 setBorrowing | Rodada 5, N.spec idêntica, solc0.6.12 / certora-cli8.19.0, --compilation_steps_only EXIT 1, methods L5–L6 sem function/semicolon | COMPILE_ERROR herdado |
| P12/complete/25 setUsingAsCollateral | Rodada 5, mesmo harness snapshot, N.spec idêntica, EXIT 1 pelos mesmos requisitos em L5–L6 | COMPILE_ERROR herdado |
| P15/incomplete/36 limitOnDiscountRate | Rodada 6 NOVA: N.spec SHA256 eee38425eb95100799fe30e8d5913f9593230763733197a3dae5dae95cb0073e, cmp idêntico; CLI 8.19.0 DIRETO, solc0.8.10, timeout 65s, HOME isolado, CERTORAKEY/CERTORA_TOKEN/CERTORA_API_KEY removidos, --compilation_steps_only EXIT 1 | COMPILE_ERROR novo: methods L7–L12 sem function e sem ;. Log integral anexado |
| Outras 154 | Nenhuma execução CVL2 individual observada | NOT_RUN |

**Totais AG04 cumulativos: 0 COMPILE_OK, 3 COMPILE_ERROR, 0 PREFLIGHT_AUTH_BLOCKED, 154 NOT_RUN, 0 equivalência.** Solc ABI bem-sucedido anteriormente não conta como compile-only CVL2. O painel global R5 tinha 4 sucessos limitados, 11 falhas e 1.371 não testados; esta nova tentativa, se nenhum agente concorrente adicionar dados, levaria a 4/12/1.370. Não atualizar ledger da coordenação sem revisão.

## P12 — assinatura, receiver e universo das regras

| Fonte | Linhas | Fato específico |
| --- | --- | --- |
| snapshot contracts/12/specs/harness/UserConfigurationHarness.sol | 12–40 | Methods públicos setBorrowing(uint256,bool), isBorrowing(uint256), setUsingAsCollateral(uint256,bool), isUsingAsCollateral(uint256) |
| aave/protocol-v2@7509203/specs/harness/UserConfigurationHarness.sol | 12–44 | Mesmas famílias incluem argumento adicional address user |
| snapshot contracts/12/contracts/protocol/libraries/configuration/UserConfiguration.sol | 22–47, 70–91 | Bibliotecas internas para setters/getters; wrapper público é a target externa, não chamar library internal como se fosse ABI externa |
| contracts/12/specs/UserConfiguration.spec | 1–66 | Fonte global tem 7 entradas methods, 4 invariants e 4 rules; cada N.spec 23/25 guarda só 2 methods e 1 rule |
| results/spec/complete/12/23.spec e 25.spec | 4–15 | Manter guard reserveIndex < 128, operações e assertions textualmente originais |

O argumento user do harness auditado não seleciona um mapa distinto (ele utiliza usersConfig no wrapper consultado), mas o valor participa da quantificação CVL e altera a assinatura externa e a cena. Não se pode concluir por isso equivalência do universo de contraexemplos. Invocações dos getters view marcadas envfree, resumo de chamadas, reverts e hipóteses não foram reproduzidos. Invariants do arquivo global não se transformam automaticamente em requireInvariant para as rules fragmentadas; o efeito de omitir os demais componentes exige análise do contexto. Nenhuma conversão sintática ou alteração de require foi efetuada.

P12/complete/10 balanceOfChange e /16 integrityBurn possuem corpo igual em tokens após remoção de whitespace/comentários versus upstream, mas o linking POOL e quantificação method f não estão fechados; /16 chama POOL.getReserveNormalizedVariableDebt, e /10 permite funções da ABI a serem delimitadas. P12/complete/11,12,13,14,15,17,18 têm corpos divergentes da versão upstream. Nove StableDebtToken incomplete continuam sem resolver constructor de cinco argumentos da versão auditada versus initialize snapshot. Nenhum import/harness reescrito.

## P15 — uma target, um diagnóstico

aave/gho-core@ce49fb0c94cfebf0159222ceb288e4f9a55d305f fixa @aave/core-v3@1.17.2. Rodada 5 autenticou SRI de core-v3 1.17.2, periphery-v3 2.0.1 e OpenZeppelin 4.8.1; aplicou o patch original em scratch, resultando em novos require, campo isLabelNonempty e getters external->public. Foram percorridas 284 arestas de import Solidity no conjunto das cinco cenas, sem missing file no pacote selecionado, não comprovando ambiente de execução da auditoria.

Apenas P15/incomplete/36 foi testado. O script auditado certora/scripts/verifyGhoDiscountRateStrategy.sh L3–20 escolhe GhoDiscountRateStrategyHarness (diferente da target nominal GhoDiscountRateStrategy no CSV), solc8.10 e settings históricas. Harness L1–9 herda GhoDiscountRateStrategy, usa WadRayMath e expõe wadMul; N.spec L6–26 contém seis methods e limitOnDiscountRate. A spec CVL integral upstream certora/specs/ghoDiscountRateStrategy.spec L1–91 contém 6 methods, duas funções auxiliares (wad, wadMulCVL) e cinco rules ativas, enquanto N.spec tem só uma rule. As outras funções não são chamadas diretamente por limitOnDiscountRate, mas não foi estabelecida equivalência do contexto global. O typechecker parou no parser methods antes de qualquer análise semântica.

## P2 — Chainlink feed receiver externo

Contratos/2/contracts/ProofOfReserveAggregator.sol reproduz os bytes do commit Certora/aave-proof-of-reserve@12296ce4. L89–122 chama AggregatorV3Interface(feedAddress).latestRoundData() no **feed externo**; não existe esse método na ABI do Aggregator. A spec original contracts/2/specs/aggregator.spec L1–13 contém latestRoundData() => NONDET, enquanto PoRFeedChange L35–54 quantifica method f e filtra selectors. O resumo CVL2 usando apenas currentContract não cobriria automaticamente o feed; wildcard pode mudar universo e política de unresolved calls. O commit auditado com 99 arquivos não continha .spec/.conf/harness CVL recuperáveis; bibliotecas Chainlink e Solidity-utils de época não foram autenticadas. Não inferir mocks, getter ou receiver. Os 15 exemplos P2 seguem NOT_RUN nesta pesquisa.

## Próximas decisões da coordenação

1. P12: arbitrar ABI auditada com user versus snapshot sem user, target externa do wrapper, POOL e globals antes de qualquer variante CVL2 por example ID.
2. P15: adjudicar target/harness P15/36, pertinência das funções e rules CVL globais, patch com novos requires, runner e ABI; somente então eventual variante scratch de sintaxe e diagnóstico individual.
3. P2: recuperar feed, dependências e configuração/harness originais e fixar receiver/summary; sem essas fontes manter bloqueio terminal documentado.
4. Não confundir ABI Solidity, parser ou CI estrutural com equivalência de motores ou de contraexemplos.

O equipamento remoto apresentou falha de sistema de arquivos após o teste: /home/mat somente leitura, Python com Bus error e df com I/O error. Assim, os três validadores não devem ser declarados como executados após esta publicação caso esse ambiente não seja recuperado. O GitHub CI, se disparado, deverá ser inspecionado separadamente e atribuído apenas ao seu próprio workflow. Nenhum Prover, CVL1, migração em massa, alteração de N.spec ou results/cvl2.

**ALERTA LARANJA — AGENTE-04 — RODADA 6**
