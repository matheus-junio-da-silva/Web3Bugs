# AGENTE-04 — Project 15 QA (Phase 1)

## Reconciliation
- Entry Web3Bugs commit `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`; PropertyGPT main `687f654c679ed45ab127b7949e2a29c8f5e491b9`; reviewed upstream GHO SHA `ce49fb0c94cfebf0159222ceb288e4f9a55d305f` independently confirmed to exist.
- Current pinned CSV: **116** canonical unique examples, all incomplete. 116 individual extracted N.spec and associated N.txt files were read through GitHub in the dossier batches. 116 individual dossiês and 17 batch CSVs prepared, then consolidated in `properties.csv`.
- Formal Results in pinned CSV: 63 VERIFIED, 53 NOT_STATED. Historical older `docs/spec_catalog_project_15.md` says 64 VERIFIED / 52 NOT_STATED; discrepancy is accounted for by the final pinned main adjudication of `balance_after_burn`. No historical Result is a claim of verification under CVL2 now.
- Family counts: `contracts/15/flashMinter.spec` 6; `contracts/15/ghoAToken.spec` 7; `contracts/15/ghoDiscountRateStrategy.spec` 1; `contracts/15/ghoToken.spec` 28; `contracts/15/ghoVariableDebtToken.spec` 25; `contracts/15/set.spec` 27; `contracts/15/VariableDebtToken.spec` 22.
- 238 evidence records (232 property-linked) and 7 groups in the recovery manifest. Active pattern IDs: INVARIANT (57), INVOKE (1), METHODS (116), SELECTOR (51), SUMMARY (60), USING (66).
- CSV coverage, uniqueness and expected range 1…116 verified within the GitHub consolidation operation. No changing the original labels, snapshots, .spec/.sol, configs or catalog index.

## Incomplete research and semantic risks
- Historical PDF pages, source-level `N.md` comments, official Prover run flags/.conf, external package Git hashes and exact compiler/remapping configurations were **not independently reconciled one by one** in this initial documentation pass. Existing catalog provenance for 22 Solidity and 8/9 CVL blobs was consulted, not reproduced from upstream blobs in this pass.
- All recovery groups remain `UNRESOLVED_PROVENANCE`; no `RECOVERABLE_WITH_PROVENANCE` claim. The 116 candidates remain `UNRESOLVED_CANDIDATE`, even when a lexical replacement is straightforward.
- `METHODS` and `SUMMARY` application requires receiver-specific ABI verification; `INVARIANT`, `ghost` and `hook` require inductive/vacuity audit; arbitrary `require_` narrowing forbidden. Unrolling limit 2 and assume-Aave-V3-Pool correctness remain historical constraints from report, not new assumptions.

## Checks not performed
- No CLI version discovery, no solc or CVL compilation, no Prover/CVL1 verification, no experimental semantic equivalence. Repository's Python validators and `git diff --check` were not executed locally because the remote desktop device was offline; the GitHub base-to-branch comparison found 206 changed files, all under the AGENTE-04 research path, with exactly 157 individual property dossiers; no original .spec, Solidity, scripts or catalogs were changed. This comparison is not equivalent to local `git diff --check`.
- This is evidence-linked pre-migration research, NOT an approved Phase 2 implementation or final compilation bucket.

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.**
