# Project 6 — Aave Static aToken Spec Catalog

This document records the adversarially reviewed catalog state for Project 6.

## Scope

Selected PropertyGPT snapshot:

- /home/mat/certora-ac-audit/PropertyGPT/certora_projects/aave_static_token

Preserved files:

- contracts/6/StaticATokenLM.spec
- contracts/6/rewardPreserve.spec
- contracts/6/StaticATokenLM.sol
- contracts/6/ERC20.sol
- resources/6/Formal_Verification_Report_staticAToken.pdf
- reports/6.md — full 16-page text extraction plus finding anchors

## Active property coverage

The source scan strips block comments and line comments before recognizing top-level rule/invariant declarations.

- StaticATokenLM.spec: 27 active properties — 19 rules and 8 invariants.
- rewardPreserve.spec: 5 active rules.
- Total active selected-source properties: **32**.
- Complete examples: **0**.
- Incomplete examples: **32**.
- Bug Label relationship rows: **33** because example 29 has two independently defensible technical relationships.

All active selected-source declarations are represented exactly once as examples 1–32.

## Why PropertyGPT says 24 while the selected source has 32

reports_info.md records CountOfProperty = 24 for Aave Static aToken. The review traced that number to the existing PropertyGPT extraction output, not to the literal active declaration count.

combined_output_train_all.csv has exactly 24 rows for aave_static_token. Compared against the source declarations it:

- omits 9 active declaration starts:
  - inv_balanceOf_leq_totalSupply
  - inv_atoken_scaled_balanceOf_leq_totalSupply
  - sumAllBalance_eq_totalSupply
  - sumAllATokenScaledBalance_eq_totalSupply
  - singleAssetAccruedRewards
  - getClaimableRewards_stable_after_initialize
  - sanity
  - rewardsConsistencyWhenSufficientRewardsExist
  - rewardsConsistencyWhenInsufficientRewards
- contains one partial/misnamed extraction beginning at StaticATokenLM.spec line 601 named getClaimableRewards_stable, even though the actual active rule is getClaimableRewards_stable_after_initialize at line 606.

Therefore 24 is an extractor artifact. The catalog correctly uses the 32 literal active declarations and does not discard properties to match the older count.

## Target Contract review

The previous catalog asserted StaticATokenLMHarness as the Target Contract. The review found that this was stronger than the available evidence.

Evidence supporting a harnessed target exists:

- StaticATokenLM.spec contains harness-only unqualified getters such as getRewardTokensLength/getRewardToken.
- The spec names a StaticATokenLMHarness contract type.

However, the selected snapshot does not contain:

- the historical verify command;
- the harness source;
- the original Certora configuration/link configuration.

The report names StaticATokenLM.sol as the main contract in scope, but a source filename is not proof of the exact Certora verification target.

For fidelity, all Project 6 CSV rows now use:

- Target Contract: **UNSPECIFIED**

Each example documents that a StaticATokenLMHarness-style verification target is the strongest inference, but is not independently confirmed.

## Source-version drift

The preserved PDF states:

- verification period: January 18 through March 31, 2023;
- latest commit reviewed and run through the Certora Prover: **ac92951**;
- scope: StaticATokenLM.sol and RayMathExplicitRounding.sol.

The prior catalog incorrectly recorded 51d46b1, a July 2023 commit. That error has been corrected in every Project 6 .md/.sol and in reports/6.md/docs.

The supplied PropertyGPT StaticATokenLM.sol has SHA-256:

bda34b0ece56a79386e5d3d2d966ca28fb5e62401a9e40e2493741621a30a971

It is byte-identical to upstream commit:

13a004738c533f11710400c1757b9570ef1e0466 — 2023-03-13 — PR #25

The supplied revision is an ancestor of ac92951. Between it and the report head, StaticATokenLM changed through at least:

- PR #27: continue instead of return when a zero reward address is encountered;
- PR #29: explicit registered-reward state/validation and RewardIndexCache;
- PR #32: max getter changes/additions;
- ac92951: lint/alignment commit on top of those changes.

Accordingly, supplied Solidity is used only as historical implementation context. Formal Result values come from report evidence, never from the supplied code.

## Incomplete status

All 32 examples remain incomplete. This is not a CVL1/CVL2 issue.

Missing or unreconstructable historical dependencies include:

- the imported erc20.spec;
- exact verification target/harness source and run configuration;
- AToken implementation/harness used by _AToken;
- RewardsControllerHarness;
- DummyERC20_aTokenUnderlying;
- DummyERC20_rewardToken;
- SymbolicLendingPoolL1;
- TransferStrategyHarness;
- ScaledBalanceTokenHarness;
- AToken _userState layout used by hooks;
- local interface/library files imported by supplied StaticATokenLM.sol;
- external Aave and solidity-utils dependency trees.

rewardPreserve.spec also exposes older single-reward ABI shapes that do not match the supplied production Solidity, including one-argument getUnclaimedRewards and zero-argument claimRewardsToSelf.

The broader PropertyGPT tree contains unrelated erc20.spec files and similarly named mocks, but none is silently substituted.

## Formal results

Across the 32 source property instances:

- VERIFIED: **8**
- VIOLATED: **0**
- NOT_STATED: **24**

The eight source instances receiving VERIFIED have direct exact-name final-report evidence:

- rewardsConsistencyWhenSufficientRewardsExist (#37)
- rewardsConsistencyWhenInsufficientRewards (#38; also detected issue #4)
- singleAssetAccruedRewards (#40)
- totalAssets_stable (#41)
- reward_balance_stable_after_collectAndUpdateRewards (#42)
- totalClaimableRewards_stable (#43)
- getClaimableRewards_stable (#44; also detected issue #1)
- getClaimableRewardsBefore_leq_claimed_claimRewardsOnBehalf (#45)

Source comments such as pass, fail, should fail, timeout, todo remove and old prover links are annotations only; they never create Result values.

### Property #39 aggregate-result correction

The report check-marks conceptual Property #39 rewardsTotalDeclinesOnlyByClaim, but explicitly says the check was split into three parametric rules to avoid timeouts.

The selected rewardPreserve.spec contains multiple source rules around that concept:

- rewardsTotalDeclinesOnlyByClaim
- rewardsTotalDoesNotDeclineByWithdraw
- rewardsTotalDoesNotDeclineByDeposit

The report does not identify a source-file/rule-instance result for those split bodies, and the selected generic source rule itself contains an older Failed (e.g. withdraw) prover annotation.

Following the catalog rule against propagating aggregate report results, **all three source instances are NOT_STATED**. The report-level checkmark remains documented as contextual evidence only.

## Detection Outcome

Across unique examples:

- FINDING: **2**
- ACCEPTED_BEHAVIOR: **0**
- NO_FINDING: **6**
- INCONCLUSIVE: **0**
- NOT_STATED: **24**

Two exact selected properties detected historical report issues while being verified on the final reviewed revision:

- Example 15 — getClaimableRewards_stable: VERIFIED + FINDING for issue #1.
- Example 29 — rewardsConsistencyWhenInsufficientRewards: VERIFIED + FINDING for issue #4.

This is intentional: Result describes the final report status; Detection Outcome records that the property detected a historical audit issue.

## Report findings

Five report issues are recorded in results/bugs.csv.

- SAT-01 — S2-1 — Medium: unregistered reward address is accepted into reward-accounting queries/flows without registered-reward validation. The PR #29 fix explicitly added registered-reward validation. The detecting property itself has S6-4 accounting-stability intent.
- SAT-02 — L2 — Low: one-share-worth asset loss from rounding mismatch. Report Property #14 is absent from the selected specs.
- SAT-03 — L2 — Low: rounded-to-zero deposit can violate EIP-4626 revert semantics. Report Properties #11/#12 are absent from the selected specs.
- SAT-04 — S6-2 — Informational: getUnclaimedRewards returned a quantity in inconsistent units. Exact selected Property #38 detected it.
- SAT-05 — L7 — Informational: theoretical overflow/revert in totalAssets/maxWithdraw at extreme amounts. Report Properties #21/#26 are absent from selected specs.

The report also contains a Recommendation concerning _claimRewardsOnBehalf stopping at address(0), fixed by PR #27. It remains a recommendation and is not promoted to a vulnerability row.

## Property-level Bug Labels

Relationship-row counts:

- S6-4: **24**
- S6-2: **2**
- UNMAPPED: **7**
- Total relationships: **33**

Two label refinements were made during review:

1. singleAssetAccruedRewards is S6-2, not the broader S6-4. Its assertion is specifically about two reward getters returning semantically consistent values in the one-asset case.
2. rewardsConsistencyWhenInsufficientRewards has two defensible relationships:
   - S6-4 for payout/unclaimed/claimable conservation assertions;
   - S6-2 for getter-value/unit semantics, which is the mechanism of report issue #4.

This preserves the distinction between technical property relationships and final finding labels.

## UNMAPPED diagnostic/development rules

Seven rules remain UNMAPPED:

- totalClaimableRewards_stable_SANITY
- totalClaimableRewards_stable_after_initialized
- getClaimableRewards_stable_SANITY
- getClaimableRewards_stable_after_initialize
- sanity
- sanity_metaDeposit
- sanity_metaWithdraw

Reasons include deliberate assert false reachability probes, source comments saying should fail, and pre-initialization probes that the source itself questions/removes. A security label would overstate these rules.

The later getClaimableRewards_stable_after_metaWithdraw and getClaimableRewards_stable_after_withdraw rules are located in a development section but retain S6-4 because their executable assertions state a concrete reward-accounting stability requirement rather than generic reachability.

## Report assumptions and qualifiers

Report-wide assumptions preserved in the examples include:

- reward token for a reward-bearing aToken is not the aToken itself;
- a registered reward exists in the Incentives Controller and configureAssets has populated the relevant reward state;
- sum of balances equals totalSupply, so each balance is bounded by totalSupply;
- loops are unrolled;
- non-multi-reward violations requiring more than one loop iteration may be missed;
- multi-reward violations requiring more than two loop iterations may be missed.

The PDF layout was also inspected for property-specific footnotes:

- Property #37 carries footnote [4]: msg.sender is not the StaticATokenLM.
- Property #38 carries footnotes [4] and [7]: msg.sender is not the StaticATokenLM and is not the TransferStrategy.
- Aggregate Property #39 carries footnote [4]: msg.sender is not the StaticATokenLM.

Those qualifiers are now explicit in examples 28–30.

## Important semantic limitations

### getClaimableRewardsBefore_leq_claimed_claimRewardsOnBehalf

The selected CVL measures DummyERC20 reward-token balance of onBehalfOf before and after claimRewardsOnBehalf(onBehalfOf, receiver, rewards), while the Solidity claim path transfers to receiver.

Therefore the source rule proves only its literal upper bound on the measured onBehalfOf balance delta. It is not described as an exact-payment or correct-recipient proof.

### singleAssetAccruedRewards

The rule is conditional: only when the rewards-controller asset list has exactly one asset equal to the symbolic asset does it require equality of the aggregate and per-asset accrued getters. It is not a general multi-asset consistency proof.

### AToken invariants

Several invariants directly rely on _AToken.balanceOf, scaledBalanceOf, totalSupply, scaledTotalSupply and _userState storage layout. The dependent AToken implementation/harness is absent, so the available StaticATokenLM excerpts cannot reproduce those proofs.

### rewardPreserve ABI drift

rewardPreserve.spec and StaticATokenLM.spec are not a clean single-ABI snapshot. The older rewardPreserve signatures are retained literally rather than normalized to the supplied Solidity.

### Common dispatcher block

Several extracted specs retain the common CVL dispatcher/model declarations from the original methods block. Because the historical linked harness call graph is missing, this is conservative source preservation rather than a claim that every retained dispatcher is individually necessary to the selected assertion. Missing dependencies are not inferred solely from an unrelated retained dispatcher; the examples are incomplete independently because the import/target/harness tree is absent.

## Property coverage table

| Example | Property | Bug Label relationship | Result | Detection Outcome | Nature |
| ---: | --- | --- | --- | --- | --- |
| 1 | inv_balanceOf_leq_totalSupply | S6-4 | NOT_STATED | NOT_STATED | normative |
| 2 | inv_atoken_balanceOf_leq_totalSupply | S6-4 | NOT_STATED | NOT_STATED | normative |
| 3 | inv_atoken_balanceOf_leq_totalSupply_redeem | S6-4 | NOT_STATED | NOT_STATED | normative |
| 4 | inv_atoken_balanceOf_2users_leq_totalSupply | S6-4 | NOT_STATED | NOT_STATED | normative |
| 5 | inv_atoken_scaled_balanceOf_leq_totalSupply | S6-4 | NOT_STATED | NOT_STATED | normative |
| 6 | sumAllBalance_eq_totalSupply | S6-4 | NOT_STATED | NOT_STATED | normative |
| 7 | sumAllATokenScaledBalance_eq_totalSupply | S6-4 | NOT_STATED | NOT_STATED | normative |
| 8 | singleAssetAccruedRewards | S6-2 | VERIFIED | NO_FINDING | normative |
| 9 | totalAssets_stable | S6-4 | VERIFIED | NO_FINDING | normative |
| 10 | totalAssets_stable_after_collectAndUpdateRewards | S6-4 | NOT_STATED | NOT_STATED | normative |
| 11 | reward_balance_stable_after_collectAndUpdateRewards | S6-4 | VERIFIED | NO_FINDING | normative |
| 12 | totalClaimableRewards_stable | S6-4 | VERIFIED | NO_FINDING | normative |
| 13 | totalClaimableRewards_stable_SANITY | UNMAPPED | NOT_STATED | NOT_STATED | diagnostic |
| 14 | totalClaimableRewards_stable_after_initialized | UNMAPPED | NOT_STATED | NOT_STATED | diagnostic |
| 15 | getClaimableRewards_stable | S6-4 | VERIFIED | FINDING | normative |
| 16 | getClaimableRewards_stable_SANITY | UNMAPPED | NOT_STATED | NOT_STATED | diagnostic |
| 17 | getClaimableRewards_stable_after_deposit | S6-4 | NOT_STATED | NOT_STATED | normative |
| 18 | getClaimableRewards_stable_after_atoken_transferFrom | S6-4 | NOT_STATED | NOT_STATED | normative |
| 19 | getClaimableRewards_stable_after_atoken_transferFrom_1 | S6-4 | NOT_STATED | NOT_STATED | normative |
| 20 | getClaimableRewards_stable_after_initialize | UNMAPPED | NOT_STATED | NOT_STATED | diagnostic |
| 21 | getClaimableRewards_stable_after_refreshRewardTokens | S6-4 | NOT_STATED | NOT_STATED | normative |
| 22 | getClaimableRewardsBefore_leq_claimed_claimRewardsOnBehalf | S6-4 | VERIFIED | NO_FINDING | normative |
| 23 | sanity | UNMAPPED | NOT_STATED | NOT_STATED | diagnostic |
| 24 | sanity_metaDeposit | UNMAPPED | NOT_STATED | NOT_STATED | diagnostic |
| 25 | sanity_metaWithdraw | UNMAPPED | NOT_STATED | NOT_STATED | diagnostic |
| 26 | getClaimableRewards_stable_after_metaWithdraw | S6-4 | NOT_STATED | NOT_STATED | normative |
| 27 | getClaimableRewards_stable_after_withdraw | S6-4 | NOT_STATED | NOT_STATED | normative |
| 28 | rewardsConsistencyWhenSufficientRewardsExist | S6-4 | VERIFIED | NO_FINDING | normative |
| 29 | rewardsConsistencyWhenInsufficientRewards | S6-2; S6-4 | VERIFIED | FINDING | normative |
| 30 | rewardsTotalDeclinesOnlyByClaim | S6-4 | NOT_STATED | NOT_STATED | normative |
| 31 | rewardsTotalDoesNotDeclineByWithdraw | S6-4 | NOT_STATED | NOT_STATED | normative |
| 32 | rewardsTotalDoesNotDeclineByDeposit | S6-4 | NOT_STATED | NOT_STATED | normative |

## Independent review checks

The post-review audit verified:

- 32/32 active declarations found after comment stripping;
- 24 rules + 8 invariants;
- 33 Project 6 Bug Label relationships;
- all Project 6 targets are UNSPECIFIED rather than an unproved harness claim;
- literal property bodies occur unchanged inside every extracted .spec;
- every Original Spec Lines range in the CSV occurs verbatim in the extracted artifact;
- every declared Solidity provenance range occurs verbatim in the .sol excerpt;
- required .md sections and .txt incomplete reasons exist for all 32 examples;
- no stale 51d46b1 reference remains in Project 6 .md/.sol;
- the preserved PDF independently extracts ac92951 as the latest reviewed commit;
- Property #39 aggregate status is not assigned to examples 30–32;
- example 8 has S6-2;
- example 29 has both S6-4 and S6-2;
- SAT-01 uses S2-1;
- source and report hashes remain unchanged;
- the PropertyGPT 24-count discrepancy is reproducibly explained by 9 omitted active starts plus one partial/misnamed extractor record.

## Validation

The literal python commands requested by the workflow remain unavailable because the machine has no python executable alias.

Equivalent python3 validators after review:

- python3 scripts/check_specs.py . — PASS: 164 spec examples and 169 Bug Label relationships are structurally consistent.
- python3 scripts/check_contests_csv.py . — PASS.
- python3 scripts/check_contracts.py . — PASS.

Additional adversarial audit:

- PYTHONPATH=/tmp/project6_pdfdeps python3 /tmp/project6_review_audit.py — PASS.

These checks validate catalog/source/report consistency; they do not rerun the Certora Prover.

## Final reviewed status

- Total selected-source active properties: **32**
- Complete: **0**
- Incomplete: **32**
- VERIFIED: **8**
- VIOLATED: **0**
- NOT_STATED: **24**
- FINDING: **2**
- NO_FINDING: **6**
- NOT_STATED outcomes: **24**
- UNMAPPED properties: **7**
- Bug Label relationships: **33**

The reviewed catalog deliberately prefers UNSPECIFIED/NOT_STATED/UNMAPPED where the evidence does not justify a stronger claim.
