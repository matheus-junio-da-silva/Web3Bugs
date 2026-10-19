# Análise matemática e semântica — P19 mathOfChangeSupply

## Correspondência original ↔ derivada

A definição original `divPrecisely(uint x, uint y) returns mathint` aceita apenas argumentos no domínio numérico de `uint256`, se bem tipados. A definição derivada usa `divPrecisely(mathint x, mathint y) returns mathint`, mas mantém **inalterado** o corpo `x*1000000000000000000 / y`. É uma ampliação de tipos de parâmetros, **não** uma mudança do cálculo ou das hipóteses da regra.

Cada regra permanece `mathOfChangeSupply(uint T, uint NR, uint RC)`, com condições `T <= MAX_SUPPLY()`, `T > 0 && NR > 0 && T > NR`, `RC > 0`. As chamadas permanecem `divPrecisely(RC,(T-NR))` e `divPrecisely(RC,RCPT)`. Depois da primeira chamada há `require RCPT <= MAX_UINT256()`; não há limiar positivo de RCPT.

## Prova documental dos argumentos concretos

1. `T`, `NR` e `RC` permanecem `uint`; como `T ≤ 2^128−1` e `T>NR≥1`, a diferença `1≤T−NR≤2^128−2` é positiva e cabe no intervalo `uint256`. O outro argumento `RC` é `uint256` por tipo.
2. Quando `RC/(T−NR)` é avaliado de forma definida como expressão inteira e `RC>0`, `T−NR>0`, o resultado matemático `RCPT` é não negativo. O `require RCPT≤MAX_UINT256()` preservado impõe o teto. Assim, o valor passado no segundo call-site continua no intervalo numérico representável pelo parâmetro antigo `uint256` nos caminhos matematicamente definidos que satisfazem as premissas.
3. A conclusão é limitada aos **valores dos argumentos** sob a semântica matemática assumida; não comprova que o Prover CVL1 usava igual interpretação para overflow, casts ou denominador zero. Também não comprova que a asserção final é verdadeira.

## Contraexemplo relevante para divisão por zero

O coordenador observou o caso `T=2^128−1`, `NR=1`, `RC=1`: satisfaz todas as premissas originais. A primeira divisão tem numerador `10^18` e denominador `2^128−2`, portanto, com divisão inteira não negativa habitual, `RCPT = floor(10^18/(2^128−2)) = 0`. A hipótese `RCPT≤MAX_UINT256()` é satisfeita. O próximo cálculo `divPrecisely(RC,RCPT)` divide por **zero**.

Não foi assumido nem demonstrado qual é o comportamento para esse caminho na semântica histórica CVL1 ou na configuração específica do Certora CLI 8.19.0; compilar não resolve essa questão. **Não adicionar** `require RCPT>0`, `assume`, casts `require_uint256`, axiomas, mudanças de assert ou mudança na definição matemática para apagar o caso.

## Diferença de linguagens e evidências

As [mudanças oficiais CVL2](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#mathematical-operations-return-mathint) documentam resultado `mathint` para `+,-,*,/,%`, entre outros operadores, aritmética matemática exata e simplificação das regras de casts. O [guia oficial](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#type-errors-in-arithmetic-and-casts) adverte que `require_` casts podem esconder contraexemplos e tornar a regra vacuamente verdadeira. O novo tipo da definição evita narrowing implícito dos argumentos já usados, **sem introduzir uma restrição**; isso fundamenta a candidata sintática. A equivalência comportamental permanece **não provada**.

A evidência experimental é do [coordenador, terceira revisão do PR #44](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/44#pullrequestreview-5577673176): os dois arquivos derivados, identificados pelo hash, receberam exit 0 na compilação. Isso **não** autoriza classificação como 00_unchanged, 01_documented ou VERIFIED. O status continua **02_unresolved**.
