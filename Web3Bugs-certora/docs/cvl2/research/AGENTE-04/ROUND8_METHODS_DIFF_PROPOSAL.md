# AGENTE-04 — RODADA 8: transformação CVL2 **apenas documental** de P15/incomplete/36

**NÃO É UMA SPEC DERIVADA. NÃO TESTADO EM CERTORA CVL2.** Este arquivo descreve **somente** hipótese de sintaxe dos seis métodos da cópia `results/spec/incomplete/15/36.spec`, sem tocar nela nem no texto da rule. Commit de auditoria fixo `aave/gho-core@ce49fb0c94cfebf0159222ceb288e4f9a55d305f`; target real do runner `GhoDiscountRateStrategyHarness`; N.spec SHA256 **herdado da R6** `eee38425eb95100799fe30e8d5913f9593230763733197a3dae5dae95cb0073e`.

## Diff proposto do bloco methods, não aplicado

```diff
 methods {
-    calculateDiscountRate(uint256, uint256) returns (uint256) envfree
-    MIN_DISCOUNT_TOKEN_BALANCE() returns (uint256) envfree
-    MIN_DEBT_TOKEN_BALANCE() returns (uint256) envfree
-    DISCOUNT_RATE() returns (uint256) envfree
-    GHO_DISCOUNTED_PER_DISCOUNT_TOKEN() returns (uint256) envfree
-    wadMul(uint256, uint256) returns (uint256) envfree
+    function calculateDiscountRate(uint256, uint256) external returns (uint256) envfree;
+    function MIN_DISCOUNT_TOKEN_BALANCE() external returns (uint256) envfree;
+    function MIN_DEBT_TOKEN_BALANCE() external returns (uint256) envfree;
+    function DISCOUNT_RATE() external returns (uint256) envfree;
+    function GHO_DISCOUNTED_PER_DISCOUNT_TOKEN() external returns (uint256) envfree;
+    function wadMul(uint256, uint256) external returns (uint256) envfree;
 }
```

## Matriz fato/inferência/prova faltante

| SOURCE/REPORT FACT | INFERENCE | MISSING PROOF |
| --- | --- | --- |
| CLI 8.19.0 R6: seis erros CVL2 `function` e `;` (L7–12) | Prefixo e terminador podem sanar **esse** erro de parsing | Nenhum teste da variante; podem existir novos erros |
| ABI Solidity solc 0.8.10 R5: seis métodos externos na target | `external` corresponde à ABI dos calls diretos; não usar `internal` sem razão | Receiver/inherited method resolution do CLI, dispatch e global context |
| Solidity strategy `calculateDiscountRate` **pure**; getters `public constant`; harness `wadMul external view` | `envfree` é uma hipótese coerente, sem dependência ambiental óbvia | Não passou por `envfreeFuncsStaticCheck` nem `envfreeFuncsAreNonpayable`; não remover `envfree` para passar |
| Source full `ghoDiscountRateStrategy.spec` tem cinco rules e duas CVL helpers; N.spec só uma rule | Helpers e rules adicionais podem não ser chamados diretamente por esta rule | Igualdade da cena/invariantes/reverts e do universo de contraexemplos |

**Receiver:** CVL2 methods sem qualifier usam default `currentContract` em declarações exatas, porém funções herdadas têm contrato definidor `GhoDiscountRateStrategy`; regras de summary distintas para herdadas. Como **não há summary** na spec do exemplo, não adicionar `_.`, `NONDET`, `optional`, `GhoDiscountRateStrategyHarness.` ou `GhoDiscountRateStrategy.` sem decisão de resolução de método. Nenhum `require`, `assert`, `cast`, hook, ghost ou Solidity pode mudar como atalho.

**Gate:** apenas depois de recuperação WSL comprovada e autorização por P15/36 do coordenador: copiar arquivo original com hash/cmp e target/harness/solc resolvidos para scratch isolado, aplicar EXCLUSIVAMENTE diff aos seis methods, executar **só** `--compilation_steps_only` com timeout/logs completos. Mesmo sem erro de compilação, **não declarar equivalência**.

Documentação: [Changes CVL2](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#required-internal-or-external-annotation), [Methods](https://docs.certora.com/en/latest/docs/cvl/methods.html#envfree-annotations).

**AGENTE-04 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS**
