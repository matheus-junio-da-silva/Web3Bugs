# AGENTE-04 — RODADA 5 — QUALIDADE CVL2

Data 2026-10-20. Base imutável: 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. Branch research/cvl2-agente-04, PR #42 Draft. Trabalho em worktree separado de HEAD dc5f710; não houve reset, edição de source ou merge. Painel de coordenação PR #47, ROUND4_DASHBOARD.md e ledger por 23 projetos conferidos antes de editar.

## Resumo da matriz

A matriz ROUND5_PROGRESS.csv tem 157 linhas com chaves únicas (Project ID, original Status, Example ID): P15 116/116 incomplete, P12 17 complete + 9 incomplete, P2 1 complete + 14 incomplete. As 157 fontes .spec e 157 N.spec, N.md e N.sol existem; os 139 N.txt de incomplete foram inspecionados quanto à existência. Cada linha retém propriedade, target, resultado histórico, Detection Outcome, SHA-256 da fonte e N.spec, prioridade, ABI, closure, status real e próximo gate. O CSV canônico não foi alterado.

| Indicador | Resultado da rodada 5 |
| --- | ---: |
| Casos documentados | 157 |
| DOCUMENTED_CANDIDATE históricos, hipóteses apenas | 18 (P12 17, P2 1) |
| Certora compilation_steps_only EXECUTADOS | 2 |
| Certora compile-only EXIT 0 | 0 |
| Certora compile-only EXIT 1 | 2 (P12/complete/23 e 25) |
| ABI solc do UserConfigurationHarness snapshot | EXIT 0 |
| ABI solc do GHO com bundles autenticados | 3 cenários EXIT 0 (sem Certora) |
| SEMANTIC_PROVEN | 0 |
| MIGRATED_COMPLETE | 0/3 projetos |
| Prover, CVL1, derivados results/cvl2 | 0 |

Status laranja: documentação, import closure e ABI melhoraram, mas nenhuma equivalência CVL1 para CVL2 foi demonstrada. Estrutura 100% não significa migração 100%.

## Resultados por exemplo e família

P12/complete/23 setBorrowing e P12/complete/25 setUsingAsCollateral: cópias N.spec byte-idênticas, target UserConfigurationHarness do snapshot, CLI Certora 8.19.0 e solc 0.6.12. ABI snapshot compilou; ambas as specs falharam no typechecker CVL2 pela falta de palavra function e terminador ; em methods, linhas 5 e 6. Os argumentos address user existem no harness auditado e não no snapshot; as fontes não constituem a mesma cena. Nenhuma spec foi alterada para satisfazer o parser. Consulte P12_TARGET_ABI_AND_DIAGNOSTICS.md e evidence/p12_23_compile.log, evidence/p12_25_compile.log.

P12/complete/10–18: duas rules têm similaridade lexical com upstream, sete diferem; linking POOL, seletores, reverts e contexto não comprovados. P12/incomplete/1–9: StableDebtTokenHarness auditado depende do construtor de cinco parâmetros, enquanto o snapshot usa initialize e getter incompatíveis. Nenhuma substituição.

P15: pacote auditado aave/gho-core@ce49fb0 com @aave/core-v3@1.17.2. Três tarballs baixados e autenticados por SHA512 SRI/ SHA256; cinco scripts históricos, 284 arestas de import estáticas e zero paths ausentes nas cópias reconstruídas. Patch original aplicado em scratch, novos requires e mudança external para public identificados; ABI solc de GhoToken original (30), GhoToken patchado (30), GhoTokenHarness (37) e GhoDiscountRateStrategyHarness (6) gerada. Isso não autentica o ambiente Certora, settings e ghosts. Consulte P15_PACKAGE_IMPORT_CLOSURE.md.

P2: quatro Solidity do commit 12296ce4 são byte-idênticos no snapshot. O tree auditado contém 99 paths e nenhum .spec, .conf ou harness CVL. A regra complete/1 PoRFeedChange depende de summary latestRoundData que opera sobre receiver do feed externo, não função do Aggregator; ABI e bibliotecas externas do job não fechadas. Outros 14 exemplos sem dummies e helpers. Consulte P2_ABI_AND_NEGATIVE_SEARCH.md.

## Tabela de fontes e linhas

| Fonte imutável | Linhas/ocorrência | Significado |
| --- | --- | --- |
| results/spec/complete/12/23.spec | L4–7 methods, L9–15 rule | typechecker CVL2 EXIT 1 em L5/L6 |
| results/spec/complete/12/25.spec | L4–7 methods, rule seguinte | typechecker CVL2 EXIT 1 em L5/L6 |
| contracts/12/specs/harness/UserConfigurationHarness.sol | L15–36 | funções public sem address user |
| aave/protocol-v2@7509203/specs/harness/UserConfigurationHarness.sol | L12–44 | assinaturas adicionais com address user |
| aave/protocol-v2@7509203/runUserConfigCLI.sh | L1 | runner histórico solc6.8 literal, binário não autenticado |
| aave/gho-core@ce49fb0/package-lock.json | packages node_modules/@aave/core-v3 | versão 1.17.2 fixada com SRI |
| aave/gho-core@ce49fb0/certora/applyHarness.patch | hunks GhoToken antigo L75–147 | require, isLabelNonempty, external para public |
| aave/gho-core@ce49fb0/certora/scripts/verify*.sh | certoraRun, --link, --verify | 5 famílias de cena |
| contracts/2/contracts/ProofOfReserveAggregator.sol | L3–8 imports; L21–35 getters; L89–122 feed | chamada Chainlink feed.latestRoundData |
| contracts/2/specs/aggregator.spec | L1–16 methods; L18–28 helper; L35–54 rule | CVL1 summary global exige decisão de receiver |
| Certora/aave-proof-of-reserve@12296ce4 | tree Git 99 paths | zero specs ou harness Certora visíveis |

Referências oficiais: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html e https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html. O manual indica function e ; em methods e alerta que resumos CVL1 globais não equivalem ao receiver corrente CVL2. A presença de ABI nem a compilação somente sintática resolve essas diferenças.

## Gates para o coordenador

P12: selecionar qual versão da source/harness define o domínio da rule e, caso a caso, se futuramente autoriza cópia derivada. P15: adjudicar target principal dos scripts versus target catalogada, imports/links completos, patch com requires e cena CVL global antes de cada novo compile-only. P2: recuperar as specs originais, dependências externas, dummies, receivers e settings. Sem esses insumos, bloqueio documental é resultado legítimo; não se fabricam wrappers.

Auditoria cruzada somente leitura de #40/#46 incluída em CROSS_AUDIT_PR40_46.md. Nenhum desses dois PRs foi editado.

**AGENTE-04 — RODADA 5 — QUALIDADE CVL2**
