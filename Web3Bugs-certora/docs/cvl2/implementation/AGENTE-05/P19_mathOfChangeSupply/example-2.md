# Project 19 — complete/2.spec → 02_unresolved/2.spec

## Identificação e controle de integridade

- Base Git: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- Histórico imutável: [complete/19/2.spec](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/19/2.spec).
- Derivado: `results/cvl2/02_unresolved/19/2.spec`.
- SHA-256 do original: `132af5147a37652fe4318fc3fda8b6148fe6da0cc3195397c86d1527677c3df7`.
- SHA-256 do derivado: `cffd0de64eef3d466acbd706967e4729fd8aa8ad12e2e3376ba241eafa9adac3`.
- Target: `contracts/19/spec/harnesses/Dummy.sol` — `Dummy`; SHA-256 histórico `11f334db4012673cfb05cd9d1aca8904e9f3a822080a4d3c1c52ed474665c875`.
- Regra CVL: `mathOfChangeSupply`.
- Assertion preservada literalmente: `assert T2 <= T || T2 == NR;`.
- O nome da regra é compartilhado entre as specs, **mas as assertions são diferentes**.
- Autorização: [PR #44, revisão terceira](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/44#pullrequestreview-5577673176).

## Diff semântico e literal

Apenas a assinatura é modificada na linha 4:

```diff
-definition divPrecisely(uint x, uint y) returns mathint
+definition divPrecisely(mathint x, mathint y) returns mathint
```

O espaço final original da linha 4 e demais whitespaces históricos são retidos literalmente. A checagem de reversão (trocar a nova assinatura pela antiga) reproduziu todos os bytes originais. Os SHA-256 derivados coincidem com os calculados de maneira independente pelo coordenador. Não se alteram definição `= x*1000000000000000000 / y ;`, corpo da regra, `require`, `assert`, target, ou Solidity.

## Cadeia de domínio, por chamada

**Premissas originais não alteradas:** `T,NR,RC` são `uint` e a regra tem `T <= 2^128 - 1`, `T > 0`, `NR > 0`, `T > NR`, `RC > 0`. Na primeira chamada, `x=RC` permanece dentro de `uint256`. O segundo argumento `y=T-NR` é um `mathint` positivo, mas seu **valor** está em `[1, 2^128-2]`, portanto também representável como `uint256`.

No primeiro cálculo definido, `RCPT = floor(RC*10^18/(T-NR)) >= 0` para numerador/denominador positivos. O `require RCPT <= MAX_UINT256()` impõe limite superior de `2^256 - 1`. Logo, na segunda chamada, `x=RC` é `uint256` e `y=RCPT` está numericamente no intervalo de `uint256`, **inclusive zero**. O alargamento dos parâmetros formais para `mathint` aceita esses valores sem casts restritivos. Nenhuma alteração foi realizada na tipagem dos argumentos de regra.

**Limite da inferência:** a compatibilidade de intervalos das chamadas não prova equivalência de execução CVL1/CVL2, inclusive a interpretação de aritmética, coerções históricas, arredondamento e divisão por zero; compilação não verifica essas propriedades.

## Contraexemplo à garantia de denominador não-zero

Considere os valores matemáticos sob os próprios `require`: `T=340282366920938463463374607431768211455` (`2^128-1`), `NR=1`, `RC=1`.

Então `T-NR=2^128-2 > 10^18`, e `RCPT=floor(10^18/(2^128-2))=0`. A premissa `RCPT <= MAX_UINT256()` é satisfeita. A chamada subsequente `divPrecisely(RC, RCPT)` passa `y=0`. Esse caso não é afastado pela regra original. **Não acrescentar `require RCPT > 0` nem casts que excluam o caso.** O comportamento formal em divisão por zero precisa de adjudicação independente; não foi comprovado aqui.

## CVL1 vs CVL2 e evidência independente

- CVL2 produz `mathint` em operações aritméticas; a expressão `T-NR` e a variável `RCPT` antes eram incompatíveis com parâmetros `uint256` da declaração original no typechecker CVL2.
- No CVL2, `uint256` é subtipo de `mathint`, então o alargamento da assinatura é compatível com os valores analisados.
- CVL1 possuía regras diferentes de coerção entre tipos; **não** foi executada uma compilação CVL1 nem comparada sua semântica com CVL2 nesta fase.
- O valor matemático `x*10^18/y` permanece escrito **literalmente igual**. Mudança de domínio formal pode afetar a interpretação de bordas; a análise não constitui prova formal de equivalência.
- Docs: [mathematical operations return mathint](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#mathematical-operations-return-mathint), [implicit casting](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#implicit-and-explicit-casting), [migration type errors](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#type-errors-in-arithmetic-and-casts).
- Revisão [PR #44](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/44#pullrequestreview-5577673176): original exit 1, candidata exit **0**, CLI `8.19.0`, `solc 0.8.7`, `--compilation_steps_only`, timeout 60s. O coordenador não documentou uma duração individual da variante candidata; **não inventar duração**.
- **Esta sessão:** SHA-256 e diff da única alteração autorizada checados; nenhuma nova compilação Certora (dispositivo offline). Os três validadores oficiais rodaram na CI GitHub com exit 0 cada; o whitespace check retornou exit 2 devido a espaços históricos preservados ([CI](CI_VALIDATION.md)). O resultado de compilação do coordenador **não** é atribuído a uma nova execução local. [Runbook](REPRODUCE.md).

## Classificação de migração

`02_unresolved` — derivado tipável de acordo com experimento independente, mas **equivalência semântica não demonstrada**, incluindo possível divisão por zero. Nenhuma inferência de VERIFIED, VIOLATED ou equivalência histórica. Não promover para `01_documented` nem `00_unchanged` antes de parecer independente.

---

### Adendo específico — assertion do exemplo 2 (2026-10-19)

A disjunção `assert T2 <= T || T2 == NR;` é **mais restritiva**, no modelo de divisão inteira positiva definido (`q=RCPT>0`), do que `assert T2 <= MAX_SUPPLY();`. A fórmula matemática dá `T2>=T>NR`, então `T2 == NR` é impossível nesse subdomínio. Com `T=500000000000000002, NR=1, RC=1`, resulta `q=1` e `T2=1000000000000000001`; neste modelo, a assertion 2 é **falsa** enquanto a 1 é verdadeira. Não se atribui isso ao Prover ou ao CVL1 histórico. A segunda divisão com `RCPT=0` continua sem semântica interversões demonstrada. [Análise e fontes completas](SEMANTIC_REVIEW.md).

**Gate atual:** CI/integridade PASS conforme [coordenador no PR #46](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/46#pullrequestreview-5578571091); exit 2 de whitespace citado acima é histórico. **Equivalência não comprovada; `02_unresolved`, DRAFT.**
