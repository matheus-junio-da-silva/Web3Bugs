# AGENTE-04 — RODADA 9 — Evidências CVL2 e contrarrevisão

**Escopo e versão:** 20/10/2026, PR [#42](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/42), branch \`research/cvl2-agente-04\`, HEAD inicial \`06dca368f5f2324da45f156dd9bc206745f11af0\`, baseline imutável \`2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3\`. P15 GHO 116, P12 AAVE V2 26, P2 PoR 15 = **157 propriedades**. Zero equivalência formal demonstrada, zero projetos integralmente migrados.

## Leitura e procedência documental

Antes das mudanças: \`docs/spec_catalog.md\` (blob \`7211e989...\`), \`docs/spec_catalog_workflow.md\` (\`aa6fd641...\`), \`docs/spec_catalog_project_1.md\` (\`fd5ed877...\`), \`docs/standard.md\` (\`df4eefcc...\`); \`results/spec/complete/1/1.spec\` (closure snapshot) e \`incomplete/1/1.spec\` (\`queue2\` ausente); revisão mais recente do PR #42; [PR #48 / painel R8](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/docs/cvl2/coordination/ROUND8_P7_SELECTOR_PILOT.md). Foram consultados os capítulos oficiais [Migration](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), [Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), [Methods](https://docs.certora.com/en/latest/docs/cvl/methods.html), [Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html), [Hooks](https://docs.certora.com/en/latest/docs/cvl/hooks.html), [Statements](https://docs.certora.com/en/latest/docs/cvl/statements.html) e [remappings](https://docs.certora.com/en/latest/docs/prover/cli/packages_and_remappings.html). Catálogo \`complete\` não significa equivalente CVL2.

A [matriz](ROUND9_MATRIX_157.csv) tem 157 chaves individuais e mantém Bug Labels, Property, Target, Result, Detection Outcome e SHA-256 originais. Nesta R9, foram **recalculados a partir de bytes os 157 hashes N.spec e 157 hashes source**, todos iguais ao ledger anterior; 1390 relações históricas correspondem a 1386 chaves globais. Colunas \`source_or_report_fact\`, \`inference\`, \`missing_proof\` permanecem separadas.

## 1. Seis tentativas controladas e sem sobrecontagem

Após verificação de saúde (leitura/escrita isolada \`/tmp\`, Git/Python, solcs e clone clean HEAD), os seis comandos foram realizados em \`/tmp/cvl2-ag04-r9-20261020/scratch\`: \`certora-cli 8.19.0\`, \`--compilation_steps_only\`, \`timeout 65s\`, \`HOME\` isolado e variáveis \`CERTORAKEY\`, \`CERTORA_TOKEN\`, \`CERTORA_API_KEY\` removidas; sem Prover e sem CVL1.

| Registro em [ROUND9_ATTEMPTS.json](ROUND9_ATTEMPTS.json) | Target/escopo | Exit | Classe observada |
| --- | --- | ---: | --- |
| \`p15_original\` | P15/36 byte-idêntica, GhoDiscountRateStrategyHarness | 1 | CVL2_PARSER_ERROR, seis methods sem \`function\`/\`;\` |
| \`p15_candidate\` | P15/36 variante lexical, sem remapping de \`@aave/core-v3\` | 1 | **SOLC_IMPORT_MAPPING_ERROR**, não parser CVL2 |
| \`p12_23\` | P12/23 byte-idêntica, UserConfigurationHarness snapshot 0.6.12 | 1 | CVL2_PARSER_ERROR de methods |
| \`p12_25\` | P12/25 byte-idêntica, UserConfigurationHarness snapshot 0.6.12 | 1 | CVL2_PARSER_ERROR de methods |
| \`p15_candidate_remapped\` | P15/36 derivada + \`--packages @aave/core-v3=node_modules/@aave/core-v3\` | **0** | **CVL2_COMPILE_OK, FRAGMENTO DERIVADO** |
| \`p15_original_remapped\` | P15/36 original + **mesmo remapping e target** da derivada | 1 | CVL2_PARSER_ERROR original |

**Seis tentativas, somente três IDs:** quatro falhas do parser CVL2 em **três originais distintos** (P15/36 duas vezes; P12/23 e /25 uma cada); **um COMPILE_OK de variante derivada P15/36**; **um erro Solidity de import**, excluído dos contadores parser; **154 exemplos AG04 continuam NOT_RUN**. O original P15/36 segue \`COMPILE_ERROR\`; não apaga o exit 1 antigo porque houve sucesso de cópia alterada. Nenhum \`VERIFIED\`, \`SEMANTIC_PROVEN\` ou migrado.

**Evidência arquivada integralmente:** [ROUND9_ATTEMPTS.json](ROUND9_ATTEMPTS.json) guarda os seis comandos, \`stdout_raw\`, \`stderr_raw\`, códigos de saída e SHA256 dos fluxos; [ROUND9_INPUT_MANIFEST.json](ROUND9_INPUT_MANIFEST.json) contém os inputs/target/source hashes. Os logs originais estão preservados sem alterações como strings JSON escapadas. Isso evita confundir falhas de \`solc\` com o parser CVL2.

## 2. P15/incomplete/36: hipótese lexical com diff restrito

Original SHA-256 **\`eee38425eb95100799fe30e8d5913f9593230763733197a3dae5dae95cb0073e\`**; derivada scratch **\`b75fd97e4e5fca063d66079b74db7abe89f2c6a179ed41bc5eda39893d578a8d\`**. Alteração exclusiva: seis entradas de \`methods\` recebem \`function\`, \`external\` e \`;\`, preservando **todos** os \`envfree\`, assinaturas, \`rule limitOnDiscountRate\` e assertion textual. Nenhuma spec derivada foi publicada; a [proposta da R8](ROUND8_METHODS_DIFF_PROPOSAL.md) permanece documentação.

Auditado: [aave/gho-core@ce49fb0c94cfebf0159222ceb288e4f9a55d305f](https://github.com/aave/gho-core/tree/ce49fb0c94cfebf0159222ceb288e4f9a55d305f). O runner \`certora/scripts/verifyGhoDiscountRateStrategy.sh\` L3–20 aponta para **GhoDiscountRateStrategyHarness**, não apenas strategy nominal. A target herda \`calculateDiscountRate(uint256,uint256)\` (\`external pure\`) e quatro getters \`public constant\` (\`view\`); seu próprio \`wadMul(uint256,uint256)\` é \`external view\`. A rule chama \`calculateDiscountRate\` e \`DISCOUNT_RATE()\`; as seis declarações continuam envfree. *Fonte auditada*: \`src/contracts/facilitators/aave/interestStrategy/GhoDiscountRateStrategy.sol\` L15–54, \`certora/harness/GhoDiscountRateStrategyHarness.sol\` L1–9. Os dois helpers matemáticos e outras quatro rules de \`certora/specs/ghoDiscountRateStrategy.spec\` **não** fazem parte do fragmento testado.

**Hashes dos quatro inputs centrais:** harness \`f2d96e04622aeedfbaf08f5fbdf3b1d81012b8fcd192ec4f45879890034d34e0\`; strategy munged \`0ca3b38fb9b994b83272ef44f48c48e8205e817fdbb6e68186f289b31a0b11f5\`; interface \`ba36739805f81276acdf6a1432ed1b33c10d001e6fcfe28d218e8306b1420331\`; \`@aave/core-v3@1.17.2/WadRayMath.sol\` \`fae5b995ec613cc213050c99ea6352c9c18ceebba106d03b1726cfa8f1f0124e\`. Cenário usa os pacotes autenticados em R5; remapping explícito elimina um erro de resolução de import sem alterar Solidity/CVL. A original com a **mesma** flag falhou no parser, a derivada completou compilação.

**Missing proof:** equivalência de contexto full-spec vs fragmento, flags exatas do runner auditado, static check \`envfreeFuncsStaticCheck\`/\`envfreeFuncsAreNonpayable\`, resolução de receptor de funções herdadas, reverts/arredondamentos de WadRayMath, universo de contraexemplos e eventuais summaries. Patch GHO de \`GhoToken\` acrescenta \`require\` e estado \`isLabelNonempty\`, mas não modifica diretamente strategy/harness nos quatro imports desta família; não extrapolar a outros GHO.

## 3. P12/23 e /25: original reproduzido, ABI histórica diferente

N.spec hashes: P12/23 **\`a8b6271f0d0d5030fbe78e48becf28c1a66ad6754f70e5a9e722cf4690449560\`** e /25 **\`b91c97498f1b60f7664e279ca1520193c03644887463df4df7145a64ce85876b\`**; harness snapshot SHA \`0bbda4db0ee80986a3c63672d50bd5858ab7fe62cb7a28d440a0e7320846c116\`. Ambas as cópias originais em cenário snapshot solc 0.6.12 deram **exit 1 parser** sem mudança de regra.

No commit auditado [aave/protocol-v2@750920303e33b66bc29862ea3b85206dda9ce786](https://github.com/aave/protocol-v2/tree/750920303e33b66bc29862ea3b85206dda9ce786), \`specs/harness/UserConfigurationHarness.sol\` L12–43 aceita \`address user\` adicional nos setters e getters, enquanto snapshot não. O wrapper auditado opera em um só mapa \`usersConfig\` e não usa \`user\` no corpo — **fato da fonte** — mas a spec global quantifica o endereço e usa ABI distinta. Source global tem sete methods, quatro invariants e quatro rules, versus N.spec extraídos com dois methods e uma rule. **Inference:** uma projeção de storage poderia coincidir, porém selectors, quantificação, env/caller e reverts não foram provados equivalentes. Não substituir o wrapper nem adicionar casts/requires para fazer compilar.

P12 VariableDebt 10–18 continua 2/9 regras somente lexicalmente similares ao auditado e sete divergentes, sem \`POOL\` closure; StableDebtToken depende de harness/construtor histórico ainda ausente.

## 4. P2: receiver Chainlink e summary histórico não recuperado

Git [Certora/aave-proof-of-reserve@12296ce4c6f9bde6663e1baa02cf19f179c1048b](https://github.com/Certora/aave-proof-of-reserve/tree/12296ce4c6f9bde6663e1baa02cf19f179c1048b) fixa via gitlinks \`chainlink-brownie-contracts@1d301b43d374a23524eca878ffc4f9b1cf8a93d7\`, \`solidity-utils@723cf9a0dbc11486910594327178b9501e646c20\` e \`aave-address-book@a75e2044531136c45c6ce3cd54cda54da1102ce4\`; \`foundry.toml\` blob \`8255763df6ab3a6a6d1e0f794c4a709b366ff106\` contém remappings. Interface \`AggregatorV3Interface.sol\` SHA-bloco Git \`cd72a0c0b928f23e0d40fe1d5db985099e15c810\` oferece \`latestRoundData() external view\` com cinco retornos. O \`ProofOfReserveAggregator.sol\` L108–118 recebe esse valor de **\`AggregatorV3Interface(feedAddress)\` externo**, e \`IERC20(totalSupplyAddress).totalSupply()\` é outra chamada externa.

CVL1 \`contracts/2/specs/aggregator.spec\` tem \`latestRoundData() => NONDET\` sem receiver explicitado; em CVL2 um summary \`currentContract\` pode perder chamadas externas e \`_.\` pode ampliar a abrangência. Política exata entre \`UNRESOLVED\` e \`ALL\`, runner e harness CVL histórico não autenticados. **Não criar mock, summary, getter nem wrapper especulativos**. P2=15 casos **NOT_RUN**.

## 5. Contrarrevisão PR #40 e #46 — SOMENTE LEITURA

**[PR #40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40)** HEAD \`d9e8e668a92dd468a5e676e1e6ef7d284affab78\`, Draft. R8 piloto **do coordenador**, publicado por #48, testou variantes de P7/47 e P7/73 com seis prefixos \`sig:\` e ambas compilaram (exit 0), mas seus originais já tinham parser errors; em P7/47 houve fallback autofinder. Há potencial vacuity em \`method f\`, \`f@withrevert\`, ABI dos dois tokens e CVL global (hooks/ghosts) não reconstruída. **Não atribuídas essas execuções ao AG04**.

**[PR #46](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/46)** HEAD \`62754c10e3e9dc23d122aad3333eac2ec60f817d\`, Draft. P19/1,2 derivadas \`mathint\` seguem \`02_unresolved\`: \`RCPT=0\` possível, segunda divisão por zero, diferença entre coerção CVL1 e \`mathint/0\` CVL2 não provada. Relação entre duas assertions para \`RCPT>0\` não demonstra equivalência entre versões; não alterar require, assert ou casts.

## Próximas experiências a deliberar, sem execução agora

1. **P15/36 full spec:** fixar as duas funções CVL auxiliares, cinco rules, receiver de funções herdadas e static checks envfree; então autorizar apenas um novo \`--compilation_steps_only\` de spec global autenticada, com hash/cmp, flags históricos e teste de contraste com derivada R9 exit0.
2. **P12/23 antes de /25:** coordenador escolher explicitamente domínio/ABI auditado com \`address user\` ou snapshot sem user, seu harness, invariants e caller; só então permitir variante de sintaxe individual em scratch, sem alterar \`require reserveIndex < 128\` ou corpos Solidity.

**Sem** Prover/CVL1, aceitação semântica, projeto integralmente migrado, mock ou merge de implementação.

**AGENTE-04 — RODADA 9 / EVIDÊNCIAS, TESTES CONTROLADOS E CONTRARREVISÃO**
