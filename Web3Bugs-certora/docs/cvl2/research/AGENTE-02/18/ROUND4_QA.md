# AGENTE-02 — Round 4 QA / Scope and validation

Date: 2026-10-20. PR [#37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37); baseline `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Worktree unique: `/home/mat/cvl2-agente02-round4` branch `research/cvl2-agente-02-round4-local` derived from PR HEAD `3da04efedfe6d75b049b15fa37a040572260eca4`; push destination only `research/cvl2-agente-02` after verifying that the remote branch has not advanced.

## Reproduced validation at worktree (from `Web3Bugs-certora/`)

```text
python3 scripts/check_specs.py .          exit 0 — 1386 examples, 1390 Bug Label relations
python3 scripts/check_contests_csv.py .   exit 0
python3 scripts/check_contracts.py .      exit 0
```

Additional read-only Python reconciliation: `properties.csv` versus `round4_diagnostic_matrix.csv`, primary key (`project_id`, `original_status`, `example_id`) and `property`/`target`/`original_spec` equality **181/181**, all 181 dossiês presentes, 69 complete + 112 incomplete, 50 NOT_RUN/131 BLOCKED, no COMPILE_OK/COMPILE_ERROR, 181 SEMANTIC_UNRESOLVED; 10 SHA in `round4_source_identity.csv`. **exit 0**.

## Precisely what was and was not executed

- GitHub historical `fetch_file`: 10 OpenZeppelin Solidity blobs at pinned audited SHA and five Rocket Joe artifacts at pinned SHAs; local `git hash-object` of 10 corresponding OpenZeppelin snapshot files matched the remote blob IDs.
- **No Certora compilation invocation, no compiler output, no `--compilation_steps_only` diagnostic claimed, no Prover, no CVL1, no migration script, no local ABI reconstruction.** A call to inspect wrapper version `certoraRun --version` was pre-empted by local `CERTORAKEY` guard, not Certora compilation and not counted as a failure.
- No original files or catalog CSV were written. The diagnostic CSV adds separate status axes; it does not change original `Result`, `Detection Outcome` or dependency completeness.
- No mutation performed on AGENTE-03 PR #36; comparison there is sample-based, with explicitly stated limits.

## Git diff acceptance gate

From worktree *after committing* the documentary changes:

```bash
git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
git diff --name-only 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
```

Accept only exit 0 on the first command and paths all within `Web3Bugs-certora/docs/cvl2/research/AGENTE-02/18/` on the second. An empty `git diff --cached --check` is not a substitute for the committed-diff check.

**AGENTE-02 — RODADA 4**
