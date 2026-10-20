# Rodada 7 — revisão independente e gate de merge, 20/10/2026

Esta análise refere-se ao dataset `Web3Bugs-certora` (base histórica `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`). A catalogação preserve `results/spec`, `contracts` e `results/spec/spec_buglabel.csv`. O CSV histórico contém **1.390 linhas de relações Bug Label** referentes a **1.386 propriedades individuais** de **23 projetos**.

## Indicadores

| Porta | Numerador / denominador | Significado |
| --- | ---: | --- |
| Matrizes individuais Round 7 reconciliadas ao catálogo | **1.386 / 1.386 (100%)** | 8 matrizes com 8 commits SHA40 e campos históricos comparáveis sem divergências; não assegura semântica |
| Projetos com pesquisa documentada | **23 / 23 (100%)** | Há blocker por propriedade e source de origem |
| CVL2 `--compilation_steps_only` com exit 0 | **4 / 1.386 (0,29%)** | P7/37,65 fragmentos no snapshot; P19/1,2 derivados `mathint`, não históricos byte iguais |
| CVL2 parser/typecheck com exit 1 atribuível à spec | **12 / 1.386 (0,87%)** | Cinco P7, dois P10, dois P12, um P15, dois P18; log P15/36 verificado na R6 |
| Sem execução CVL2 válida observada | **1.370 / 1.386 (98,85%)** | Zero provas atribuíveis a estes casos |
| Equivalência semântica histórica CVL1→CVL2 demonstrada | **0 / 1.386** | Nenhum caso com domínio/summaries/harness/runners/prova preservados |
| Projetos integralmente migrados e formalmente validados | **0 / 23** | Não confundir `complete` histórico com migração |

Arquivos: [ROUND7_PROGRESS.csv](ROUND7_PROGRESS.csv), [ROUND7_COMPILATION_OBSERVATIONS.csv](ROUND7_COMPILATION_OBSERVATIONS.csv), [checker](../../../scripts/check_cvl2_round7_progress.py). Uma reconciliação independente em memória dos dados obtidos pelo conector GitHub verificou **23 projetos, 1.386 chaves únicas, 1.390 relações, 8 HEADs, 4/12/1.370 resultados e zero inconsistências**; teste negativo em memória detectou contador P1 artificialmente inflado. O workflow adicional `cvl2-ledger-integrity` no PR de coordenação executa os verificadores Python reais e falha deliberadamente com uma cópia falsificada dos dados; seu status deve ser checado, sem presumir aprovação prévia.

## Achados significativos da Rodada 7 por agent

| Agente e PR | Pesquisa nova / evidência | Bloqueio |
| --- | --- | --- |
| [01 — #39](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/39), P10 266 | Inventário de **13 method literals ativos** vs 15 em comentários, matrizes LibParam 33/34, seleção HMaker 11 e famílias Registry/Proxy 29 | ABI pós Perl, `stack_slot`, receivers e scripts completos |
| [02 — #37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37), P18 181 | Manifest de blobs Git para 181 N.spec, análise dos cinco casos P18/3,4,23,46,53 e métodos públicos | Runner auditado e escolha internal/external / summaries; dois parser failures anteriores sem novo teste |
| [03 — #36](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/36), P24 164 | Comparação matemática de guarda LaunchEvent: `b>=r` e `b-v>=r` NÃO são equivalentes; testemunha `b=100,r=80,v=30` | Fork posterior/patch, Staking, Owner.sol e runner exato |
| [04 — #42](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/42), P2/12/15 157 | Seis métodos P15/36 associados a ABI/mutabilidade, distinção de feed Chainlink externo P2 e parâmetro `user` do harness P12 | Nenhum novo parser test; P15/36 erro da R6; receiver e semântica CVL1 desconhecida |
| [05 — #40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40), P3/6/7/19/21 148 | Análise de selector `sig:`, `method f` e `@withrevert`, separa P7/47 e /73, preserva P19 zero divisor | Variante `sig:` nunca compilada; não inferir não-vacuidade |
| [06 — #38](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/38), P1/4/17/22 159 | Cinquenta/blobs e provenance temporal bridges junho/setembro, `munged` P4, Specify 2019 e wrappers Popsicle por família | Snapshot Solidity não é cena de prova; recuperação WSL requerida |
| [07 — #41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41), P8/9/11/20 156 | W1 em 22 specs e W2/W3 P8 como contradição matemática, P9 Mento-core, five patches BentoBox e MAX_INT | Não se demonstrou escopo/resultado do Prover; sem proxies históricos |
| [08 — #43](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43), P5/13/14/23 155 | **Nova branch pública Certora Radicle** com harnesses/drivers; P14 arrays `[0]` e getExcessCollateral pós patch | Branch posterior à auditoria, CVT geração e cena auditada ausentes; `solc` ABI não é CVL2 |

### Condição de merge

**Documentação de pesquisa** pode ser integrada somente se arquivos permanecerem documentais, sem modificar originais, os 8 workflows de CI estiverem verdes, o conteúdo não afirmar semântica/prova indevidas, o checker de progresso passar com caso positivo e negativo, e houver revisão de autoria/escopo. Merge de documentação **NÃO** significa aceite de uma migração de código.

**Migração formal/derivados `results/cvl2`** exige individualmente: fonte e hash, target e ABI, fonte CVL global + dependências, flags/harness, `--compilation_steps_only`, casos de revert, satisfatibilidade/vacuity, e evidência suficiente da equivalência de significado CVL1/CVL2. Hoje **nenhum caso possui o conjunto completo**; o [PR #46](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/46) permanece `02_unresolved` sem promoção. Não há base para merge de implementação nem para marcar projeto como 100% migrado.

## Incidente de infraestrutura

Até a recuperação atestada do WSL [incidente R6](ROUND6_WSL_IO_INCIDENT.md), **nenhum** agente deve iniciar novas compilações/alterações no volume instável. Pesquisas remotas e QA de dados pelo GitHub podem continuar, sem usar `SIGBUS`/`EROFS` como resultado de CVL2. A coordenação realiza apenas checks de leitura e CI em runner GitHub controlado.
