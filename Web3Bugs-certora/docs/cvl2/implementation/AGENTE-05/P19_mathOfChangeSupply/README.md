# AGENTE-05 — FASE 2 / IMPLEMENTAÇÃO EXPERIMENTAL P19

**Classificação obrigatória: `02_unresolved`.** A compilação é uma evidência de tipagem/sintaxe, **não** de equivalência semântica, VERIFIED ou VIOLATED.

## Autorização e proveniência

- Coordenador: [terceira revisão independente do PR #44](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/44#pullrequestreview-5577673176), de 2026-10-19.
- Base imutável: `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- PR #44: diagnóstico anterior, não alterado por esta implementação.
- Branch isolada: `experiment/cvl2-p19-mathint-agent05-phase2`; nenhum merge.
- Originais preservados: `results/spec/complete/19/{1,2}.spec`.
- Novos derivados: `results/cvl2/02_unresolved/19/{1,2}.spec`.
- Solidity preservado: `contracts/19/spec/harnesses/Dummy.sol`, alvo `Dummy`.
- Escopo: exatamente **2 dos 1.386** exemplos. Os outros 1.384 permanecem intocados.

## Transformação única autorizada

```diff
-definition divPrecisely(uint x, uint y) returns mathint
+definition divPrecisely(mathint x, mathint y) returns mathint
```

A linha original termina com **um espaço literal**; essa característica histórica é preservada no derivado. Nenhum outro byte é alterado. As duas cópias são verificadas por SHA-256 e pela inversão exata da transformação.

| Exemplo | SHA256 original | SHA256 derivado | Assertion preservada |
| --- | --- | --- | --- |
| [1](example-1.md) | `279c6c956d9084cb576f9e3f99dba63936d27b6e07401f9878751ac22808016a` | `6dff6a352b42887fbf8c8679a16cb35c20489fefd668ce960146e701fe4ff4af` | `assert T2 <= MAX_SUPPLY();` |
| [2](example-2.md) | `132af5147a37652fe4318fc3fda8b6148fe6da0cc3195397c86d1527677c3df7` | `cffd0de64eef3d466acbd706967e4729fd8aa8ad12e2e3376ba241eafa9adac3` | `assert T2 <= T || T2 == NR;` |

**Resultado de integridade desta sessão:** hashes candidatos calculados a partir das cópias e comparados com os SHA-256 registrados na revisão independente: **ambos coincidem**. Os originais foram lidos no commit-base e seus SHA-256 igualmente comparados.

## Evidência de compilação, sem extrapolação

A revisão [#44](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/44#pullrequestreview-5577673176) relata quatro typechecks independentes com `certora-cli 8.19.0`, `solc 0.8.7`, `--compilation_steps_only` e timeout GNU 60s. Ambos os originais falharam com exit 1 (dois erros `mathint` vs `uint256`), ambas as variantes derivadas tiveram **exit 0**. Este resultado é evidência **do coordenador**, não execução repetida pelo AGENTE-05 nesta sessão.

**Compilação e CI têm escopos distintos:** a única compilação CVL2 das derivadas é o experimento independente anterior do coordenador no PR #44 (CLI 8.19.0, exit 0 nas duas; nenhuma nova compilação nesta investigação). Na HEAD `c2d10e3265765a61d50aa2c2d668b1a9e051cb27`, o coordenador confirmou ambas as GitHub Actions **SUCCESS**: [`validate` 39335709810](https://github.com/matheus-junio-da-silva/Web3Bugs/actions/runs/39335709810) e [`Project 24 full catalog validation` 39335709821](https://github.com/matheus-junio-da-silva/Web3Bugs/actions/runs/39335709821), inclusive whitespace após `.gitattributes` restrito. O exit 2 anterior é **histórico e solucionado**, não o estado atual. [Histórico e fechamento de CI](CI_VALIDATION.md).

## Investigação semântica documental — evidências e bloqueios

A [análise focalizada](SEMANTIC_REVIEW.md) separa: **documentado** (aritmética `mathint` CVL2 e coerções CVL1 dependentes de contexto), **deduzido matematicamente** (os quatro argumentos nas duas chamadas, `RCPT=0`, `V1⊊V2` no subdomínio de divisão positiva definida) e **não demonstrado** (precisão histórica CVL1 do intermediário, semântica operacional `mathint / 0` e igualdade dos universos de contraexemplos CVL1/CVL2). Fontes incluem documentação Certora de 2023, especificação histórica e PR #46. Não há inferência de VERIFIED/VIOLATED a partir de testemunhas aritméticas.

## Validade tipada da alteração — sem equivalência formal

Na primeira chamada `divPrecisely(RC, T-NR)`, `RC` é `uint256` e `T-NR` é matematicamente positivo e no intervalo `[1, 2^128-2]` por causa dos `require`. Na segunda `divPrecisely(RC, RCPT)`, `RC` continua `uint256`; quando a primeira divisão está definida, `RCPT` é não-negativo e o `require RCPT <= MAX_UINT256()` o limita superiormente a `uint256`. Portanto, para entradas cujo cálculo esteja definido, o alargamento dos parâmetros formais não precisa ampliar o conjunto de valores das **duas chamadas presentes nesta regra**. Isso é uma análise de domínio, não uma demonstração da semântica global CVL1/CVL2.

**Obstáculo semântico ainda aberto:** `RCPT == 0` pode ocorrer sem violar os `require` originais, e então o denominador da segunda divisão é zero. Nenhuma hipótese extra é permitida ou foi adicionada. A revisão precisa determinar o comportamento desse caso e o tratamento de divisão CVL1/CVL2; mais detalhes em [`example-1.md`](example-1.md), [`example-2.md`](example-2.md).

## Fontes oficiais específicas

1. [Certora — Mathematical operations return mathint](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#mathematical-operations-return-mathint): operadores aritméticos CVL2 retornam `mathint`.
2. [Certora — Implicit and explicit casting](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#implicit-and-explicit-casting): `uint256` é subtipo de `mathint` e não requer cast para alargar.
3. [Certora — Changes to integer types](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#changes-to-integer-types): operações inteiras de precisão matemática não têm overflow em CVL2.
4. [Certora — Type errors in arithmetic and casts](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#type-errors-in-arithmetic-and-casts): recomendações e risco de `require_` casts. Nenhum cast foi introduzido.
5. [Revisão independente e experimento pré-especificado do coordenador](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/44#pullrequestreview-5577673176): transformação única e hashes de controle.

## Estado final

**Duas specs derivadas implementadas; classificação `02_unresolved`; gates CI/integridade PASS na HEAD revisada pelo coordenador; compilação CVL2 anterior PASS (somente typecheck); equivalência CVL1→CVL2 NÃO COMPROVADA segundo [revisão semântica documental](SEMANTIC_REVIEW.md). SEM CVL1, SEM PROVER, SEM MERGE.**
