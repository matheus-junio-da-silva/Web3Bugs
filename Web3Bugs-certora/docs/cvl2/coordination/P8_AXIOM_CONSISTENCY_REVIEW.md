# P8 AAVE Vault — contrarrevisão independente dos axiomas W1/W2/W3

**Data:** 20/10/2026. **Fontes originais imutáveis:** `Web3Bugs-certora/results/spec/incomplete/8/14.spec` e `.../8/1.spec` no baseline `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. **Relatório agente:** [PR #41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41), `ROUND4_EVIDENCE.md`. Nenhuma spec ou contrato foi alterado; **não foi executado Prover nem compilação CVL1/CVL2**.

## W1 — P8/incomplete/14 e grupo de 22 instâncias

Texto extraído da própria N.spec (diretiva ghost/axiom universal):

```cvl
ghost rayMul_g(uint256 , uint256) returns uint256 {
    axiom forall uint256 x. forall uint256 y.
        (
         ((x==0||y==0) => rayMul_g(x,y)==0)
         &&
         x <= rayMul_g(x,y) && rayMul_g(x,y) <= 2*x
        );
}
```

Escolhendo `x=1, y=0`, o primeiro termo força `rayMul_g(1,0)==0`, enquanto o segundo força `1<=rayMul_g(1,0)`. **Conjunção impossível no modelo de inteiros**. Não depende de overflow, assinatura externa ou valores de outras variáveis.

A classificação *22 instâncias (IDs 14–35)* vem da matriz do AGENTE-07; examinei o conteúdo integral de P8/14 como testemunha concreta dessa contradição, **não** executei checagem formal de todas as 22 N.spec em um Prover.

## W2 — P8/incomplete/1

O `ghost mulDiv_g` tem este axioma universal (o argumento `rounding` é `uint8`):

```cvl
axiom forall uint256 x. forall uint256 y.
      forall uint256 denominator. forall uint8 rounding.
    rounding == 1 =>
        x*y < mulDiv_g(x,y,denominator,rounding)*denominator;
```

`x=0,y=0,denominator=0,rounding=1` reduz a consequência exigida a `0<0`, que é falsa. Portanto a fórmula universal é insatisfatível em aritmética convencional independentemente do valor da função `mulDiv_g`; com multiplicação por zero, o termo direito é 0.

## W3 — P8/incomplete/1

O `ghost rayDiv_g` contém:

```cvl
axiom forall uint256 x. forall uint256 y.
    x*RAY() - y/2 < rayDiv_g(x,y)*y;
```

Substituindo `x=0,y=0`, ambos os lados são zero (a divisão é `0/2`, portanto **não** há divisão por zero nesta substituição): novamente `0<0`. Este modelo também não admite solução para o axioma universal.

## Relevância para a interpretação do relatório

- **Achado lógico independente:** as fórmulas literais contêm testemunhos de contradição sob semântica de inteiros usual. Testadas somente substituições exatas por um script Python read-only; o resultado foi FALSE nos três casos, e as quatro expressões-fonte foram localizadas nos arquivos originais.
- **Limite de inferência:** ainda é necessário verificar na cena Prover quais axiomas se tornam efetivamente disponíveis, como se dá seu escopo/instanciação e se a ferramenta rejeita ou presume modelos insatisfatíveis. **Não alegamos** que o resultado formal histórico foi necessariamente vacuamente verdadeiro sem executar as verificações correspondentes.
- **Não corrigir o original:** remover/relaxar esses axiomas, criar precondições `y>0` ou trocar `<` por `<=` modificaria o conjunto de modelos históricos. Esse tipo de patch não é permitido apenas para tornar a property compilável/VERIFIED.
- **Gate:** documentar para o AGENTE-07 um plano de teste de *satisfatibilidade e consistência* por grupo W1/W2/W3, em arquivo derivado separado e revisão específica; não executar Prover ou reescrever CVL histórico sem autorização posterior. Até lá estes exemplos permanecem `UNRESOLVED` e têm **alerta semântico elevado**.

O diagnóstico caracteriza **defeito potencial do modelo de especificação** distinto de incompatibilidade sintática CVL1→CVL2 e de dependência de Solidity ausente. Seu impacto histórico precisa de comprovação versionada, sem alterar `Result`, `Detection Outcome` e Bug Labels do catálogo.
