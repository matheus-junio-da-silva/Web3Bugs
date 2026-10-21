# AGENTE-06 — Round 4 QA (2026-10-20)

Starting branch HEAD: \`684bd419ee8e35f27ca7ee07138fced321160793\`.
Baseline: \`2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3\`.

Isolated worktree: \`/home/mat/agente06-round4-20261020\` (detached until publication). Original contracts, specs, reports, canonical CSV and historical classifications untouched.

## Observed local checks (worktree containing this Round 4 documentation)

- \`python3 scripts/check_specs.py .\` from \`Web3Bugs-certora\`: **EXIT 0**, 1,386 examples and 1,390 Bug Label relations validated.
- \`python3 scripts/check_contracts.py .\`: **EXIT 0**, consistency with reports.
- \`python3 scripts/check_contests_csv.py .\`: **EXIT 0**, consistency with reports.
- Independent CSV check: **EXIT 0**; \`ROUND4_PROGRESS_159.csv\` contains 159 unique canonical keys exactly matching \`historical_closure_decisions.csv\`; 159 N.spec SHA-256 and available per-example N.md/N.sol/N.txt SHA-256 checked against preexisting per-project matrices.
- All 159 CSV rows say \`NOT_RUN_HISTORICAL_ABI_OR_TARGET_UNPROVEN\` and \`NOT_DEMONSTRATED\`: these labels mean **no CVL2 run and no equivalence proof**, not a failed test.
- \`git -c core.whitespace=cr-at-eol diff --check BASE...HEAD\` must be validated **after the new docs are committed**; result to be recorded in the GitHub PR discussion from the exact final commit.

## Limits

This check verifies documentary keys/hashes and script integrity, **not** transitive historical source closure, CVL2 compilation, CVL1 semantics, original verification result, or Prover equivalence. No source-side action has been performed.
