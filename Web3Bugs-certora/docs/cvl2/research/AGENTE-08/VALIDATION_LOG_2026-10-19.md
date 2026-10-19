# AGENTE-08 — WSL validation (2026-10-19)
Isolated worktree: /home/mat/cvl2-agente08-review2/worktree (fresh filtered sparse Git clone + isolated git worktree). Local branch local/agente08-review2 tracks origin/research/cvl2-agente-08.

## Commands and observed results
Working directory: worktree/Web3Bugs-certora.

- python3 scripts/check_specs.py . : EXIT 0; Check passed! 1386 spec examples and 1390 Bug Label relationships are structurally consistent.
- python3 scripts/check_contests_csv.py . : EXIT 0; Check passed!; ./results/contests.csv is consistant with ./reports.
- python3 scripts/check_contracts.py . : EXIT 0; Check passed!; ./contracts is consistant with ./reports.
- git diff --check : EXIT 0; no output.
- git diff --name-only | grep -v paths under Web3Bugs-certora/docs/cvl2/research/AGENTE-08/ | wc -l : 0 out of scope paths.
- Independent Python comparison: 155 canonical unique examples, 155 reports, original Property/Result/Detection Outcome unchanged, 155 UNRESOLVED_CANDIDATE.

## Initial false failures due to sparse checkout
First run omitted reports/; check_contests_csv.py and check_contracts.py returned FileNotFoundError ./reports (exit 1). Adding reports/resources/results fixed check_contests. check_contracts initially printed missing contract code for other project IDs because only scoped contracts were checked out; after fetching all historical contracts, final run exited 0. These were environment issues, not dataset errors.

## Deliberately not executed
No solc compiler, no CVL1/CVL2 compiler, no Certora Prover, no replay or proof of equivalence. No source file changed. After commit, compare the committed branch against the original baseline and rerun diff checks.
