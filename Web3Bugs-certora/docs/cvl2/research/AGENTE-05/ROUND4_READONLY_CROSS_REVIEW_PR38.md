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
