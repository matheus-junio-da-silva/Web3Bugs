# FAROL — Auditoria semântica cruzada / rodada 2

Data: 2026-10-18. Escopo: **173 propriedades** (AAVE V3 74; AAVE V2 26; Compound 41; Furucombo IDs 97–128 32).

## Procedimento e integridade

Conferidos os 173 arquivos originais extraídos .spec, regras completas e invariantes, requires, static_requires, métodos, ghosts/axioms, helpers, snapshots e resumos; comparados ao N.md correspondente e às citações Solidity. Fontes históricas intactas. Os PDFs foram abertos e texto extraído diretamente dos binários SHA-256 listados abaixo. Sem execução do Certora Prover, sem prova atual, sem demonstração de equivalência de versão do Solidity.

As decisões se referem à **classificação/interpretação em cada exemplo**, não à correção operacional dos contratos. CONFIRMED = predicado/label sustentáveis na fonte observável; CORRECTION_REQUIRED = erro específico de label ou interpretação a corrigir após aprovação; INCONCLUSIVE = histórico/target/assumptions insuficientes para endossar um vínculo mais forte. Result não é Detection Outcome nem completude estática.

## Resultado quantitativo

| Projeto | IDs | Total | CONFIRMED | CORRECTION_REQUIRED | INCONCLUSIVE | Result VERIFIED | Result NOT_STATED |
|---|---|---:|---:|---:|---:|---:|---:|
| 7 — AAVE V3 | 1–74 | 74 | 64 | 5 | 5 | 18 | 56 |
| 12 — AAVE V2 | 1–26 | 26 | 17 | 0 | 9 | 21 | 5 |
| 17 — Compound Money Market V2 | 1–41 | 41 | 31 | 0 | 10 | 9 | 32 |
| 10 — Furucombo — handlers 97–128 | 97–128 | 32 | 0 | 0 | 32 | 0 | 32 |
| **TOTAL** | — | **173** | **112** | **5** | **56** | **48** | **125** |

## Correções propostas (não aplicadas)

- **P7 #6 additiveMint** — S6-4 → S6-4. The mint calls on a and b occur sequentially within ONE CVL execution, not via restoration of initialStorage; document this alias/order limit before equating to two independent worlds.
- **P7 #47 disallowedFunctionalities** — SC → S5-2. Forbidden debt-token ERC20 entrypoints are access/operation restrictions (S5-2), not an unclassified implementation-specific SC pattern; the filtered set explicitly includes allowance getter.
- **P7 #68 additiveMint** — S6-4 → S6-4. Literal rule additiveMint is correct but its assert message says "burn is not additive"; do not describe a burn call. Keep accounting category provisionally (L2 requires an established rounding root cause).
- **P7 #73 disallowedFunctionalities** — SC → S5-2. Forbidden debt-token ERC20 entrypoints are access/operation restrictions (S5-2), not an unclassified implementation-specific SC pattern; the filtered set explicitly includes allowance getter.
- **P7 #74 getReserveNormalizedVariableDebtCheck** — S3-2 → S6-2. The observable assertion compares two return values of getReserveNormalizedVariableDebt after supply, not a direct storage write. Prefer unexpected getter value S6-2 absent a proven state-update root cause.

## Verificações técnicas por projeto

### Project 7 — AAVE V3
- O PDF indica o commit histórico a87d546 e hipóteses de juros sem acumulação, hash determinístico, unrolling e efeitos externos resumidos. O snapshot posterior não é automaticamente a versão verificada.
- Getter de índice (exemplo 74): o predicado é condicional a dívida anterior não nula; S6-2 é candidato mais específico que S3-2 enquanto não demonstrada uma escrita incorreta. As regras de mint/burn/transfer com bounded_error_eq codificam tolerâncias; L2 somente com testemunho de erro de precisão, não por nome.
- Regras de assinatura, supply, flags e setters receberam precondições/asserções individuais no CSV; não foram consideradas provadas pela tabela genérica do PDF. Os invariantes sobre ghosts e summaries exigem cuidado especial.

### Project 12 — AAVE V2
- Os 9 casos StableDebtToken usam harness de construtor incompatível com a implementação fornecida; a rubrica ✔* em PDF significa versão simplificada ignorando arredondamento. Não reinterpretamos VERIFIED histórico como execução recompilável sobre o snapshot.
- Em additiveMint #6, o CVL requer taxa estável inicial zero e usa initialStorage; o achado histórico de arredondamento a taxas elevadas não pode ser identificado automaticamente com este contraexemplo. Os resultados e outcomes históricos permanecem distinguíveis.
- As regras de VariableDebtToken e UserConfiguration foram avaliadas por tipo de assertion; condições de retorno de getters são S6-2, de setter/estado S3-2, de aditividade potencialmente L2 apenas quando causalidade por precisão é demonstrada.

### Project 17 — Compound Money Market V2
- compound.cvl contém operações da API histórica V1 (por exemplo _setOriginationFee e supply(address,uint256)), sem target MoneyMarket V1 no snapshot. Não substituímos Comptroller/CToken V2 como prova de execução.
- Regras frame_* #22–38 incluem method f sem filtro de não-mutação, exigindo old == new; elas são testes diagnósticos potencialmente falsificados por operações válidas. Preservação de UNMAPPED é intencional, não confirmação de bugs.
- Alguns blocos de accounting incluem assertions distintas para códigos de erro, saldos e reservas; S6-2, S3-2 ou S6-4 só podem ser atribuídas a uma falha concreta. A documentação registra as fórmulas, sem inventar um único root cause.

### Project 10 — Furucombo / IDs 97–128
- São oito handlers × quatro regras (stack, aprovação temporária, movimento de tokens, isolamento de terceiros). As quatro fórmulas originais foram verificadas com os helpers e as condições require; uma repetição por handler não prova a compilação para aquele target.
- A tabela do PDF informa resultados de inspeção por handler (incluindo None e 🔎), não prova VERIFIED individual. Scripts e Solidity 2021 podem estar ausentes; código atual com imports externos também não demonstra equivalência de versão.
- Em tokenMovementCorrectness, as duas implicações não exigem sem precondições que todos os saldos sempre tenham deltas exatos. Em noOtherPartyModified, os aliases de token e exclusões de somebody delimitam a garantia. Todo Resultado/Outcome foi mantido NOT_STATED.

## Evidência histórica — hashes dos PDFs lidos

- P7: resources/7/AaveV3Jan2022-1.pdf — 8 páginas, SHA-256 ddb5d098bcb5770a0ab78ac756cf84996f1e7c33b1817ec921bf6ba2a251acc9.
- P12: resources/12/AaveV2Dec2020.pdf — 25 páginas, SHA-256 83b8f4e29a5d17b2cb6af45a87bf78da5695a7c6a7c57f129e5b989ae6132143.
- P17: resources/17/CompoundMoneyMarketV2Aug2019.pdf — 47 páginas, SHA-256 cb48b1c159df4ef3d603f84afc2e7fa9da6c2c0b72f9760e6d962807f4177a1a.
- P10: resources/10/FurucomboMay2021.pdf — 31 páginas, SHA-256 a42e33196f3bdadb7df52c5554aca0e2d15d7aaa517b42db118db015b278d769.

## Limites de confiança e próximos passos

- Não foram executados certoraRun nem scripts que reconstituam a cadeia de transformação/harness 2019–2022. A decisão INCONCLUSIVE deve permanecer até que sejam obtidos ABI e versão históricos do target e haja uma correspondência de resultado para a exata assertion.
- O PDF é autoridade apenas para as propriedades e targets do relatório; o arquivo PDF original, os .spec, N.md, bug labels atuais e results/bugs.csv não foram alterados.
- A matriz oferece expressão literal de cada assertion/invariant, requires do bloco, axioms/summaries, alvo histórico, referência Solidity, tipo de contraexemplo falsificante, label atual/proposto, Resultado e Outcome separados, páginas e SHA do PDF e decisão.

## Validação dos artefatos

- Linhas de dados CSV: 173; IDs únicos: 173; correspondência literal fonte → extração: 173/173.
- Decisões: CONFIRMED=112, CORRECTION_REQUIRED=5, INCONCLUSIVE=56.
- Alterações previstas: apenas os dois arquivos de revisão nesta pasta; não haverá merge automático.
