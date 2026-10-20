# AGENTE-01 / Rodada 8 — propostas lexicais *documentais*, não executadas

**Alvo:** P10/complete/33 e P10/complete/34. Documento exclusivamente propositivo; nenhum `N.spec` original, Solidity, harness, relatório, resultado ou `require/assert` foi editado. Não contém variante executável homologada, não aprova Fase 2.

## Identidades e fonte da cena

| Campo | P10/complete/33 | P10/complete/34 |
| --- | --- | --- |
| Fonte `N.spec` baseline | `results/spec/complete/10/33.spec` | `results/spec/complete/10/34.spec` |
| Git blob do `N.spec` | `e55057a90f641156538f732c0fe172c28cd86dad` | `3e180d5f3a046f2e63192cd1a464cadff5b8775a` |
| Regra CVL histórica | `noThrow` | `noRevert` |
| Trecho fonte `libParam.spec` GLOBAL | L6–19 | L21–31 |
| `methods` no recorte | duas entradas `envfree` | **nenhuma** |
| Último diagnóstico real | Round 5: parser CVL2 EXIT 1, métodos sem `function`/`;` | Round 5: parser CVL2 EXIT 1, selector sem `sig:` |
| Novo `certoraRun` R8 | **NOT_RUN_INFRA_BLOCKED** | **NOT_RUN_INFRA_BLOCKED** |

GLOBAL: [`dinngo/furucombo-contract@c90dec1/specs/libParam.spec#L1-L31`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/libParam.spec#L1-L31), Git blob `096f9f704226a7aa77c3d0da3862644db5051eb3`. Harness: [`LibParamHarness.sol#L10-L19`](https://github.com/dinngo/furucombo-contract/blob/c90dec1046e5e26edf70f985dd86381403912482/specs/harnesses/LibParamHarness.sol#L10-L19), blob `e31683f3b63a95d3522f897748d0d13159388a15`. Biblioteca: `LibParam.sol` blob `740e8a5ccae25d5e041c9736545c13de7cd3867f`.

## A. Diff textual mínimo HIPOTÉTICO — complete/33

O recorte contém os métodos globais originais, inclusive `envfree`. Apenas a grafia das declarações e o selector tipado são sugeridos abaixo. O receiver explícito pode ser indicado **se** o target do diagnóstico for a cena exclusiva `LibParamHarness`; a omissão do receiver em CVL2 denota `currentContract` e deve ser comparada separadamente.

```diff
 methods {
-    isStatic(bytes32) returns (bool) envfree
-    getNumOfReferences(bytes32) returns (uint256) envfree
+    function LibParamHarness.isStatic(bytes32) external returns (bool) envfree;
+    function LibParamHarness.getNumOfReferences(bytes32) external returns (uint256) envfree;
 }
 ...
-    if (f.selector == getParams(bytes32).selector) {
+    if (f.selector == sig:getParams(bytes32).selector) {
```

**Fatos de Solidity verificáveis em fonte, não ABIs de execução:** ambas as funções do harness são `external` e `nonpayable` por ausência de `view/pure/payable` nas linhas L10 e L14; `isStatic` retorna `bool`, `getNumOfReferences` retorna `uint256`. Na biblioteca `LibParam`, funções de nome semelhante são `internal pure` (L17, L36) e **não são automaticamente o alvo de chamadas CVL sem receiver**. O wrapper `getParams(bytes32)` é `external` com **nenhum retorno**; seu corpo chama a rotina `internal pure` que retorna arrays e exige verificações extras.

**Riscos de semântica ainda vermelhos:** `envfree` não é summary; mantém seu próprio dever de independência do ambiente. Receiver explicitamente restrito pode alterar universo de scene multicontrato. `method f` ainda pode incluir outros métodos: não acrescentar `filtered`, `optional`, `require`, `assume`, casts nem trocar `lastHasThrown` por `lastReverted` para silenciar erros. Os guards `e.msg.value==0`, `!isStatic(x)`, `getNumOfReferences(x)>0`, `getParams@withrevert`, `f@withrevert`, `assert !lastHasThrown` são intocáveis. A biblioteca ainda tem `require(n>0)`, `require(i<n)`, `require(i==n)`: não há prova de que os guards da regra previnam todos os reverts.

**Nível de evidência:** `DOCUMENTED_CANDIDATE` gramatical; `COMPILE_OK=NO`, `SEMANTIC_PROVEN=NO`.

## B. Diff textual mínimo HIPOTÉTICO — complete/34

```diff
-    if (f.selector == getParams(bytes32).selector) {
+    if (f.selector == sig:getParams(bytes32).selector) {
         require false;
     } else {
         f@withrevert(e, arg);
     }
     assert !lastReverted;
```

A linha `require false;` acima aparece como **contexto preservado**, não é uma adição. Este `require` exclui o ramo `getParams`; a assertion subsequente cobre apenas caminhos admissíveis do ramo `else`. **Não** alegar que `getParams` foi provado livre de reverts; não criar novo `methods` no recorte, pois ele não constava na extração `34.spec`.

**Nível de evidência:** `DOCUMENTED_CANDIDATE` lexical; `COMPILE_OK=NO`, `SEMANTIC_PROVEN=NO`.

## C. Proposta de dois diagnósticos separados para decisão do coordenador

1. **Experiência proposta E1 — P10/complete/33:** depois de recuperação formal do WSL e gate individual, fixar CLI/solc0.6.12, seed `LibParamHarness.sol` + `LibParam.sol`, snapshot hash, recorte byte-exato como controle e variante lexical separada apenas em scratch. `certoraRun --compilation_steps_only`, timeout, logs completos e hashes `sha256sum`/`cmp`, e anotar o **primeiro** diagnóstico real posterior a `methods`. Examinar divergência com `specs/libParam.spec` global **em execução separada**, sem afirmar equivalência.
2. **Experiência proposta E2 — P10/complete/34:** autorização independente, mesmo target/versions e controle byte-exato, somente hipótese `sig:`; preservar `require false;` e `assert !lastReverted`. Diagnóstico compile-only não autoriza remover o ramo nem declarar resultado VERIFIED. Antes de eventual prova, demonstrar satisfatibilidade do ramo `else`, f-domain e efeitos de `@withrevert`.

A ausência de credenciais não deve virar `COMPILE_ERROR`; falhas EIO/SIGBUS/EROFS impedem a tentativa. Nenhuma experiência foi realizada nesta R8. Eventual `COMPILE_OK` restrito à variante não equivale a `SEMANTIC_PROVEN`. A aprovação de implementação exige gate adicional por property.

**AGENTE-01 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS.**
