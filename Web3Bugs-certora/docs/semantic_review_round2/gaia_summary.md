# GAIA — revisão semântica cruzada, rodada 2

**Escopo:** Projects 1, 2, 3, 6 e 22; **141 instâncias de property**, sem alteração de qualquer `N.md`, `.spec`, `.sol`, fonte histórica ou PR e sem merge. Revisão sobre o ZIP local fornecido, comparações CVL/Solidity no snapshot, PDFs locais disponíveis e — somente para o Project 22, ausente do ZIP — fontes da branch integrada `catalog/p22-echo-popsicle-v3-optimizer`, PR #18, commit `ff012a7e549ff488ee008e746f840576589f4084`.

## Resultado e leitura dos estados

`CONFIRMED` confirma a adequação **documental/semântica limitada às evidências acessíveis**, e jamais significa reexecução de Certora. `CORRECTION_REQUIRED` exige mudar documentação/label/oráculo antes da aceitação. `INCONCLUSIVE` não é aprovação: faltam target, harness, proveniência visual do PDF ou evidências suficientes. Neste relatório, **pendentes = CORRECTION_REQUIRED** e **inconclusivos são contabilizados separadamente**.

| Project | Exemplos | Confirmados | Correção pendente | Inconclusivos | VERIFIED histórico | VIOLATED histórico | NOT_STATED |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 — AAVE L2 Bridge | 70 | 0 | 64 | 6 | 44 | 2 | 24 |
| 2 — AAVE Proof of Reserve | 15 | 8 | 1 | 6 | 10 | 0 | 5 |
| 3 — AAVE Rescue Mission | 3 | 3 | 0 | 0 | 2 | 1 | 0 |
| 6 — AAVE Static aToken | 32 | 24 | 0 | 8 | 8 | 0 | 24 |
| 22 — Popsicle V3 Optimizer | 21 | 5 | 0 | 16 | 12 | 0 | 9 |
| **Total** | **141** | **40** | **65** | **36** | **76** | **3** | **62** |

**Prioridades por registro:** P0 = **2**; P1 = **99**; P2 = **40**. Uma prioridade não deve ser confundida com a gravidade de uma vulnerabilidade on-chain: descreve a urgência de corrigir a evidência técnica do catálogo.

## Evidências e método

A matriz lê os corpos de `rule`/`invariant` dos arquivos `.spec` arquivados, separa `assert` de `require`, `filtered`, `preserved` e condições globais, confronta métodos/storage dos `.sol` e registra eventuais declarações ausentes. Captura Bug Label original, resultado e Outcome sem propagação por família. A coluna `source_paths` identifica cada arquivo; `source_limitations` registra hipóteses, ghost/hooks, missing harness e versão. Onde o CVL chama helpers históricos indisponíveis, o predicado é descrito apenas até o limite do corpo acessível — **não se inventou a implementação faltante**.

Os PDFs foram examinados localmente com extração de texto para Projects 2 (`resources/2/Aave-Proof-of-Reserve-Formal-Verification-Report.pdf`), 3 (`resources/3/Rescue-Mission-Phase-1.pdf`) e 6 (`resources/6/Formal_Verification_Report_staticAToken.pdf`). O Project 1 contém transcrição por página em `reports/1.md`, mas o ZIP não inclui seu PDF original; as afirmações sobre marcas visuais dependem dessa transcrição. Para Project 22, o PDF de 10 páginas é citado no catálogo remoto, mas só foi acessada a transcrição `reports/22.md`, com identificações por página; não foi feita validação visual ou reexecução da prova. Essa diferença de qualidade de fonte motivou classificações conservadoras.

### P0 — oráculo semanticamente excessivo (Project 1)

1. **`complete/1/15` — `whoChangesActionsSetState`**: a regra seleciona **qualquer `f` não-view** e executa `f(e,args)`, mas exige `getCurrentState(id)` idêntico antes/depois. `execute` e `cancel` são operações legitimamente capazes de alterar estado (`_actionSets[id].executed`/`.canceled`). A property, sem exclusões adicionais, descreve um falso invariante de imutabilidade. Revisão proposta: **`S3-2` → `UNMAPPED` provisório**, até definir seletor e pressupostos corretos; `Result=NOT_STATED` mantido.
2. **`complete/1/32` — mesma regra no target Optimism/Arbitrum**: repetição do problema; a documentação precisa explicar a seleção de `f` e não pode tratar uma mudança de estado legítima como bug. Mesma decisão/proposta.

A classificação P0 aqui é de **risco de soundness do oráculo**, não afirmação de que o Prover gerou contraexemplo ou que houve exploit. Ambos permanecem sem resultado formal individual declarado.

## Project 1 — AAVE L2 Bridge: 70

**64 justificativas Solidity precisam ser reescritas:** todos os 36 arquivos `results/spec/complete/1/{1..36}.md` e os 28 arquivos `results/spec/incomplete/1/{1..28}.md` usam literalmente a frase genérica sobre *state, lifecycle, queue/execution, or access-control*. A frase não identifica qual getter, mutador, storage/mapping ou transição realmente estabelece a assertion. Todos esses 64 têm `solidity_justification_decision=REWRITE_REQUIRED`, e a matriz inclui o predicado recuperado do CVL, funções/storage do excerto e orientação individual em `justification`/`technical_intent` para substituir a frase.

| Família do predicado | Vínculo CVL → Solidity exigido na justificativa específica |
|---|---|
| Configuração e privilégios (`whoChangedStateVariables`, `properDelay`, `minDelayLtMaxDelay`) | Getters `getDelay`, `getGracePeriod`, `getGuardian`, `getMinimumDelay`, `getMaximumDelay`; storage `_delay`, `_gracePeriod`, `_guardian`, limites; `update*` com `onlyThis`/validação. A regra exige mudança somente pelo `currentContract` ou a ordem dos limites, conforme a assertion concreta. |
| Contador/queue (`queuedChangedCounter`, `queuedStateConsistency`, `actionDuplicate`) | `_actionsSetCounter`, `_actionSets`, `_queuedActions[hash]`, `getActionsSetCount`, `_queue` e ingresso `processMessageFromRoot`/`queue2`: demonstrar incremento, novo estado `queued` ou prevenção de duplicidade, sem confundir caminhos. |
| Temporalidade/identidade (`independentQueuedActions`, `sameExecutionTimesReverts`, `holdYourHorses`) | `executionTime=block.timestamp+_delay`, cálculo de hash e `_queuedActions`: as duas primeiras properties testam comportamentos opostos sob hipóteses diferentes. `independentQueuedActions` é **VIOLATED/FINDING**, descrito na transcrição do relatório pp.2 e 11; a colisão ocorre quando o delay muda entre blocos. |
| Máquina de estados (`executeCannotCancel`, `executedForever`, `canceledForever`, `expiredForever`, `executedValidTransition*`) | `getCurrentState`, `execute`, `cancel`, `.executed/.canceled`, `executionTime` e `gracePeriod`. `expiredForever` tem ressalva histórica de mudança da grace period; não prometer imutabilidade incondicional. |
| Entrada privilegiada e origem da mensagem (`queuePriviliged`, `cancelPriviliged`, `onlyCancelCanCancel`) | `processMessageFromRoot` no Polygon, executores L2/messenger nos outros targets, guardian e restrições do chamador. Proibir segundo chamador não é equivalente a negar todas as queues. |
| Getters ausentes em `incomplete` | Atributos `executed/canceled`, `ID2actionHash` e `queue2` podem depender de harness ou funções CVL históricas não presentes. Trecho Solidity não substitui implementação faltante. |

**Seis instâncias restantes não devem receber justificativa artificial**: `incomplete/1/{29,30,31,32,33,34}` (`sanity`, `noRevert`, `alwaysRevert`, `simpleFrontRunning`, `privilegedOperation`, `whoChangedBalanceOf`) são regras genéricas de análise/diagnóstico sem target contratual demonstrado; classificação `INCONCLUSIVE`. `assert false` nas sondas de alcance (`complete/1/22` e `incomplete/1/28-29`) não é finding nem garantia de segurança. `notCanceledNotExecuted` tem requisito `id == getActionsSetCount()` apenas em `preserved`; ignorá-lo altera a interpretação da property.

## Project 2 — AAVE Proof of Reserve: 15

**`complete/2/1` — `PoRFeedChange` (`CORRECTION_REQUIRED/P1`)**: o CVL observa `_proofOfReserveList` e `_bridgeWrapperList` via getters, roteia três setters/disable por `call_f_with_params` e exige que **outros selectors preservem** ambos os mappings. A prosa do PDF sobre *other functions* diz que devem mudar — o oposto do `assert` original. O label primário `S3-2` é sustentado. Proposta de retirar a relação adicional `S2-1`: exigir feed/wrapper não zero em chamada habilitada bem-sucedida **não testa**, por si, falta de validação do ID `asset` ou escrita não autorizada por usuário; a claim mais ampla carece de evidência no predicado. Resultado histórico `VERIFIED/NO_FINDING` preservado como atribuição nominal, não reexecutado.

`incomplete/2/1` (`notAllReservesBacked_UnbackedArry_Correlation`) é **inconclusivo**: o corpo testa igualdade de dois booleanos, mas o helper `areAllReservesBackedCorrelation` e o getter `allBacked` não estão no snapshot. `S6-2` é inferência baseada na função de produção `areAllReservesBacked`, não reconstrução do helper perdido. Os invariants de `flagConsistancy`, `flagConsistancy2` e `uniqueArray` são tratados como **inconclusivos** porque `_assets`, `_assetsState`, `mirrorArray`, `mirrorFlag`, `reverseMap` e `Sload/Sstore hooks` impõem hipóteses cruzadas; o `preserved` filtra `executeEmergencyAction`. Não tratar os 10 `VERIFIED` do PDF como comprovação de todos os mocks/harness ausentes. As regras de enable/disable restante preservam `CONFIRMED` documental, sob limitação de replay.

O relatório limita unrolling a **três iterações** nos executores e resume `areAllReservesBacked` com valor arbitrário ao verificar executores. São condicionantes da prova, não propriedade da implementação real do oráculo Chainlink.

## Project 3 — AAVE Rescue Mission: 3

`incomplete/3/1` testa `((LEND.totalSupply-LEND.balanceOf(LEND))/LEND_AAVE_RATIO) <= AAVE.balanceOf(migrator)`. O relatório marca **VIOLATED/FINDING** na história da migração, inclusive o cenário de contagem incorreta de LEND durante dois upgrades assíncronos; há correções citadas nos commits `4c59da8d` e `c905eaf`. Isso **não implica violação na revisão final mitigada**. `incomplete/3/2` revalida o mesmo lastro após a sequência `initialize` do migrador e do AAVE V2 (ou caminho genérico `f`), com requisitos de `msg.sender` contra tokens. `incomplete/3/3` exige `stkAAVE.totalSupply <= AAVE.balanceOf(StakedToken)`. As três são `CONFIRMED` como *classificação e leitura histórica*, **não** como provas reexecutadas: faltam bindings das interfaces/harness e o `onTransfer` é assumido sem efeito sobre storage dos contratos. O rótulo `S6-4` corresponde ao lastro/accounting, não a simples detecção por arredondamento.

## Project 6 — AAVE Static aToken: 32

A arquitetura possui **shares ERC20 estáticas** (`balanceOf`, `totalSupply`) e **assets do aToken** (`_AToken.balanceOf`, `scaledBalanceOf`, `scaledTotalSupply`); a relação de conversão depende de índice e arredondamento e **não autoriza equiparar numericamente shares e assets**. Em depósitos `_deposit` minta shares; em saques `_withdraw` queima shares, enquanto getters e RewardsController contabilizam accrual, índices e claims. O CVL usa ghosts de soma de saldos, `hooks` de storage e `requireInvariant`, além de summaries `NONDET`/`DISPATCHER`; abstrações podem excluir estados ou induzir prova vacuamente verdadeira.

As **24** propriedades `NOT_STATED` são `CONFIRMED` quanto ao tratamento conservador (não se herda checkmark). As **oito** `VERIFIED` permanecem **INCONCLUSIVE/P1** na reprodução independente:
`8` `singleAssetAccruedRewards`, `9` `totalAssets_stable`, `11` `reward_balance_stable_after_collectAndUpdateRewards`, `12` `totalClaimableRewards_stable`, `15` `getClaimableRewards_stable`, `22` `getClaimableRewardsBefore_leq_claimed_claimRewardsOnBehalf`, `28` `rewardsConsistencyWhenSufficientRewardsExist`, `29` `rewardsConsistencyWhenInsufficientRewards`. O PDF nomeia essas properties, mas corresponde ao commit `ac92951`; o Solidity disponível reflete revisão anterior (upstream `13a0047`), e não foram preservados `erc20.spec`, target/harness completo, bibliotecas AToken/RewardsController e respectivos links. **Resultado histórico não é retirado**, mas sua equivalência ao snapshot não foi confirmada.

`totalClaimableRewards_stable_SANITY`, `getClaimableRewards_stable_SANITY`, testes de `initialize` e testes `sanity` são diagnósticos deliberadamente fortes ou de reachability; `UNMAPPED` nesses casos não deve ser automaticamente substituído por `S6-4` só porque há uma igualdade ou uma falha esperada. O relatório menciona registro prévio dos reward tokens, restrições de sum-of-balances, caso em que reward token difere do aToken e limitação de loops (uma ou duas iterações conforme o caso).

## Project 22 — Popsicle V3 Optimizer: 21

Project 22 **não consta no ZIP**. Fontes recuperadas na branch integrada por GitHub, sob PR #18. Das **12** propriedades `VERIFIED/NO_FINDING` do catálogo — `complete/22/{7,8,9,10,11,12,13,14,15,17,18,19}` — há atribuição nominal na transcrição do relatório pp.7–10, mas não foi possível confrontar visualmente o PDF, o modelo simbólico e a viabilidade conjunta das `requireInvariant`; todas permanecem **INCONCLUSIVE/P1** na revisão independente, sem mudar o dado histórico `VERIFIED`.

`complete/22/{1,2,3}` são FullMath: `mulDiv`/`mulDivRoundingUp`, overflow, truncamento e denominator zero. O relatório declara bibliotecas matemáticas fora do escopo central: são `NOT_STATED`, não herdam 12 checks do otimizador. `incomplete/22/{4,5}` usam `PoolActionsWrapper`: falta ABI getter público `totalSupply()` para o primeiro e referência `to` não declarada no segundo; ambos permanecem **INCONCLUSIVE**. `complete/22/6` não tem assertion ativa, só chama `callBurnAllLiquidity`; e `20,21` têm `assert false` de reachability: `UNMAPPED`, sem finding, `CONFIRMED` documental.

Os seguintes detalhes impedem interpretação superficial: `total_vs_protocol_Fees` (**14**) testa `totalFees0 > protocolFees0` estrito, exceto ambos zero; `liquidity_GE_poolBalance0` (**15**) testa igualdade `==` apesar de “GE”; `balance_vs_protocol_Liquidity` (**7**) verifica apenas **token0**; `zero_totalSupply_zero_owed` (**11**) testa **ambos owed0/owed1**; `empty_pool_state_reverse` (**10**) mede liquidez contra balances **menos owed**, não contra shares diretamente. O pool simplificado não comprova invariantes do Uniswap V3 real.

## Prioridade de intervenção e critérios de fechamento

1. **P0:** avaliar a validade do oráculo de `whoChangesActionsSetState` nas duas instâncias e remover/fundamentar `S3-2` somente após filtragem legítima de métodos.
2. **P1:** reescrever 64 justificativas do Project 1 com função, variável, mapping e contraexemplo **por linha**; corrigir o mapeamento adicional de PoRFeedChange; não declarar evidência individual sobre os oito resultados de Static aToken ou doze resultados Popsicle sem target/model/PDF equivalentes. Completar seis targets genéricos só se houver a evidência histórica, nunca por invenção.
3. **P2:** conservar interpretações localmente sustentadas e `NOT_STATED`, incluindo sondas `UNMAPPED`, mantendo ressalvas de report para execução e assumptions.


**Sem alterações realizadas no catálogo original:** os arquivos produzidos são somente `docs/semantic_review_round2/gaia_review.csv` e `docs/semantic_review_round2/gaia_summary.md`, gerados em área de trabalho isolada. Nenhum PR foi aberto, atualizado ou integrado, e nenhum CI foi disparado (sem alteração remota). Os rótulos propostos aparecem em `bug_label_review` no CSV; `bug_label_catalog` guarda o original.

**Integridade da matriz:** 141 registros de dados, chaves únicas `(project_id, catalog_status, example_id)`, nenhum predicado vazio, decisões restritas a três estados. SHA-256 do CSV: `bd9488051eb32c656fb4acef6d37d95309840393e913ecb0aa516ff65e871ec0`.