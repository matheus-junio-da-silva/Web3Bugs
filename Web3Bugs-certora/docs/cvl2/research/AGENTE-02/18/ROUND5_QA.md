# AGENTE-02 — RODADA 5 / QA de integridade — 2026-10-20

Worktree independente: `/home/mat/cvl2-agente02-round5`, branch local `research/cvl2-agente-02-round5-local`. O comando de diff da HEAD **commitada** será executado após a criação do commit e novamente após o push, com resultado publicado no PR #37.

## Validadores executados da raiz `Web3Bugs-certora/`

```text
$ python3 scripts/check_specs.py .
Check passed! 1386 spec examples and 1390 Bug Label relationships are structurally consistent.

exit=0
```

```text
$ python3 scripts/check_contests_csv.py .
Check passed!

	`./results/contests.csv` is consistant with `./reports`

exit=0
```

```text
$ python3 scripts/check_contracts.py .
Check passed!

	`./contracts` is consistant with `./reports`

exit=0
```

## Reconciliação independente

- 181/181 keys únicas, 69 complete e 112 incomplete, sem trocar Property/Target/Result/Detection Outcome.
- 50 DOCUMENTED_CANDIDATE = NOT_RUN; 131 BLOCKED; 0 CVL COMPILE_OK/COMPILE_ERROR; 181 SEMANTIC_UNRESOLVED.
- Proveniência 157 ABSENT_AT_AUDITED_COMMIT e 24 CONTENT_DIFFERS.
- 4 saídas Solidity `solc` 0.8.6 `ABI_EXTRACTED` (targets distintos), 0 erros Solidity, 4 logs stdout GZIP completos e 4 stderr completos.
- 9 tentativas `certoraRun --compilation_steps_only` em scratch, todas barradas antes do parser por guard local sem `CERTORAKEY`. São preflights, não compilações CVL.
- Uma execução `patch --dry-run --batch --fuzz=0` em scratch híbrido Rocket Joe: exit 1, hunk #7 rejeitado em LaunchEvent.sol; stdout e stderr completos.
- Cópias temporárias de specs e Solidity foram verificadas por SHA-256. Fonte original não foi editada.
- Nenhum Prover, teste CVL1, migration script ou `results/cvl2/` criado.

## Comando obrigatório do diff commitado

```bash
git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
```

Escopo permitido: exclusivamente `Web3Bugs-certora/docs/cvl2/research/AGENTE-02/18/`; após commit conferir caminhos por `git diff --name-only BASE...HEAD`.

**AGENTE-02 — RODADA 5 — QUALIDADE CVL2.**
