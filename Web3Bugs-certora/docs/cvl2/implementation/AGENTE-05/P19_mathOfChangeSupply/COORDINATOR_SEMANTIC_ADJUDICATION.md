# Revisão semântica independente do coordenador — P19/1 e P19/2

**Data:** 2026-10-19  
**PR:** [#46](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/46)  
**Fonte histórica imutável:** `Web3Bugs-certora/results/spec/complete/19/{1,2}.spec` no commit `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`  
**Status:** `02_unresolved` para ambas. **Não houve Prover formal ou teste CVL1 nesta revisão.**

## 1. Escopo documental e independência

Esta contrarrevisão verifica a consistência das contas e a **suficiência limitada** das fontes apresentadas em `SEMANTIC_REVIEW.md`; não reclassifica resultados históricos e não altera regras ou contratos. As specs derivadas diferem das originais apenas pela assinatura `divPrecisely(uint x, uint y) returns mathint` para `divPrecisely(mathint x, mathint y) returns mathint`. A compilação local CVL2 *apenas* dessas variantes foi demonstrada anteriormente pelo coordenador com exit 0 (CLI 8.19.0, `--compilation_steps_only`), não repetida nesta contrarrevisão. A compilação das originais resultou em erros de tipos.

**Fontes principais:**
- Original [math.spec](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/19/spec/math.spec).
- [Certora — Changes Introduced in CVL2, Changes to integer types](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#changes-to-integer-types), sobretudo *Mathematical operations return mathint* e *Implicit and explicit casting*. A documentação afirma aritmética exata em CVL2, não uma equivalência formal deste arquivo CVL1.
- [Certora — CVL2 Migration Guide, Type errors in arithmetic and casts](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#type-errors-in-arithmetic-and-casts), alerta para casts de tipo `require_` que podem ocultar contraexemplos.
- [Certora — Finding Bugs in Formal Specifications, 2022](https://medium.com/certora/finding-bugs-in-formal-specifications-536ee3141e57), discute domínio não definido de divisão por zero e efeito das precondições. Não fixa uma semântica interversões `mathint / 0`.

## 2. Contraprova aritmética independente

Sejam `K=10^18`, `S=2^128-1`, `U=2^256-1`, `D=T-NR`, `A=RC*K` e `q=floor(A/D)`. Das premissas literais: `2<=T<=S`, `1<=NR<T`, `1<=RC<=U`, portanto `1<=D<=S-1`.

**Hipótese explícita:** para `D>0` e `q>0`, ambas as divisões CVL da regra comportam-se como divisão matemática inteira por positivos, sem wrap, e produzem `T2=floor(A/q)+NR`. Esta hipótese é verificável como modelo matemático, mas **não foi demonstrada como semântica da versão CVL1 histórica**.

Pela divisão euclidiana, `A=D*q+r` com `0<=r<D`, logo
```text
T2 = floor(A/q) + NR
   = D + floor(r/q) + NR
   = T + floor(r/q) >= T > NR.
```
Consequências neste subdomínio, e **somente** nele:
- `assert T2 <= T || T2 == NR` equivale a `T2==T`; o segundo termo da disjunção é impossível.
- Como `T<=S`, a violação da assertion 1 (`T2>S`) implica a violação da assertion 2 (`T2>T`). A implicação inversa não vale: `V1` é subconjunto **próprio** de `V2` **no mesmo modelo com q>0**.
- Nenhuma dessas relações identifica uma propriedade como formalmente VERIFIED/VIOLATED e não compara `CVL1` com `CVL2`.

**Testemunhos calculados com inteiros exatos (não traces Certora):**

| Caso | T | NR | RC | q | T2 | Efeito |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Denominador zero | `340282366920938463463374607431768211455` | 1 | 1 | 0 | indefinido | Segunda chamada tem y=0, apesar de cumprir as premissas anteriores |
| Só assertion 2 falha | `500000000000000002` | 1 | 1 | 1 | `1000000000000000001` | Assertion 1 verdadeira; assertion 2 falsa |
| Ambas falham | `340282366920938463463374607431768211455` | 1 | `340282366920938463464` | 1 | `340282366920938463464000000000000000001` | `T2>S` e `T2>T` |

A testemunha `q=0` satisfaz `require RCPT<=MAX_UINT256()`; não se atribui valor a `T2` nem um resultado de assert na divisão por zero. Não se deve adicionar `require RCPT>0`: isso reduziria os valores contemplados pela regra original.

Outro risco independente: `RC=U, T=S, NR=1` dá `A=U*K>U` e ainda `q<=U` no modelo exato. Assim, o `require` que limita o **quociente** não limita o **produto intermediário**. A documentação consultada não estabelece que o CVL1 histórico avaliava esse intermediário exatamente como o CVL2.

## 3. Decisão de revisão

- **Compilação da candidata e integridade do diff:** evidenciadas em execução anterior e CI do PR; não houve recompilação nesta rodada.
- **Fundamentação A1/A2 da mudança de tipo:** suficiente para explicar o erro do compilador CVL2 e a transformação candidata mínima em *definition* puramente CVL.
- **Preservação dos requisitos, assertions e código Solidity:** confirmada textualmente nas cópias derivadas.
- **Equivalência semântica CVL1→CVL2:** **NÃO PROVADA**. Carece de fundamento versionado para coerções/aritimética CVL1 e comportamento em `mathint/0` nos modelos relevantes. Não deduzir apenas pelo sucesso do typechecker e não aceitar invariantes/contraexemplos adicionais como justificados.
- **Classificação final por ora:** `02_unresolved` para `19/1` e `19/2`. PR #46 deve continuar **DRAFT e sem merge**.

**Portão para qualquer promoção futura:** nova evidência oficial ou avaliação formal aprovada sobre (a) aritmética/coerção na versão histórica CVL1 usada na spec e (b) tratamento do segundo divisor igual a zero; se não existir, preservar a lacuna como resultado da pesquisa, sem conversões especulativas. Não executar automaticamente CVL1, Prover, nem mudar as premissas ou as specs históricas.

Esta revisão é independente das conclusões autorrelatadas do agente; os cálculos foram recalculados com inteiros exatos pelo coordenador e os links de documentação oficial foram consultados na data acima.
