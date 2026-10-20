# AGENTE-05 — Rodada 5: contrarrevisão independente do PR #38 (somente leitura)

**Data:** 2026-10-20. **HEAD lida:** `e075395f28f81a0b19917a0aff566da1638f43e1`, PR #38 `research/cvl2-agente-06` Draft. A branch foi consultada através de `git fetch origin research/cvl2-agente-06` no workspace isolado do AGENTE-05 e `git show origin/research/cvl2-agente-06:<path>`, **sem checkout, edição, push ou commit** na branch do AGENTE-06. Baseline `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.

## P17: Specify 2019, não assumir linguagem CVL1 padrão

| ID | Linhas e construtos em `N.spec` | Dependência semântica e risco identificado | Veredito |
| --- | --- | --- | --- |
| **complete/8 `borrowFresh`** | `results/spec/complete/17/8.spec:19–28`: `env e0/e1/e2` + `havoc`; `:47–83`: `sinvoke` em getters; `:64–65`: `static_require result == invoke borrowFreshPub(e1,...)` seguido de `lastReverted`; `:114–117`: duas `static_assert` de equivalência bidirecional | Substituir `invoke` por `@withrevert` e `static_require` por `require` não prova a ligação entre env pré/pós, efeito da chamada e tratamento do resultado/revert da versão Specify. `havoc other` é de **local**, diferente de `havoc env`. As duas equivalências não podem ser rebaixadas a implicações unidirecionais. | `UNRESOLVED`; preservar domínio e asserts até runtime Specify e `.spclnk` autenticados |
| **complete/9 `repayBorrowFresh`** | `results/spec/complete/17/9.spec:19–28`: envs + `havoc other`; `:32`: `borrower != currentContract`; `:67–68`: `static_require result == invoke repayBorrowFreshPub(...)` e captura `lastReverted` | `other` é distinto de payer e borrower; trocar `havoc` por qualquer valor fixo/cast restringiria o domínio. Não há evidência de como a versão Specify relaciona `e0/e1/e2` e estados de armazenamento; a função de retorno não significa automaticamente uma prova de sucesso. | `UNRESOLVED`; não presumir equivalência lexical |
| **complete/39 `transferFrom`** | `results/spec/complete/17/39.spec:21–32` cria 4 envs e `havoc other`; `:69–80` cria `bool doApprove; havoc doApprove;` e `uint256 approvedAmount; havoc approvedAmount;` antes de `sinvoke approve(...)` condicional e `static_require success == invoke transferFrom(...)` | A ramificação `doApprove` altera a sequência de ações, bem como o estado pré-`transferFrom`; não pode ser omitida ou tratada como simples `method f`. A relação e1a/e1b, allowance observada e `lastReverted` dependem da execução Specify 2019. | `UNRESOLVED`; precisa engine+aliases e jobs originais |

A análise independente de leitura **concorda com os blockers** do AGENTE-06, mas o guia CVL2 não documenta o motor histórico Specify 2019 nem assegura preservação de `static_assert/static_require/invoke/havoc`. A contagem lexical agregada do AGENTE-06 (41 `static_assert`, 40 `static_require`, 41 `sinvoke`, 28 `invoke`, 41 `havoc`) é propriedade dos recortes, não medição de equivalência, satisfatibilidade ou resultados.

## P1: `queue2` e a ABI real do Bridge

Na fonte `contracts/1/specs/Optimism_ArbitrumBridge.spec:128,158,191,216,267,277,332,386,414–447,461,495–516` surgem chamadas `queue2(e,args)` e `queue2@withrevert(...)`, inclusive sequências que dependem do sucesso da primeira chamada e do revert da segunda. A versão catalogada de `contracts/1/contracts/bridges/L2BridgeExecutor.sol:45` expõe **`function queue(...)`**, **não** `queue2`; a spec ainda possui `_mock(e)` em `:171,289,480`. Afirmar que `queue2` é alias de `queue` exigiria wrapper original e prova da correspondência de argumentos/side effects. A diferença de autorização Polygon vs L2 aumenta o risco de falsificar o cenário. Há `queue2Reachability` na fonte `:501–505`, mas a mera presença lexical não prova sua execução na auditoria.

**Adjudicação independente:** `queue2` (14 ocorrências de casos bloqueados segundo matriz), `_mock` (6), `complexity runner` (6) e outros 44 `run_unattributed` devem permanecer eixos diferentes; nunca fabricar getter/harness nem substituir `queue2` para o parser aceitar. As evidências de commit `303bd3e...` ancoram Solidity, não o job per-rule.

## QA do PR #38 no escopo desta contrarrevisão

- HEAD confirmada `e075395f28f81a0b19917a0aff566da1638f43e1`. `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...origin/research/cvl2-agente-06` foi **EXECUTADO, EXIT 0**, no checkout isolado do AGENTE-05. Nenhuma branch do AGENTE-06 foi escrita.
- Foram lidos os recortes P17/8,9,39, a fonte original P1/Optimism_ArbitrumBridge.spec, a implementação L2BridgeExecutor.sol e `ROUND4_TECHNICAL_FINDINGS.md`; não foi executado Prover, CVL1 nem CVL2 e **não** houve releitura integral de todas as 159 regras nesta Rodada 5.
- Não identifiquei promoção indevida desses casos: `159/159 UNRESOLVED` e gatilhos documentais permanecem apropriados. Parecer limitado à amostra semântica indicada, não conclusão de equivalência de qualquer regra.

**Gate para o coordenador/AGENTE-06:** recuperar gramática/runtime e `.spclnk` Verify/Specify executados em 2019, de modo a definir semântica `havoc env/local`, `static_require`, `invoke`, `lastReverted`; localizar wrapper/prova de ABI `queue2`, helper `_mock` e runners por rule. Manter PR #38 Draft.
