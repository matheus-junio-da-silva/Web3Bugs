# FAROL — Project 18 semantic adjudication / round 2

Review PR #22: 24 CORRECTION_REQUIRED analyzed individually, reading unchanged original CVL and Solidity context. Created on main@80f551f23bbd86d7901c6a28e7f44c68aebae8fd.

## Decisions

- **23 CERES proposals accepted**, **1 rejected** (#45 SC, replaced with better supported SE-4), **24 documentation corrections**, **5 label changes**, **0 Result changes**, **0 Outcome changes**.
- All **94 INCONCLUSIVE** from CERES remain historically unproved absent source-specific harness, targets and assumptions.
- **Four VIOLATED/FINDING** are historical predecessor-version quorum cases (PDF p.2), not failures proved against corrected later source. No source or Results copied into current-build claims.

## Labels under docs/standard.md

| ID | Existing | CERES | FAROL | Reason |
|---:|---|---|---|---|
| 45 | S3-2 | SC | **SE-4** | Successful batch call demands valid matching array arguments; specificity SE-4 outranks generic SC; not a storage state-update rule. |
| 79 | S6-4 | UNMAPPED | **UNMAPPED** | Votes from already delegated minted tokens can legitimately increase. Ghost is not ERC20 totalSupply. |
| 80 | S6-4 | UNMAPPED | **UNMAPPED** | Burned delegated votes legitimately decrease. Ghost equality does not prove a bug. |
| 110 | S5-2 | UNMAPPED | **UNMAPPED** | Legitimate proposal cancellation before deadline can violate an overbroad execute/cancel conjunction. |
| 174 | S5-2 | UNMAPPED | **UNMAPPED** | Reverse implication passes whenever execution does NOT revert; no guarantee of blocking premature execution. |

## Priority #172/#174 — exact logical difference

- Both require hashIdCorrelation with data.length < 32, matching id hash, isOperationPending(id) and !isOperationReady(e,id) before call.
- **#172** executes execute@withrevert and asserts lastReverted. Non-reverting premature execute would violate #172.
- **#174** executes execute@withrevert, stores unused bool reverted, asserts only lastReverted => isOperationPending(id) && !isOperationReady(e,id). Logical falsifier requires a true revert and a false post-state consequent. A normally returning execute satisfies #174, even if that successful call is unsafe.
- TimelockController._timestamps, _DONE_TIMESTAMP, isOperationPending, isOperationReady, execute, _beforeCall, _execute, _afterCall are relevant. PDF p.3 has Timelock executor observation with Rules Broken: None, not a direct proof of #174.
- Neither CVL rule was edited.

## All other documentation

- IDs 13,14,51: separate sender/receiver and balance/permission assertions for ERC1155. IDs 71,76–78,95,100: voting-supply, checkpoint, past-supply and distinct delegate/other conditions.
- IDs 83–89: ERC20Wrapper three-way alias cases, wrapper and underlying supply/balance equations, including mathint value in #89 without an explicit nonnegative require.
- IDs 108,128,130: snapshot/deadline pair, conditional two-assert voting categories, conditional extension-only two assertions; no invented universal contract guarantee.
- Each amended N.md contains all literal assertions, conditions and modeling dependencies, Solidity, logical falsifier and preserved historical status.

## Integrity and evidence

- Ceres CSV SHA256 fe78bdd413b928dd85a81e9f67f592a892c028aad52853a62d26e5a028695a41 (read only from audit/p18-ceres-semantic-round2).
- Original PDF 13 pages SHA256 4a35df36c47e6e7e2b4333cb3890bc2a8cbca569e32b2fc6f24820b8a56cbc37; not altered; report describes four historical quorum failures and separately identifies test mutants.
- Three shared CSVs: only results/spec/spec_buglabel.csv changes five Project 18 rows (label and Detection Intent); results/bugs.csv and results/contests.csv remain byte-identical to main.
- docs/spec_catalog_project_18_semantic_matrix.csv now lists all assertions for the 19 multi-assert cases; CERES matrix is untouched.
- No source under contracts/18, no N.spec, N.sol, PDF or historical reports was modified. No Certora replay.

## Validation

Local command output, status, CI and SHA are recorded in farol_p18_validation.md; branch will remain unmerged.
