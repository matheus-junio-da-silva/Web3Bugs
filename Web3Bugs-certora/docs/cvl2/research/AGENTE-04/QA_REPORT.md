# AGENTE-04 — cross-project QA and handover (2026-10-19)

- Baseline Web3Bugs `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`, PropertyGPT `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- All 3 `properties.csv` parsed as quoted CSV. **157 distinct canonical keys**: Project 2 (1 complete, 14 incomplete), Project 12 (17 complete, 9 incomplete), Project 15 (0 complete, 116 incomplete). Total: **18 complete / 139 incomplete**.
- GitHub compare from baseline to draft branch, checked at commit `925c1e8edf68128a123380d8f485e46fc571ed49`: 24 commits ahead, 206 changed files, all inside `Web3Bugs-certora/docs/cvl2/research/AGENTE-04/`. Exactly **157** new individual dossier paths, all referenced by their corresponding `properties.csv`. No changes to historical `.spec`, `.sol`, contracts snapshot, catalogs, CSV original, scripts or reports.
- The GitHub compare scope test is distinct from execution of `git diff --check`; CLI/solc/Prover were **not** executed.
- The Project 15 pinned baseline includes semantic adjudication that shifted one `balance_after_burn` historic result to NOT_STATED; do not overwrite it with older catalog markdown values.
- Cross-project assumptions not treated as proven: recovery of historical hidden harnesses, blob-identity of external dependencies, original Prover configs, quantified reachability, preserved/invariant induction, receiver scope of summaries, no-loss-of-counterexamples under casts, report per-rule attribution.
- Research files may contain candidate patterns whose precise applicability remains provisional; links/evidence and individual CVL snippets are checkpoints for coordinator review, not automated migration instructions.
- No attempt was made to create Fase 2 code, alter source history or merge.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**
