# CERES — revisão independente de proveniência | Project 15 — GHO Core

**Data:** 2026-10-18. **Escopo:** documentação de revisão; não é novo Project ID, não é reprodução do Certora Prover e não altera a branch Helix.  
**Helix:** `catalog/p15-helix-gho-core`, HEAD observada `3df3a898d06f0cdfbe51ccd40f75ff5ca1701164`; naquele instante ainda não havia PR GHO Core ou arquivos `contracts/15` no snapshot dessa branch.  
**Branch desta evidência:** `review/ceres-p15-gho-core-provenance`, derivada da `main` `eba10cbb6a37ba5230bda307cdf9105ba72489dc`, sem PR ou merge.

## Evidências e identificadores de origem

1. Fonte fornecida: [PropertyGPT — certora_projects/gho-core](https://github.com/matheus-junio-da-silva/PropertyGPT/tree/main/certora_projects/gho-core), tree `687f654c679ed45ab127b7949e2a29c8f5e491b9`; inventário **33 arquivos**.
2. Relatório externo candidato: [Certora — GHO Stablecoin, 7 de março de 2023](https://www.certora.com/reports/aave-gho); [PDF CDN, 13 páginas](https://certora.cdn.prismic.io/certora/a227c693-7aa3-471f-a7b2-7148c06a2110_Aave_Gho_Formal_Verification_Report.pdf). **O PDF não consta no diretório PropertyGPT.** Também existe PDF no repositório original, [FormalVerificationReportForAavesGHOToken.pdf](https://github.com/aave/gho-core/blob/ce49fb0/certora/reports/FormalVerificationReportForAavesGHOToken.pdf), blob `b1ee9100ad6373633d42f004dd46654512f3d796`. Não foi verificada igualdade byte a byte entre os dois PDFs; ambas as proveniências devem ser registradas.
3. Revisão auditada explicitamente declarada no PDF: [aave/gho-core@ce49fb0c94cfebf0159222ceb288e4f9a55d305f](https://github.com/aave/gho-core/tree/ce49fb0c94cfebf0159222ceb288e4f9a55d305f), atividade de 30/01 a 28/02/2023; targets enumerados: `GhoToken.sol`, `GhoDiscountRateStrategy.sol`, `GhoInterestRateStrategy.sol`, `GhoAToken.sol`, `GhoVariableDebtToken.sol`, `GhoFlashMinter.sol`, `GhoOracle.sol`.

## Correspondência de versões / resultado da comparação por Git blob

Comparei todos os arquivos de `PropertyGPT/certora_projects/gho-core/` com `aave/gho-core@ce49fb0`, mapeando os Solidity para `src/contracts/` e as specs para `certora/specs/`. **31/32 arquivos comparáveis idênticos**, mais `.DS_Store` (1 arquivo sem contraparte upstream). A única divergência entre código/spec é:

| Fonte | Git SHA-1 | Tamanho | Declarações ativas |
| --- | --- | ---: | ---: |
| PropertyGPT `ghoDiscountRateStrategy.spec` | `8bee3f5dba4285d4ebb01e9c9044577fe51a8957` | 677 B | 1 |
| Upstream auditado `certora/specs/ghoDiscountRateStrategy.spec` | `809aed55ed67807a88544a3375868ef460bdf641` | 3.727 B | 5 |

Os 31 demais, incluindo **todos os Solidity dos sete targets** preservados e as **outras oito specs**, têm SHA de objeto Git idêntico ao mesmo commit histórico. Evidências: `GhoToken.sol` `cc3c999a93c27499d1943b3e24170a0beb12638d`; `GhoVariableDebtToken.sol` `c309318286d2dccc604f2149fbbcc08b29b55d68`; `ghoVariableDebtToken.spec` `f4ad68107de3572f5b21559893a8a55bb6861ba8`. **É uma correspondência de bytes de source code, não uma prova de equivalência do ambiente executado.**

As cinco regras ativas da spec histórica de desconto eram:
- `equivalenceOfWadMulCVLAndWadMulSol`;
- `maxDiscountForHighDiscountTokenBalance`;
- `zeroDiscountForSmallDiscountTokenBalance`;
- `partialDiscountForIntermediateTokenBalance`;
- `limitOnDiscountRate`.

PropertyGPT preservou apenas `limitOnDiscountRate`. O relatório enumera #30 (maxDiscount…), #31 (zeroDiscount…) e #32 (limitOnDiscountRate). **#30 e #31 não são source rules ativas do snapshot**, embora apareçam no original auditado. Não fabricar exemplos para elas como se estivessem na fonte; documentar exclusões/diferença e solicitar decisão de escopo ao orquestrador.

## Cruzamento das 71 propriedades do PDF com source rules ativas

Contagem obtida lendo os `rule` e `invariant` não comentados de **todas as nove specs** fornecidas e comparando seus nomes aos 71 itens da tabela histórica. É reconciliação de identificação nominal, não aprovação coletiva de prova.

| Família do relatório | Índices | Coincidências com source ativa |
| --- | --- | ---: |
| GhoVariableDebtToken | #1–29 | 26/29 |
| GhoDiscountRateStrategy | #30–32 | 1/3 |
| GhoToken | #33–58 | 24/26 |
| GhoAToken | #59–65 | 7/7 |
| GhoFlashMinter | #66–71 | 6/6 |
| **Total** | **71 itens** | **64/71** |

As sete entradas **sem source rule ativa correspondente no PropertyGPT**:

| PDF | Propriedade | Evidência / tratamento |
| --- | --- | --- |
| #3 | `onlyRebalanceCanUpdateUserDiscountRate` | CVL **comentada** em `ghoVariableDebtToken.spec:139`. O PDF marca ❌ e associa finding Low de timelock; após `81bb51b` a restrição foi descontinuada. Registrar finding histórico **sem atribuir VIOLATED a rule ativa inexistente**. |
| #14 | `integrityOfMint_cantDecreaseInterestWithMint` | CVL **comentada** desde `ghoVariableDebtToken.spec:407`. PDF indica timeout ⏱, não VERIFIED/VIOLATED. |
| #21 | `integrityOfUpdateDiscountDistribution_discountRate` | CVL **comentada** a partir de `ghoVariableDebtToken.spec:538`; a marca ✔ do PDF não torna a source ativa. |
| #30 | `maxDiscountForHighDiscountTokenBalance` | Ausente da spec de desconto PropertyGPT; presente apenas no arquivo upstream auditado. |
| #31 | `zeroDiscountForSmallDiscountTokenBalance` | Mesmo impedimento de #30. |
| #57 | `OnlyFacilitatorManagerAlterFacilitatorExistence` | Só no relatório, não há rule/invariant ativa de mesmo nome no snapshot. |
| #58 | `OnlyBucketManagerCanChangeCapacity` | Só no relatório, não há rule/invariant ativa de mesmo nome no snapshot. |

**Regras sem resultado de relatório:** todas as regras ativas adicionais não listadas no PDF, como checks auxiliares/diagnósticos de `VariableDebtToken.spec`, `set.spec`, `ghoToken.spec` ou `integrityOfMint_updateScaledBalance_fixedIndex`, permanecem **`Result = NOT_STATED`**; não herdar status de regra parecida ou de um ✔ agregado.

**64 possíveis associações individuais:** podem receber `Result = VERIFIED` onde (1) o nome coincide, (2) há correspondência de corpo e semântica, (3) o target e a configuração histórica são os corretos, (4) a marca individual ✔/✔* do PDF é corroborada. `disallowedFunctionalities` e `burnZeroDoesntChangeBalance` surgem na **spec importada** `VariableDebtToken.spec`, não diretamente em `ghoVariableDebtToken.spec`: requer rastrear import/driver. Não declarar as 64 VERIFIED automaticamente sem revisão item a item. `Detection Outcome` precisa de evidência própria; um ✔ não é finding. Preserve assumptions e `✔*` nas descrições.

### Divergência material em #54

O PDF na página 11 descreve `balance_after_burn` como aumento do saldo e do `totalSupply`, mas `ghoToken.spec:425–438` contém `initBalance == finBalance + amount` e `initSupply == finSupply + amount` (**diminuição**). `gho/GhoToken.sol:58–66` implementa `_burn(msg.sender, amount)`. A prosa do relatório não pode ser usada literalmente para explicar essa assertion. Documente divergência, e se a associação semântica estrita não for provada, classifique o resultado daquela source rule de modo conservador `NOT_STATED`, mesmo que o item nominal do relatório tenha ✔. Não modificar a assertion histórica.

## Drivers e harnesses originais não copiados — dependências relevantes

No commit oficial `ce49fb0` existem **29 arquivos sob `certora/`**, entre eles:
- `certora/harness/ghoVariableDebtTokenHarness.sol`, `GhoTokenHarness.sol`, `GhoDiscountRateStrategyHarness.sol`, `DummyPool.sol`, `DummyERC20WithTimedBalanceOf.sol`, `MockFlashBorrower.sol`, vários DummyERC20;
- `certora/scripts/verifyGhoVariableDebtToken.sh`, `verifyGhoToken.sh`, `verifyGhoAToken.sh`, `verifyGhoDiscountRateStrategy.sh`, `verifyFlashMinter.sh`;
- `certora/Makefile`, `certora/applyHarness.patch` e PDF em `certora/reports/`.

Esses itens estão ausentes do snapshot PropertyGPT de 33 arquivos. Drivers executam sob `certora/munged/`, gerado pelo Makefile aplicando patch; `applyHarness.patch` modifica `GhoToken.sol` e inclui workaround CERT-977 (`isLabelNonempty`, entre outros). Os mocks, links e transformações são parte **material da semântica verificada**.

**Exemplos da configuração auditada:** `verifyGhoVariableDebtToken.sh` usa `GhoVariableDebtTokenHarness`, `DummyPool`, `DummyERC20WithTimedBalanceOf`, `--link` de `POOL`/`_discountToken`/`_discountRateStrategy`, `--solc solc8.10`, `--loop_iter 2`, `--optimistic_loop` e timeouts/profundidade. `verifyGhoToken.sh`: `GhoTokenHarness`, `--loop_iter 3`, workaround CERT-1060. `verifyFlashMinter.sh`: `MockFlashBorrower` mais contratos munged, `-contractRecursionLimit=1`. O snapshot não demonstra fechamento de construção de nenhum desses targets de harness; **não classificar como complete pela simples existência do .sol base ou declaração methods**.

O relatório explicita assumptions: Aave V3 Pool funciona corretamente, referências por setters já inicializadas, loops desenrolados com limite 2, valores 18 casas WAD / índice 27 RAY / percentuais BPS. Não houve replay do Certora Prover ou compilação do ambiente histórico nesta revisão.

## Veredito independente e providências

- **Origem do relatório / versão de Solidity:** correspondência **confirmada para 31/32 arquivos comparáveis** do snapshot a `ce49fb0`; original PDF existe externamente e no repositório auditado.
- **Specs e targets completos:** **não**, pois spec de desconto foi reduzida e os harnesses, drivers, mocks, ligações, patch e relatório estão fora da pasta PropertyGPT. As sete discrepâncias nominais exigem tabela própria.
- **Fidelidade formal histórica:** **não revalidada**. Os 64 nomes coincidentes são candidatos a associação específica, sujeitos a corpo/target/assumptions e possível divergência #54; todos os demais ativos não nomeados permanecem `NOT_STATED`.
- **Integração documental:** **possível com ressalvas**, se forem registradas ausências, diferenciação de status, dependências `incomplete`, status do PDF externo e qualificadores de soundness. **Integração como reprodução formal integral do relatório: não sustentada.**
- **Escopo desta intervenção:** apenas este arquivo numa branch separada; não há alteração em `main`, Project 3 ou branch do Helix; não foi criado PR e não foi feito merge.

**Auditora:** CERES (revisão independente de leitura de Git blobs, CVL, Solidity, scripts originais e PDF oficial).