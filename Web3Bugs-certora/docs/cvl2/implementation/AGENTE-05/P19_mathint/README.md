# AGENTE-05 — Fase 2: implementação experimental CVL2 — Origin OUSD P19

**Autorização:** [terceira revisão independente do PR #44](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/44#pullrequestreview-5577673176), exclusivamente para as duas cópias de `complete/19/{1,2}.spec`. Base `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. O PR de pesquisa #40 e o PR de diagnóstico #44 permanecem sem alteração.

## Artefatos

| Original | Derivada (02_unresolved) | SHA-256 derivada | Assertion preservada |
| --- | --- | --- | --- |
| `results/spec/complete/19/1.spec` | [1.spec](../../../../../results/cvl2/02_unresolved/19/1.spec) | `6dff6a352b42887fbf8c8679a16cb35c20489fefd668ce960146e701fe4ff4af` | `assert T2 <= MAX_SUPPLY();` |
| `results/spec/complete/19/2.spec` | [2.spec](../../../../../results/cvl2/02_unresolved/19/2.spec) | `cffd0de64eef3d466acbd706967e4729fd8aa8ad12e2e3376ba241eafa9adac3` | `assert T2 <= T || T2 == NR;` |

**Única transformação em cada arquivo**, sem alterar mais nada:

```diff
-definition divPrecisely(uint x, uint y) returns mathint 
+definition divPrecisely(mathint x, mathint y) returns mathint 
```

Target: `Web3Bugs-certora/contracts/19/spec/harnesses/Dummy.sol` (`contract Dummy {}`), inalterado. Nenhum source de `results/spec/complete/19/`, contrato, script, catálogo original ou outro ID modificado. Preservados tabs, comentários, corpo da definição, requires e ambas as asserts.

## Resultado da autorização

O coordenador compilou **separadamente** os dois hashes acima com `certora-cli 8.19.0`, `solc 0.8.7`, `--compilation_steps_only` e timeout 60 s, obtendo **exit 0 para ambas as variantes**, como descrito na [revisão independente](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/44#pullrequestreview-5577673176). Este agente conferiu a alteração mínima contra as duas fontes textuais no GitHub, mas **não obteve reexecução local nesta retomada** porque o Desktop Commander WSL entrou em estado offline; duração e stdout da compilação independente não estão disponíveis neste checkout. Nenhum resultado local foi inventado. Consulte [validação e reprodução](VALIDATION.md).

## Fundamentação e limitações

- [Relatório específico do exemplo 1](example-1.md); [relatório específico do exemplo 2](example-2.md).
- [Domínio, aritmética CVL1/CVL2 e divisão por zero](DOMAIN_ANALYSIS.md).
- [Validações, limitações do ambiente e comandos reproduzíveis](VALIDATION.md).
- A [Certora CVL2 Changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#mathematical-operations-return-mathint) afirma que operadores aritméticos resultam em `mathint`; o [Migration Guide](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#type-errors-in-arithmetic-and-casts) recomenda cautela com `require_` casts.

**Classificação permanece 02_unresolved.** Compilação não demonstra equivalência semântica, semântica de denominador zero, correção da propriedade ou VERIFIED. É obrigatória contrarrevisão independente antes de eventual autorização ampliada. **SEM CVL1, SEM PROVER, SEM MERGE.**

AGENTE-05 — FASE 2 / IMPLEMENTAÇÃO EXPERIMENTAL P19
