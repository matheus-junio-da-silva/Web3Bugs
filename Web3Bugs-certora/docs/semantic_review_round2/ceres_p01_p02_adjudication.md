# CERES — correction adjudication for Projects 1 and 2

Date: 2026-10-18. Source branch: main at 80f551f23bbd86d7901c6a28e7f44c68aebae8fd.

GAIA source revision (gaia_review.csv and gaia_summary.md) publication was requested in PR #8, comment 6255647257, in review/gaia-semantic-round2 as a separate documentary PR. It was not available at the time of this correction; this is NOT a surrogate GAIA revision.

65 findings are enumerated below. The first 64 are distinct generic Solidity explanation rewrites; two of these also require a Bug Label change. The 65th is a Project 2 Bug Label adjudication. No original .spec/.sol/PDF/contracts files were changed.

## 65-case checklist

| # | Example | Property | Classification | Decision |
|---:|---|---|---|---|
| 1 | complete/1/1 | whoChangedStateVariables | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 2 | complete/1/2 | queuedChangedCounter | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 3 | complete/1/3 | independentQueuedActions | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 4 | complete/1/4 | queuePriviliged | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 5 | complete/1/5 | properDelay | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 6 | complete/1/6 | minDelayLtMaxDelay | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 7 | complete/1/7 | queueDoesntModifyStateVariables | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 8 | complete/1/8 | queueCannotCancel | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 9 | complete/1/9 | noIncarnations2 | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 10 | complete/1/10 | noIncarnations3 | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 11 | complete/1/11 | executedForever | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 12 | complete/1/12 | canceledForever | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 13 | complete/1/13 | expiredForever | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 14 | complete/1/14 | cancelExclusive | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 15 | complete/1/15 | whoChangesActionsSetState | DOCUMENTATION_FIX + LABEL_CHANGE | S3-2 to UNMAPPED: legal execute/cancel modifies state |
| 16 | complete/1/16 | holdYourHorses | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 17 | complete/1/17 | executedValidTransition1 | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 18 | complete/1/18 | executedValidTransition2 | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 19 | complete/1/19 | executeFailsIfExpired | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 20 | complete/1/20 | sameExecutionTimesReverts | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 21 | complete/1/21 | actionDuplicate | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 22 | complete/1/22 | processMessageFromRootReachability | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 23 | complete/1/23 | cancelPriviliged | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 24 | complete/1/24 | properDelay | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 25 | complete/1/25 | minDelayLtMaxDelay | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 26 | complete/1/26 | whoChangedStateVariables | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 27 | complete/1/27 | noIncarnations2 | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 28 | complete/1/28 | executedForever | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 29 | complete/1/29 | canceledForever | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 30 | complete/1/30 | expiredForever | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 31 | complete/1/31 | cancelExclusive | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 32 | complete/1/32 | whoChangesActionsSetState | DOCUMENTATION_FIX + LABEL_CHANGE | S3-2 to UNMAPPED: legal execute/cancel modifies state |
| 33 | complete/1/33 | executedValidTransition1 | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 34 | complete/1/34 | executedValidTransition2 | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 35 | complete/1/35 | executeFailsIfExpired | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 36 | complete/1/36 | cancelPriviliged | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 37 | incomplete/1/1 | queuePriviliged | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 38 | incomplete/1/2 | actionNotCanceledAndExecuted | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 39 | incomplete/1/3 | notCanceledNotExecuted | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 40 | incomplete/1/4 | executeCannotCancel | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 41 | incomplete/1/5 | noIncarnations1 | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 42 | incomplete/1/6 | queuedStateConsistency | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 43 | incomplete/1/7 | onlyCancelCanCancel | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 44 | incomplete/1/8 | executeRevertsBeforeDelay | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 45 | incomplete/1/9 | afterQueueHashQueued | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 46 | incomplete/1/10 | onlyQueuedAreExecuted | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 47 | incomplete/1/11 | actionNotCanceledAndExecuted | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 48 | incomplete/1/12 | notCanceledNotExecuted | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 49 | incomplete/1/13 | queueDoesntModifyStateVariables | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 50 | incomplete/1/14 | queueCannotCancel | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 51 | incomplete/1/15 | executeCannotCancel | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 52 | incomplete/1/16 | noIncarnations1 | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 53 | incomplete/1/17 | noIncarnations3 | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 54 | incomplete/1/18 | queuedStateConsistency | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 55 | incomplete/1/19 | queuedChangedCounter | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 56 | incomplete/1/20 | onlyCancelCanCancel | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 57 | incomplete/1/21 | holdYourHorses | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 58 | incomplete/1/22 | executeRevertsBeforeDelay | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 59 | incomplete/1/23 | sameExecutionTimesReverts | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 60 | incomplete/1/24 | independentQueuedActions | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 61 | incomplete/1/25 | afterQueueHashQueued | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 62 | incomplete/1/26 | onlyQueuedAreExecuted | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 63 | incomplete/1/27 | actionDuplicate | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 64 | incomplete/1/28 | queue2Reachability | DOCUMENTATION_FIX | Specific CVL/target/Solidity explanation written; other metadata preserved |
| 65 | complete/2/1 | PoRFeedChange | LABEL_CHANGE + DOCUMENTATION_FIX | Extra S2-1 relation deleted; S3-2 retained, VERIFIED/NO_FINDING unchanged |

## Semantic judgments

1. whoChangesActionsSetState: filter only !f.isView; no filter excludes execute/cancel. Those methods set executed/canceled flags legitimately. The source asserts unqualified state equality, so its raw security label is UNMAPPED. We did not introduce source filters or infer new Solidity flaws.
2. PoRFeedChange: call_f_with_params dispatches three selectors; asserts values in feed/wrapper mappings after successful operation and that other selectors cannot change them. There is no assertion testing invalid asset IDs or require(asset != address(0)); S2-1 is not proved by the nonzero mapped feed/wrapper values. Retain S3-2.
3. Results and outcomes were not modified; verified outcomes are tied only to the historical report as documented. The Polygon vs Optimism/Arbitrum queue origin guards are different even when BridgeExecutorBase is shared.

## Evidence gaps

- EVIDENCE_GAP — original GAIA CSV/summary not yet published; cannot resolve the GAIA-specific set of six inconclusive P2 IDs without them. No guessed IDs were assigned.
- EVIDENCE_GAP — P1 incomplete/1/29–34 complexity diagnostics: unresolved original target, no invented target/method/harness.
- EVIDENCE_GAP — P2 historical helper implementations such as allBacked, areAllReservesBackedCorrelation, getAssetState/getAssetsLength and single-asset mutations: original incomplete status remains.
- EVIDENCE_GAP — P1 original PDF absent from Git main; reports/1.md is a transcript, not proof that individual PDF checkmarks were visually audited. P2 historical PDF is preserved in resources/2.
- EVIDENCE_GAP — instrucoes-obrigatorias.txt not found in Git tree despite requested mandatory reading; no assumptions about its absent content.
- P1 historic report references commit 303bd3e1, unroll limit 2, simplified queue2, external call side-effect assumptions and limited treatment of delegatecall executor-state changes; no Prover reexecution.
- No RESULT_OUTCOME_CHANGE or DEPENDENCY_FIX; historical .spec/.sol/PDF and unrelated projects preserved.

## Shared CSV reconciliation

Only the two S3-2 to UNMAPPED substitutions at Project 1 complete IDs 15 and 32 and deletion of the additional S2-1 Project 2 complete ID 1 relationship. All remaining original CSV records are byte-identical to main.

## Validation

Executed commands, exit codes, log files and the final commit SHA are recorded in the correction PR description after running the checks. Structural passing does not establish formal Certora results.
