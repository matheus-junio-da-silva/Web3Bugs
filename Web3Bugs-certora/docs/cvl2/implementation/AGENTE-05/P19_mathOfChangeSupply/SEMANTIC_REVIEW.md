# Revisão semântica documental — P19 / divPrecisely / PR #46

**Decisão:** equivalência CVL1→CVL2 **NÃO COMPROVADA** para as duas properties. Ambas permanecem em `results/cvl2/02_unresolved/19/`. Este estudo não executou Prover, CVL1, CVL2 ou alterou código. Os exemplos abaixo são **cálculos matemáticos condicionais**, não traces nem counterexamples obtidos pelo Prover.

## Controle de escopo e revisão

- Revisão mais recente do coordenador em 2026-10-19: [PR #46, revisão 5578571091](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/46#pullrequestreview-5578571091), sobre HEAD `c2d10e3265765a61d50aa2c2d668b1a9e051cb27`. Gates de integridade e CI aceitos, gate de semântica não aceito; PR DRAFT.
- Source histórica primária: [`contracts/19/spec/math.spec` no baseline 2a03637](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/19/spec/math.spec). Descreve `RCPT = RC/(T-NR)`, `T' = RC/RCPT+NR` e explicitamente o fator `1e18`/divisão inteira. Fonte dos dois asserts **diferentes**.
- Exemplos históricos: [`complete/19/1.spec`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/19/1.spec) e [`complete/19/2.spec`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/19/2.spec). Alteração derivada autorizada: **somente** tipos dos parâmetros formais `uint→mathint`, sem mudanças no corpo.
- [Certora, *Changes Introduced in CVL2*, seção Mathematical operations return mathint](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#mathematical-operations-return-mathint): no CVL2, `+`, `-`, `*`, `/`, etc. produzem `mathint` e operações aritméticas CVL são exatas/sem overflow.
- [Certora, *Implicit and explicit casting*](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#implicit-and-explicit-casting): `uint256` é subtipo de `mathint` no CVL2; CVL1 possuía regras de coerção dependentes de contexto.
- [Certora, *Migration — Type errors in arithmetic and casts*](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#type-errors-in-arithmetic-and-casts): `require_` cast pode ocultar bugs; nenhum cast novo foi inserido.
- **Testemunho histórico datado:** [texto oficial Certora/Documentation de 2023-09-12 (commit 6d00687)](https://github.com/Certora/Documentation/blob/6d00687c43e152a36b3fd8f7aa1c1190eb5b1106/docs/cvl/cvl2/changes.md) já descrevia diferença de coerções CVL1/CVL2, `mathint` e operadores; não é reconstrução a partir de código moderno.
- [Repositório oficial Certora/CVL2Migration (criado em 2023)](https://github.com/Certora/CVL2Migration/tree/cvl1/certora/spec) e [branch cvl2](https://github.com/Certora/CVL2Migration/tree/cvl2/certora/spec) confirmam o contexto histórico de migração, **mas não são teste da presente função nem documentação de divisão por zero**.
- [Certora, artigo histórico *Finding Bugs in Formal Specifications* (2022)](https://medium.com/certora/finding-bugs-in-formal-specifications-536ee3141e57): explicita que a expressão de divisão por zero usada em uma regra matemática não está bem definida e requer cuidado com o domínio. Não fornece uma tabela operacional CVL1 versus CVL2 para `x/0`.
- [Certora, artigo de 2023 sobre equivalência e divisão](https://www.certora.com/blog/optimize-gas-without-getting-rekt-part-1): distingue revert da divisão Solidity e valor zero no opcode de divisão Yul. **Isto não estabelece o comportamento de `/0` em expressões puramente CVL**.
- [Revisão independente do PR #44](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/44#pullrequestreview-5577673176): CVL2 typecheck original exit 1, derivado exit 0; a compilação não é prova semântica.

## 1 — Significado aritmético da definição

Corpo textual inalterado nos dois exemplos: `divPrecisely(x,y) = x * 1000000000000000000 / y`, `returns mathint`.

**CVL2, respaldo documental:** operadores aritméticos resultam em `mathint`; o produto matemático não sofre wrap nem overflow. Os `uint256` originais `T,NR,RC` continuam inalterados; alargar parâmetros de uma **definition CVL**, não uma função de contrato, admite valores `mathint` sem cast restritivo.

**CVL1, respaldo documental limitado:** as regras de conversão eram dependentes do contexto (Certora, 2023); a documentação consultada **não fornece demonstração versionada** de que a multiplicação `x*1e18` com formais `uint` e retorno `mathint` era avaliada com a mesma precisão/ordem de coerção de CVL2 em todos os valores admitidos. **Não declarar que CVL1 necessariamente faz overflow, wrap ou é idêntico a CVL2.** A sintaxe da divisão permanece igual, mas a igualdade da operação antiga e nova não está demonstrada.

**Risco numérico específico:** `RC` não recebe limite menor que `MAX_UINT256` pela regra. Há entradas com `RC*10^18 > MAX_UINT256` e primeiro quociente ainda `<= MAX_UINT256` (por exemplo `T=2^128-1, NR=1, RC=2^256-1` no modelo exato). Isso impede usar apenas o `require RCPT <= MAX_UINT256()` para deduzir que o produto intermediário era representável em `uint256` no CVL1. Não é alegação de overflow realmente ocorrido no CVL1.

## 2 — Domínio de **cada argumento em cada chamada**

Escreva `K=10^18`, `S=2^128-1`, `U=2^256-1`, `D=T-NR`, `A=RC*K`. Pelos `require` originais, `2 <= T <= S`, `1 <= NR <= T-1`, `1 <= RC <= U`, portanto `1 <= D <= S-1 = 2^128-2`.

| Chamada | `x` | `y` | O que está estabelecido |
| --- | --- | --- | --- |
| primeira, `divPrecisely(RC, T-NR)` | `RC`, inteiro `[1,U]` | `D`, inteiro `[1,S-1]` | Ambos os **valores** cabem em `uint256`; `D` é não-zero. Em CVL2, a expressão `T-NR` é do tipo `mathint`. |
| segunda, `divPrecisely(RC, RCPT)` | `RC`, inteiro `[1,U]` | `RCPT`, `mathint`; após primeira divisão definida e `require RCPT<=U`: intervalo **condicional** `[0,U]` | Ambos os valores caberiam numericamente em `uint256`, **mas zero é permitido para `y`**. |

A primeira divisão com numerador e denominador positivos produz `RCPT>=0` sob a interpretação usual de quociente inteiro não-negativo; o `require` só aplica **limite superior**. Portanto, a passagem de `mathint` no derivado não adiciona novos valores numéricos na primeira ou na segunda chamada **se a primeira operação tiver a interpretação matemática indicada**, mas isso é apenas um argumento de domínio, não prova de que CVL1 e CVL2 calculavam o mesmo `RCPT`, nem prova de comportamento idêntico para `RCPT=0`.

Também não se introduziu um `require` oculto, `assert` de intervalo ou cast de estreitamento; as condições da regra continuam literais.

## 3 — `RCPT=0` e segunda divisão por zero

A especificação histórica **não contém** `require RCPT>0`. No modelo usual de divisão inteira por positivos, `RCPT=floor(A/D)=0` sempre que `0<A<D`.

**Testemunha matemática reproduzível, que satisfaz todas as premissas anteriores à segunda divisão:**

- `T=340282366920938463463374607431768211455 (=S)`, `NR=1`, `RC=1`.
- `D=S-1=340282366920938463463374607431768211454` e `A=10^18`.
- `A<D` e `RCPT=0` no modelo de divisão inteira positiva; `RCPT<=U` é verdadeiro.
- A segunda chamada se torna `divPrecisely(1,0)`; `T2` **não é uma expressão matemática definida** nesse caso. **Não atribuir valor numérico ou truth value às duas assertions nesse ponto.**

**Fonte oficial/histórica recuperada:** artigo Certora de 2022 sobre especificações observa que a divisão matemática por zero não é bem definida e ilustra a necessidade de delimitar domínio. Entretanto, **não foi encontrada documentação oficial versionada que determine se uma definição CVL1/CVL2 com `mathint / 0` é descartada, tratada como erro, valor arbitrário, efeito do SMT ou outro comportamento no pipeline relevante**. Documentos sobre EVM/Solidity/Yul não suprem essa lacuna, pois `Dummy` não executa essa divisão Solidity: ela é uma expressão da *spec*. A ausência dessa regra operacional comparativa é um **bloqueio real de equivalência e de comparação de contraexemplos**.

Não adicionar `require RCPT>0`; fazê-lo eliminaria justamente essa entrada.

## 4 — Universo de contraexemplos: distinguir assertions de versões

### 4.1 Duas assertions diferentes — **relação matemática condicional demonstrável**

No subdomínio matemático `q=RCPT=floor(A/D) > 0`, com divisão inteira positiva e exata, `A=D*q+r` para `0<=r<D`. Logo:

```text
T2 = floor(A/q) + NR
   = D + floor(r/q) + NR
   = T + floor(r/q) >= T > NR.
```

Assim, **neste modelo matemático definido**, a segunda disjunção `T2 == NR` é impossível; o exemplo 2 só passa se `T2<=T`, i.e., `T2==T`. Como `T<=S`, qualquer violação da assertion do exemplo 1 (`T2>S`) também viola a do exemplo 2. Formalmente, no subdomínio modelado, `V1 ⊆ V2`.

A inclusão é **estrita** no modelo matemático: `T=500000000000000002`, `NR=1`, `RC=1`, `D=500000000000000001`, `A=10^18`, `q=1`, `T2=1000000000000000001`. O exemplo **1 passa** (`T2<=S`), enquanto o exemplo **2 falha** (`T2>T` e `T2!=NR`). Também existe testemunha matemática com ambas falsas e `q>0`: `T=S,NR=1,RC=340282366920938463464`; daí `q=1`, `T2=340282366920938463464000000000000000001>S`.

Esses valores foram conferidos por **aritmética exata independente (BigInt), não por Certora**. Não classificá-los como counterexamples retornados pelo Prover, nem transpor automaticamente para CVL1.

### 4.2 O que NÃO está provado sobre CVL1→CVL2

`V1 ⊆ V2` acima compara as **duas fórmulas de assertion** sob **um mesmo modelo matemático com `q>0`**, não compara `V1_CVL1` contra `V1_CVL2` nem `V2_CVL1` contra `V2_CVL2`. Para sustentar igualdade de universos entre linguagens seriam necessárias evidências para: (a) mesma coerção/precisão do intermediário `A=RC*K`; (b) mesma semântica de divisão inteira para argumentos positivos; (c) mesmo comportamento da segunda divisão com `q=0`, incluindo se as entradas são consideradas pelas assertions. A documentação encontrada **não fecha (a) e (c)** e não fornece equivalência formal de (b) para o engine CVL1 histórico.

Consequentemente, não é possível afirmar `V1_CVL1=V1_CVL2` nem `V2_CVL1=V2_CVL2`, tampouco afirmar que os conjuntos são necessariamente diferentes. `--compilation_steps_only` com exit 0 certifica tipagem/compilação, não esses universos. Não há base para VERIFIED, VIOLATED ou promoção de bucket.

## Matriz de adjudicação — apoio versus inferência versus bloqueio

| Afirmação | Situação e fundamento |
| --- | --- |
| A definição histórica recebe dois `uint`, retorna `mathint` e usa `x*1e18/y`; duas assertions diferentes | **DOCUMENTADA:** original `math.spec` e `complete/19/{1,2}.spec` no baseline |
| CVL2 retorna `mathint` em operações; inteiros são subtipos de `mathint`; CVL1 tinha conversões dependentes de contexto | **DOCUMENTADA:** Certora Docs, inclusive commit de 2023 |
| Em condições originais, `1<=T-NR<=2^128-2`, `RC∈[1,U]` | **DEDUÇÃO ARITMÉTICA EXATA** dos `require` documentados |
| Segundo argumento da segunda chamada pode ser zero apesar do `require RCPT<=U` | **DEDUÇÃO CONDICIONAL AO QUOCIENTE INTEIRO POSITIVO**, com testemunha explícita |
| Fórmula `floor(A/D)` e `floor(A/q)` representa fielmente CVL1 e CVL2 em todas as bordas | **NÃO COMPROVADA** historicamente, em especial coerção CVL1 e divisão por zero |
| Para `q>0`, `V1⊊V2` sob o mesmo modelo de divisão inteira exata | **PROVADO MATEMATICAMENTE, CONDICIONAL** a esse modelo; testemunhas numéricas verificadas, não traces Certora |
| `mathint / 0` tem comportamento operacional idêntico CVL1 e CVL2 | **BLOQUEADO:** sem fonte versionada sobre semantics de specs para `/0` |
| Universos de contraexemplos de cada exemplo se preservam na migração | **NÃO COMPROVADO**; nem igualdade nem desigualdade estabelecida |
| Specs derivadas compilaram com CLI 8.19.0 | **EVIDÊNCIA EXPERIMENTAL HISTÓRICA** do coordenador no PR #44, não prova semântica |
| Migração pode ser classificada `00_unchanged` ou `01_documented` | **NÃO AUTORIZADA / NÃO COMPROVADA**; manter `02_unresolved` |

## Fechamento

**Conclusão: equivalência CVL1→CVL2 NÃO COMPROVADA para as duas rules `mathOfChangeSupply`.** O domínio dos valores dos parâmetros foi delimitado matematicamente em ambas as chamadas; isso não substitui prova de semântica do cálculo CVL1 e, principalmente, da divisão por zero no cálculo intermediário. As diferenças matemáticas dos dois asserts são independentes da mudança de linguagem. Manter **ambos `02_unresolved`**, PR **DRAFT**, sem merge ou alterações adicionais de spec, casts, requires, asserts, Solidity ou configuração. Sem CVL1, sem Prover.

AGENTE-05 — FASE 2 / IMPLEMENTAÇÃO EXPERIMENTAL P19 — investigação documental semântica.
