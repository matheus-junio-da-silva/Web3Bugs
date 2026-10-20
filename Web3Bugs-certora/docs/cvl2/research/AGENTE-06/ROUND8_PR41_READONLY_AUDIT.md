# AGENTE-06 — Rodada 8 / auditoria cruzada READ-ONLY PR #41

Data 2026-10-20. PR [#41](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/41), HEAD **`7583e3447a65746cf1efdf6a1dfb931c1849968d`** observada via conector, DRAFT; baseline `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Nenhuma escrita, commit, checkout, comentário, push ou alteração na branch de AGENTE-07. A auditoria focaliza as **hipóteses de axiomas e vacuidade do P8**.

## QA de escopo e estado declarado

A API `list_pr_changed_filenames` retornou **238 caminhos**, todos sob `Web3Bugs-certora/docs/cvl2/research/AGENTE-07/`, sem arquivo fora de escopo. O objeto `ROUND7_MATRIX_156.csv` na HEAD atual preserva Git blob `863a7d514fd50e1de802e22d7911c47fb38abd3f` (156 propriedades: P8 42, P9 61, P11 16, P20 37). O novo [`ROUND8_MATRIX_156.csv`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/7583e3447a65746cf1efdf6a1dfb931c1849968d/Web3Bugs-certora/docs/cvl2/research/AGENTE-07/ROUND8_MATRIX_156.csv), blob `5bdb280d7a6598c977827f7482964e34ea5cbcfa`, contém 156 linhas de dados; examinado com o novo [`ROUND8_EVIDENCE.md`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/7583e3447a65746cf1efdf6a1dfb931c1849968d/Web3Bugs-certora/docs/cvl2/research/AGENTE-07/ROUND8_EVIDENCE.md), blob `ffd5f5d917635152a12dee8e6c52e7dd87a58420`. **Nenhuma nova compilação CVL2 observada** nessa revisão. A contagem do agente permanece 156 NOT_RUN, 0 equivalências; nenhuma validação de semantics por CI.

**Limites explícitos:** revisão documental de claims e originais exemplares; NÃO re-hashei os 156 N.spec nem executei `git diff --check`, três validadores, solc ou Prover. A contagem de W1 em 22 IDs refere-se à matriz do AG07 já auditada anteriormente; a fórmula representativa ID14 foi relida nesta rodada.

## P8 — três contradições como fórmulas, não como logs históricos

| Grupo da revisão | Fato de fonte e substituição aritmética | Interpretação ainda não provada |
| --- | --- | --- |
| **W1, 22 casos** | [`results/spec/incomplete/8/14.spec:49–54`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/14.spec#L49-L54) declara **no mesmo ghost global `rayMul_g`** que, para `x=1,y=0`, `rayMul_g(1,0)==0` e `1<=rayMul_g(1,0)`. Não há modelo de inteiros que satisfaça ambos. AG07 identifica ID 14–35; os hashes das outras 21 instâncias foram validados anteriormente, não reextraídos aqui. | A presença de um axioma textual não comprova sua ativação em cada verification job. P8/14 também tem `init_state axiom` para OUTRO ghost, que não deve ser tratado como axioma global em qualquer ponto. |
| **W2, ID1** | [`results/spec/incomplete/8/1.spec:34–35`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/1.spec#L34-L35) contém `rounding==1 => x*y < mulDiv_g(x,y,denominator,rounding)*denominator`. Com `x=y=denominator=0`, `rounding=1`, obriga `0<0` seja qual for `mulDiv_g`. | É uma contradição dos pressupostos universais se assumidos, não erro de parser do CVL2 nem teste de chamada Solidity real. |
| **W3, ID1** | [`results/spec/incomplete/8/1.spec:43–45`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/1.spec#L43-L45): `x*RAY()-y/2 < rayDiv_g(x,y)*y`. Com `x=y=0`, ambos lados são zero; **0/2 é operação válida**. | Distinta de W2, permanece condicionada ao alcance/uso da ghost na cena e ao regime de hipóteses. |

**Diferença decisiva:** (a) contradição matemática de um `forall` global escrito no fragmento é estabelecida sob sua interpretação usual; (b) que **um run histórico específico** assumiu essa ghost, seu conjunto de axiomas e suas instâncias é desconhecido; (c) que o `VERIFIED` original foi vacuamente verdadeiro é, portanto, **NÃO DEMONSTRADO**. A documentação atual [Certora Ghosts](https://docs.certora.com/en/latest/docs/cvl/ghosts.html) descreve regras de uso/ativação de axiomas quando o ghost é utilizado, estado inicial `init_state`, revert de ghosts e persistência. Não podemos transportar sem demonstração essas configurações para runner/Prover antigo.

A conclusão do AGENTE-07 de que existem 22 W1, um W2/W3 e 19 outras propriedades **sem esses padrões** é adequada **se** não se afirmar consistência das outras 19 nem equivalência. A novidade R8 sobre a rota de uso ghost `methods` summaries `rayMul/rayDiv/mulDiv` é uma **hipótese de alcance**, não um Prover log. Necessários: regra/harness `--verify`, versões de CLI e Prover, hooks Sload/Sstore, `requireInvariant`, método selector f, summaries exatos e teste de consistência derivado **somente com autorização do coordenador**, sem mudar o `N.spec` original.

## P9/P20/P11 — limites adicionais do peer review

- P9: a pesquisa R8 adicionou `remappings.txt` blob `d574784e9f9c51f05e607f49b943bfcd84c13df5` de revisão Celo posterior. Os três blobs `mento-core` no commit candidato `4ceb4f0...` são fontes concretas, mas **falta gitlink auditado** e prova de que `AccountsHarness` usou aqueles bytes/ABI; P9/6 permanece com método ausente na ABI Solidity phase2 isolada. Não usar remapping posterior para autenticar uma revisão anterior.
- P20: `MAX_INT()` em `compoundStrategyAdditional.spec:65` não é resolvido por definições em specs irmãs sem import/concatenação de runner comprovada. O patch de `try/catch` da CompoundStrategy altera potencialmente alcance de reverts. Não inferir o mesmo efeito sobre os 37 targets individualmente.
- P11: closure textual de 104 nós/204 imports e integridades tarball anteriores não prova configuração do Prover, hooks/ghosts nem resolve divergência entre SHA do relatório e commit de branch público.

## Decisão

**Conferência documental parcial: PASS** para a existência das fórmulas W1/W2/W3, quatro blobs Mento citados em revisões anteriores e manutenção de caveats de runner; **SEMANTIC_PROVEN: 0**; hipótese de vacuity do Prover histórico permanece **aberta**. Estado operacional WSL: `INFRA_BLOCKED`. Nenhum teste de satisfatibilidade ou Prover foi executado; PR #41 segue Draft, sem merge. Para avançar, coordenação deverá autorizar teste específico de axiomas *derivados* com cena versionada, após WSL saudável, sem alterar originais.

**AGENTE-06 — RODADA 8 / AUDITORIA SOMENTE LEITURA.**
