# AGENTE-05 — Contrarrevisão independente SOMENTE LEITURA: PR #38 / AGENTE-06

**Data:** 2026-10-20. Repositório `matheus-junio-da-silva/Web3Bugs`. PR [#38](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/38), HEAD **`684bd419ee8e35f27ca7ee07138fced321160793`**, baseline `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`, PR confirmado Draft. **Nenhum arquivo ou branch AGENTE-06 foi alterado.** As verificações de repositório abaixo foram feitas em checkout HEAD detached limpo `/home/mat/agente06-cvl2-phase1-worktree`.

## Verificações realizadas independentemente

- API GitHub: **236 arquivos modificados no PR #38, 236/236** sob `Web3Bugs-certora/docs/cvl2/research/AGENTE-06/`, nenhum fora do escopo. Base e HEAD reconciliados.
- `historical_closure_decisions.csv` contém **159 chaves únicas** `project_id/original_status/example_id`: P1=70, P17=41, P4=27, P22=21. Correspondência `property`, status histórico e fechamento individual com os quatro `properties.csv` passou em 159/159.
- Presença e SHA-256 dos **159 `N.spec`** comparados ao campo `n_spec_sha256` em `properties.csv`: 159/159. Os conjuntos `N.md`, `N.sol` e `N.txt` aplicáveis também foram localizados.
- Os quatro arquivos de `properties.csv` ainda mantêm todos os **159 `UNRESOLVED_CANDIDATE`**. Não houve promoção indevida para bucket migrado.
- Estados históricos: **102 `historical_blocked_*`** e **57 `historical_run_unattributed`**. Discriminados: P1 14 queue2 / 6 mock / 6 complexity / 44 unattributed; P17 41 Specify; P4 27 generated munged; P22 6 runner scope / 13 unattributed / 1 private getter / 1 free symbol.
- `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD`: **EXIT 0**. Worktree AGENTE-06 limpo. Os três validadores oficiais (`check_specs.py`, `check_contracts.py`, `check_contests_csv.py`) retornaram **EXIT 0** independentemente.

## Verificação de substância, por evidência específica

| Projeto e caso | Inspeção direta independente | Gate |
| --- | --- | --- |
| P1, `Optimism_ArbitrumBridge.spec` e `complexity.spec` | Scripts e dossiê apontam `queue2`, `_mock` e target da complexity sem ABI/runner histórico autenticado. Hash do commit Solidity `303bd3...` documenta fonte, não execução de cada rule. | Sem migração; coerente manter 14/6/6 bloqueados e 44 unattributed. |
| P17/complete/8 `borrowFresh` | Fragmento original contém `env e0/e1/e2` com `havoc`, `static_require`, `sinvoke`, `invoke borrowFreshPub`, `lastReverted` e `static_assert`. Também existem aliases `.spclnk`. Não é uma migração textual CVL1 normal. | Evidência suporta `historical_blocked_specify_semantics`. |
| P4 `StakedAaveV3Harness` | Documentos originais fazem referência a `munged` gerado por Makefile + patch; snapshots/identidade do binário pós-transformação não foram autenticados. | Não substituir com Solidity `src` bruto; 27 incomplete preservados. |
| P22/incomplete/4 | `checkBurnLiquidityShare` chama `totalSupply()`; o `N.txt` identifica campo não público de `PoolActionsWrapper`, sem getter ABI. | Falta getter; não inventar uma função. |
| P22/incomplete/5 | `checkBurnExactLiquidity` contém `require to == e.msg.sender` sem argumento/local `to` declarado. O `address to` de outra rule não entra neste escopo. | Símbolo CVL livre, separado do caso do getter. |
| P22 runner | `verifyPopsicleV3Optimizer.sh` seleciona `PopsicleV3Optimizer.spec` com `--rule $1`; não comprova execução de FullMathWrapper/PoolActions/sanity. | `historical_run_unattributed` é mais preciso que inventar resultados históricos. |

## Parecer e ressalvas

**Sem discrepância estrutural identificada** nas 159 instâncias ou na distribuição de blockers; a classificação de fechamento histórico é sustentada pelas evidências amostradas. Este parecer é **revisão de integridade integral mais exame semântico seletivo**, não reexecução de 159 provas nem auditoria semântica exaustiva das 159 assertions. Recomendo manter PR #38 **Draft** e os 159 exemplos **UNRESOLVED**, conforme decisão anterior do coordenador. `historical_blocked` significa ausência de artefatos confiáveis no corpus conhecido, não impossibilidade matemática de migração.

Não executei Prover, CVL1 ou qualquer compilação CVL2 para o PR #38; não criei comentários, commits, branches, alterações nem avaliações formais no PR do AGENTE-06. Relatório publicado unicamente na pasta do AGENTE-05, para rastreabilidade da contrarrevisão.

## Adendo: HEAD concorrente do AGENTE-06 na Rodada 4

Durante a revisão, o PR #38 avançou de `684bd419ee8e35f27ca7ee07138fced321160793` para **`3957390bedcdf8dcc70d753dfe3a437d16a5fbe8`**. O delta entre essas duas HEADs é **exclusivamente a adição** de `ROUND4_PROGRESS_159.csv`, `ROUND4_QA.md` e `ROUND4_TECHNICAL_FINDINGS.md`, todos em `docs/cvl2/research/AGENTE-06/`. A análise detalhada acima refere-se à base documental `684bd419`; o novo delta também foi examinado em modo somente leitura.

- No novo `ROUND4_PROGRESS_159.csv`, os **159** registros têm chaves únicas idênticas às de `historical_closure_decisions.csv`, repartidas em 70/27/41/21. Os 159 registros declaram `MATCH` de integridade, `NOT_RUN_HISTORICAL_ABI_OR_TARGET_UNPROVEN`, `NOT_DEMONSTRATED` e `implementation_authorized=NO`.
- `ROUND4_TECHNICAL_FINDINGS.md` mantém explícito que `queue2` não é `queue` (P1), `munged` requer patch/geração autenticados (P4), `Specify 2019` não pode ser convertido por simples sintaxe (P17), e a única runner capturada do Popsicle inclui `--rule $1` sem provar quais IDs rodaram (P22). A triagem P17 separa contagens lexicais de semântica efetiva; essa ressalva é necessária.
- `git -c core.whitespace=cr-at-eol diff --check BASE...origin/research/cvl2-agente-06` foi reexecutado no **novo HEAD 3957390b**, com **EXIT 0**; o checkout usado para esse check pertence ao AGENTE-05 e não modificou a worktree do AGENTE-06.
- A avaliação anterior de 159 hashes/artefatos diz respeito aos arquivos que permaneceram inalterados entre as duas HEADs. O novo CSV acrescenta evidência documental, **não** compilação CVL2 nem liberação de migração.

**Parecer atualizado para a HEAD 3957390b:** sem divergência estrutural encontrada no delta; gate de Fase 2 continua fechado para 159/159. PR #38 permanece Draft. Nenhuma escrita no PR/branch/worktree do AGENTE-06 foi realizada nesta contrarrevisão.
