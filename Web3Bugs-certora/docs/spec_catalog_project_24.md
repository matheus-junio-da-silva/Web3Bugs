# Rocket Joe — Project 24 CVL catalog

Original source: `PropertyGPT/certora_projects/rocket_joe` at main SHA `687f654c679ed45ab127b7949e2a29c8f5e491b9`. The complete 8-spec, 15-Solidity-file and original-PDF archive lives in `contracts/24/`. Original report summary is `reports/24.md` and a source Git hash manifest is in `docs/spec_catalog_project_24_sources.md`.

**164 active CVL declarations, 164 target-specific instances; all 164 incomplete owing to historical missing CVL/Solidity harness closure.** Results supported for 53 individually named reported conditions, with other conditions NOT_STATED. No CVL2 migration or formal rerun is claimed.

## Exhaustive source inventory

- `LEHighLevel.spec`: 10 active declarations
- `LEInProgress.spec`: 3 active declarations
- `LEPreset.spec`: 1 active declarations
- `LEValidStates.spec`: 35 active declarations
- `LEVarTran.spec`: 19 active declarations
- `LaunchEvent.spec`: 76 active declarations
- `Staking.spec`: 19 active declarations
- `sanity.spec`: 1 active declarations

`LEInProgress.spec` retains its three active rules despite the `in progress` comments. The `Staking.spec` candidate invariants commented out under its `not fully implemented` section, and commented LE invariants, are excluded. Same-named source properties remain separate examples.

## Soundness

`../helpers/erc20.spec`, external libraries and original symbolic harness implementations are missing. The LaunchEvent report explicitly models at most one loop iteration, assumes correct WAVAX and an initialized event, and harnesses `_safeTransferAVAX` in a way that can hide reentrancy. Staking has its own initialization and nonreversion assumptions and timeout reductions. No finding in `reports/24.md` is automatically attributed to a single property. `sanity.spec` has `assert false`, is a reachability probe, and receives UNMAPPED.

## All source declarations and report status

| Example | Spec | Name | Kind | Label | Result |
|---:|---|---|---|---|---|
| 1 | `LEHighLevel.spec` | `hl_EqualityOfToken` | invariant | S6-4 | VERIFIED |
| 2 | `LEHighLevel.spec` | `hl_depositAdditivity` | rule | S6-4 | NOT_STATED |
| 3 | `LEHighLevel.spec` | `hl_withdrawAdditivity` | rule | S6-4 | VERIFIED |
| 4 | `LEHighLevel.spec` | `hl_twoSideInverse` | rule | SE-1 | VERIFIED |
| 5 | `LEHighLevel.spec` | `hl_noDepositFrontRun` | rule | S6-4 | NOT_STATED |
| 6 | `LEHighLevel.spec` | `hl_noWithdrawFrontRun` | rule | S6-4 | VERIFIED |
| 7 | `LEHighLevel.spec` | `hl_noWithdrawLiquidityFrontRun` | rule | S6-4 | NOT_STATED |
| 8 | `LEHighLevel.spec` | `hl_stoppedOnlySwitch` | rule | S3-2 | VERIFIED |
| 9 | `LEHighLevel.spec` | `hl_onlyOwnerSwitch` | rule | S5-3 | VERIFIED |
| 10 | `LEHighLevel.spec` | `hl_whatShouldRevert` | rule | S5-2 | VERIFIED |
| 11 | `LEInProgress.spec` | `transition_balThisZero` | rule | S6-4 | NOT_STATED |
| 12 | `LEInProgress.spec` | `hl_moreDepositMoreGet` | rule | UNMAPPED | NOT_STATED |
| 13 | `LEInProgress.spec` | `hl_withdrawLateMorePenalty` | rule | UNMAPPED | NOT_STATED |
| 14 | `LEPreset.spec` | `oneStateOnly` | invariant | S5-2 | NOT_STATED |
| 15 | `LEValidStates.spec` | `alwaysInitialized` | invariant | S3-2 | NOT_STATED |
| 16 | `LEValidStates.spec` | `factoryGetPairCorrelationCurrentVals` | invariant | S6-4 | NOT_STATED |
| 17 | `LEValidStates.spec` | `cl_pairAndGetPairCorrelation` | invariant | S6-4 | NOT_STATED |
| 18 | `LEValidStates.spec` | `al_issuerAllocationZero` | invariant | S6-4 | VERIFIED |
| 19 | `LEValidStates.spec` | `al_balanceLessThanAllocation` | invariant | S6-4 | VERIFIED |
| 20 | `LEValidStates.spec` | `al_userAllocationLessThanMaxAllocation` | invariant | S6-4 | VERIFIED |
| 21 | `LEValidStates.spec` | `al_issuerTimelockNonZero` | invariant | S6-4 | VERIFIED |
| 22 | `LEValidStates.spec` | `al_userTimelockSeven` | invariant | S6-4 | VERIFIED |
| 23 | `LEValidStates.spec` | `al_timelocksCorrelation` | invariant | S6-4 | VERIFIED |
| 24 | `LEValidStates.spec` | `op_incentivesCorrelation` | invariant | S6-4 | VERIFIED |
| 25 | `LEValidStates.spec` | `op_userNotWithdrawnPair` | invariant | S6-4 | VERIFIED |
| 26 | `LEValidStates.spec` | `op_userNotWithdrawnIncentives` | invariant | S6-4 | VERIFIED |
| 27 | `LEValidStates.spec` | `op_wavaxBalanceAndSumBalances` | invariant | S6-4 | VERIFIED |
| 28 | `LEValidStates.spec` | `op_avaxAllocZero` | invariant | S6-4 | VERIFIED |
| 29 | `LEValidStates.spec` | `op_lpSupplyZero` | invariant | S6-4 | VERIFIED |
| 30 | `LEValidStates.spec` | `op_PairBalanceIsZero` | invariant | S6-4 | VERIFIED |
| 31 | `LEValidStates.spec` | `op_PairAndTotalSupplyCorrelation` | invariant | S6-4 | VERIFIED |
| 32 | `LEValidStates.spec` | `op_AvaxCorrelation` | invariant | S6-4 | VERIFIED |
| 33 | `LEValidStates.spec` | `op_tokenCorrelation` | invariant | S6-4 | VERIFIED |
| 34 | `LEValidStates.spec` | `op_tokenResFixed` | rule | S6-4 | VERIFIED |
| 35 | `LEValidStates.spec` | `cl_avaxAllocSumUserBalances` | invariant | S6-4 | VERIFIED |
| 36 | `LEValidStates.spec` | `cl_avaxReservCheck` | invariant | S6-4 | VERIFIED |
| 37 | `LEValidStates.spec` | `cl_incentivesCorrelation` | invariant | S6-4 | VERIFIED |
| 38 | `LEValidStates.spec` | `cl_userAllocUnchanging` | rule | S6-4 | VERIFIED |
| 39 | `LEValidStates.spec` | `cl_avaxAllocUnchanging` | rule | UNMAPPED | VERIFIED |
| 40 | `LEValidStates.spec` | `cl_userBalanceFixed` | rule | S6-4 | VERIFIED |
| 41 | `LEValidStates.spec` | `cl_lpSupplyFixed` | rule | S6-4 | VERIFIED |
| 42 | `LEValidStates.spec` | `cl_AvaxCorrelation` | invariant | S6-4 | VERIFIED |
| 43 | `LEValidStates.spec` | `os_tokenCorrelation` | invariant | S6-4 | VERIFIED |
| 44 | `LEValidStates.spec` | `os_avaxAllocSumUserBalances` | invariant | S6-4 | VERIFIED |
| 45 | `LEValidStates.spec` | `os_avaxReserveDecrease` | rule | S6-4 | VERIFIED |
| 46 | `LEValidStates.spec` | `os_userBalanceNonIncreasing` | rule | S6-4 | VERIFIED |
| 47 | `LEValidStates.spec` | `cs_lpSupplyFixed` | rule | S6-4 | VERIFIED |
| 48 | `LEValidStates.spec` | `cs_userBalanceFixed` | rule | S6-4 | VERIFIED |
| 49 | `LEValidStates.spec` | `cs_avaxAllocatedFixed` | rule | S3-2 | VERIFIED |
| 50 | `LEVarTran.spec` | `al_userAllocationNonDecreasing` | rule | S6-4 | NOT_STATED |
| 51 | `LEVarTran.spec` | `al_stoppedOnlyByOwner` | rule | S5-3 | NOT_STATED |
| 52 | `LEVarTran.spec` | `op_balanceChangeByDepositOrWithdraw` | rule | S6-4 | NOT_STATED |
| 53 | `LEVarTran.spec` | `op_allocationChangeByDeposit` | rule | S6-4 | NOT_STATED |
| 54 | `LEVarTran.spec` | `op_tokenReserveUnchange` | rule | S6-4 | NOT_STATED |
| 55 | `LEVarTran.spec` | `op_tokenIncentivesBalanceUnchange` | rule | S6-4 | NOT_STATED |
| 56 | `LEVarTran.spec` | `op_tokenIncentivesForUsersUnchange` | rule | S6-4 | NOT_STATED |
| 57 | `LEVarTran.spec` | `op_tokenIncentiveIssuerRefundUnchange` | rule | S6-4 | NOT_STATED |
| 58 | `LEVarTran.spec` | `tr_pairOnlyChange` | rule | S3-2 | NOT_STATED |
| 59 | `LEVarTran.spec` | `tr_initializedOnlyChange` | rule | S3-2 | NOT_STATED |
| 60 | `LEVarTran.spec` | `tr_incentivesForUsersChanges` | rule | S6-4 | NOT_STATED |
| 61 | `LEVarTran.spec` | `tr_incentiveIssuerRefundChanges` | rule | S6-4 | NOT_STATED |
| 62 | `LEVarTran.spec` | `cl_unchangingPair` | rule | S3-2 | NOT_STATED |
| 63 | `LEVarTran.spec` | `cl_hasWithdrawnPair_pairBalance_OnlyChangeUser` | rule | S6-4 | NOT_STATED |
| 64 | `LEVarTran.spec` | `cl_hasWithdrawnPair_pairBalance_OnlyChangeIssuer` | rule | S6-4 | NOT_STATED |
| 65 | `LEVarTran.spec` | `cl_pairAndTokenBalancesNonIncreasing` | rule | S6-4 | NOT_STATED |
| 66 | `LEVarTran.spec` | `cl_hasWithdrawnIncentivesOnlyChange` | rule | S6-4 | NOT_STATED |
| 67 | `LEVarTran.spec` | `cl_tokenIncentivesBalancesNonIncreasing` | rule | S6-4 | NOT_STATED |
| 68 | `LEVarTran.spec` | `cl_tokenIncentivesBalanceCanBeZero` | rule | S6-4 | NOT_STATED |
| 69 | `LaunchEvent.spec` | `factoryGetPairCorrelationCurrentVals` | invariant | S6-4 | NOT_STATED |
| 70 | `LaunchEvent.spec` | `factoryGetPairCorrelationNewVals` | invariant | S6-4 | NOT_STATED |
| 71 | `LaunchEvent.spec` | `pairAndGetPairCorrelation` | invariant | S6-4 | NOT_STATED |
| 72 | `LaunchEvent.spec` | `noIssuerForNonInitialized` | invariant | S3-2 | NOT_STATED |
| 73 | `LaunchEvent.spec` | `noAllocationIfNonInitialized` | invariant | S6-4 | NOT_STATED |
| 74 | `LaunchEvent.spec` | `noBalanceIfNonInitialized` | invariant | S6-4 | NOT_STATED |
| 75 | `LaunchEvent.spec` | `notStoppedIfNonInitialized` | invariant | S3-2 | NOT_STATED |
| 76 | `LaunchEvent.spec` | `noAuctionStartIfNonInitialized` | invariant | S3-2 | NOT_STATED |
| 77 | `LaunchEvent.spec` | `al_issuer_allocation_zero` | invariant | S6-4 | NOT_STATED |
| 78 | `LaunchEvent.spec` | `al_balance_less_than_allocation` | invariant | S6-4 | NOT_STATED |
| 79 | `LaunchEvent.spec` | `al_userAllocation_less_than_maxAllocation` | invariant | S6-4 | NOT_STATED |
| 80 | `LaunchEvent.spec` | `al_differentTokenAndWavaxAddresses` | invariant | S6-4 | NOT_STATED |
| 81 | `LaunchEvent.spec` | `isInitialized` | invariant | S3-2 | NOT_STATED |
| 82 | `LaunchEvent.spec` | `initNotStopped` | invariant | S6-4 | NOT_STATED |
| 83 | `LaunchEvent.spec` | `initIssuerTimelockNonZero` | invariant | S3-2 | NOT_STATED |
| 84 | `LaunchEvent.spec` | `initUserTimelockSeven` | invariant | S3-2 | NOT_STATED |
| 85 | `LaunchEvent.spec` | `initAuctionStart` | invariant | S6-4 | NOT_STATED |
| 86 | `LaunchEvent.spec` | `initPhaseTimesSet` | invariant | S3-2 | NOT_STATED |
| 87 | `LaunchEvent.spec` | `initTimelocksCorrelation` | invariant | S3-2 | NOT_STATED |
| 88 | `LaunchEvent.spec` | `initIncentivesCorrelation` | invariant | S6-4 | NOT_STATED |
| 89 | `LaunchEvent.spec` | `initTokenBalanceCheck` | invariant | S6-4 | NOT_STATED |
| 90 | `LaunchEvent.spec` | `op_not_stopped` | invariant | S3-2 | NOT_STATED |
| 91 | `LaunchEvent.spec` | `op_user_not_withdrawn_pair` | invariant | S3-2 | NOT_STATED |
| 92 | `LaunchEvent.spec` | `op_user_not_withdrawn_incentives` | invariant | S6-4 | NOT_STATED |
| 93 | `LaunchEvent.spec` | `opWavaxBalanceAndSumBalances` | invariant | S6-4 | NOT_STATED |
| 94 | `LaunchEvent.spec` | `opWavaxBalanceAndWavaxReserve` | invariant | S6-4 | NOT_STATED |
| 95 | `LaunchEvent.spec` | `opTokenBalanceCheck` | invariant | S6-4 | NOT_STATED |
| 96 | `LaunchEvent.spec` | `op_avax_alloc_zero` | invariant | S3-2 | NOT_STATED |
| 97 | `LaunchEvent.spec` | `op_lp_supply_zero` | invariant | S6-4 | NOT_STATED |
| 98 | `LaunchEvent.spec` | `opPairBalanceIsZero` | invariant | S6-4 | NOT_STATED |
| 99 | `LaunchEvent.spec` | `opPairAndTotalSupplyCorrelation` | invariant | S6-4 | NOT_STATED |
| 100 | `LaunchEvent.spec` | `op_avax_reserve_sum_user_balances` | invariant | S6-4 | NOT_STATED |
| 101 | `LaunchEvent.spec` | `cl_not_stopped` | invariant | S3-2 | NOT_STATED |
| 102 | `LaunchEvent.spec` | `cl_avax_alloc_sum_user_balances` | invariant | S6-4 | NOT_STATED |
| 103 | `LaunchEvent.spec` | `clWavaxCorrelation` | invariant | S6-4 | NOT_STATED |
| 104 | `LaunchEvent.spec` | `cl_pair_bal_eq_lp_sum` | invariant | S6-4 | NOT_STATED |
| 105 | `LaunchEvent.spec` | `cl_token_bal_eq_res_token` | invariant | S6-4 | NOT_STATED |
| 106 | `LaunchEvent.spec` | `clIncentivesCorrelation` | invariant | S6-4 | NOT_STATED |
| 107 | `LaunchEvent.spec` | `cl_nonzero_user_pair_bal` | invariant | S6-4 | NOT_STATED |
| 108 | `LaunchEvent.spec` | `cl_bal_this_zero` | invariant | S6-4 | NOT_STATED |
| 109 | `LaunchEvent.spec` | `op_token_res_fixed` | rule | S6-4 | NOT_STATED |
| 110 | `LaunchEvent.spec` | `cl_user_alloc_unchanging` | rule | S6-4 | NOT_STATED |
| 111 | `LaunchEvent.spec` | `cl_avax_alloc_fixed` | rule | S3-2 | NOT_STATED |
| 112 | `LaunchEvent.spec` | `cl_lp_supply_fixed` | rule | S6-4 | NOT_STATED |
| 113 | `LaunchEvent.spec` | `al_userAllocationNonDecreasing` | rule | S6-4 | NOT_STATED |
| 114 | `LaunchEvent.spec` | `al_stoppedOnlyByOwner` | rule | S5-3 | NOT_STATED |
| 115 | `LaunchEvent.spec` | `op_balanceChangeByDepositOrWithdraw` | rule | S6-4 | NOT_STATED |
| 116 | `LaunchEvent.spec` | `op_allocationChangeByDeposit` | rule | S6-4 | NOT_STATED |
| 117 | `LaunchEvent.spec` | `op_tokenReserveUnchange` | rule | S6-4 | NOT_STATED |
| 118 | `LaunchEvent.spec` | `op_tokenIncentivesBalanceUnchange` | rule | S6-4 | NOT_STATED |
| 119 | `LaunchEvent.spec` | `op_tokenIncentivesForUsersUnchange` | rule | S6-4 | NOT_STATED |
| 120 | `LaunchEvent.spec` | `op_tokenIncentiveIssuerRefundUnchange` | rule | S6-4 | NOT_STATED |
| 121 | `LaunchEvent.spec` | `tr_pairOnlyChange` | rule | S3-2 | NOT_STATED |
| 122 | `LaunchEvent.spec` | `tr_initializedOnlyChange` | rule | S3-2 | NOT_STATED |
| 123 | `LaunchEvent.spec` | `tr_incentivesForUsersChanges` | rule | S6-4 | NOT_STATED |
| 124 | `LaunchEvent.spec` | `tr_incentiveIssuerRefundChanges` | rule | S6-4 | NOT_STATED |
| 125 | `LaunchEvent.spec` | `cl_unchangingPair` | rule | S3-2 | NOT_STATED |
| 126 | `LaunchEvent.spec` | `cl_hasWithdrawnPair_pairBalance_OnlyChangeUser` | rule | S6-4 | NOT_STATED |
| 127 | `LaunchEvent.spec` | `cl_hasWithdrawnPair_pairBalance_OnlyChangeIssuer` | rule | S6-4 | NOT_STATED |
| 128 | `LaunchEvent.spec` | `cl_pairAndTokenBalancesNonIncreasing` | rule | S6-4 | NOT_STATED |
| 129 | `LaunchEvent.spec` | `cl_hasWithdrawnIncentivesOnlyChange` | rule | S6-4 | NOT_STATED |
| 130 | `LaunchEvent.spec` | `cl_tokenIncentivesBalancesNonIncreasing` | rule | S6-4 | NOT_STATED |
| 131 | `LaunchEvent.spec` | `cl_tokenIncentivesBalanceCanBeZero` | rule | S6-4 | NOT_STATED |
| 132 | `LaunchEvent.spec` | `hl_EqualityOfPairs` | invariant | S6-4 | NOT_STATED |
| 133 | `LaunchEvent.spec` | `hl_EqualityOfPairAndTotalSupply` | invariant | S6-4 | NOT_STATED |
| 134 | `LaunchEvent.spec` | `hl_TotalSupplyEquality` | invariant | S6-4 | NOT_STATED |
| 135 | `LaunchEvent.spec` | `hl_EqualityOfToken` | invariant | S6-4 | NOT_STATED |
| 136 | `LaunchEvent.spec` | `hl_depositAdditivity` | rule | S6-4 | NOT_STATED |
| 137 | `LaunchEvent.spec` | `hl_withdrawAdditivity` | rule | S6-4 | NOT_STATED |
| 138 | `LaunchEvent.spec` | `hl_moreDepositMoreGet` | rule | S6-4 | NOT_STATED |
| 139 | `LaunchEvent.spec` | `hl_withdrawLateMorePenalty` | rule | S6-4 | NOT_STATED |
| 140 | `LaunchEvent.spec` | `hl_twoSideInverse` | rule | SE-1 | NOT_STATED |
| 141 | `LaunchEvent.spec` | `hl_noDepositFrontRun` | rule | S6-4 | NOT_STATED |
| 142 | `LaunchEvent.spec` | `hl_noWithdrawFrontRun` | rule | S6-4 | NOT_STATED |
| 143 | `LaunchEvent.spec` | `hl_noWithdrawLiquidityFrontRun` | rule | S6-4 | NOT_STATED |
| 144 | `LaunchEvent.spec` | `hl_createPairAtLeastOnce` | rule | S3-2 | NOT_STATED |
| 145 | `Staking.spec` | `is_initialized` | invariant | S6-4 | NOT_STATED |
| 146 | `Staking.spec` | `not_initializing` | invariant | UNMAPPED | NOT_STATED |
| 147 | `Staking.spec` | `balanceOf_Joe_eq_totalJoeStaked` | invariant | S6-4 | NOT_STATED |
| 148 | `Staking.spec` | `user_balances_less_than_totalJoeStaked` | invariant | S6-4 | VERIFIED |
| 149 | `Staking.spec` | `userInfo_amount_safe_mutate` | rule | S6-4 | VERIFIED |
| 150 | `Staking.spec` | `RJPS_only_owner_and_function` | rule | S5-3 | NOT_STATED |
| 151 | `Staking.spec` | `pending_reward_decreased_only_user` | rule | S6-4 | NOT_STATED |
| 152 | `Staking.spec` | `staking_non_trivial_rJoe` | rule | UNMAPPED | VERIFIED |
| 153 | `Staking.spec` | `staking_trivial_on_zero_time` | rule | S6-4 | VERIFIED |
| 154 | `Staking.spec` | `longer_stake_greater_return` | rule | UNMAPPED | VERIFIED |
| 155 | `Staking.spec` | `deposit_no_frontrunning` | rule | SE-1 | VERIFIED |
| 156 | `Staking.spec` | `withdraw_no_frontrunning` | rule | SE-1 | VERIFIED |
| 157 | `Staking.spec` | `additivity_withdraw` | rule | SE-1 | VERIFIED |
| 158 | `Staking.spec` | `additivity_deposit` | rule | SE-1 | VERIFIED |
| 159 | `Staking.spec` | `verify_deposit` | rule | S6-4 | VERIFIED |
| 160 | `Staking.spec` | `verify_withdraw` | rule | S6-4 | VERIFIED |
| 161 | `Staking.spec` | `verify_updateEmissionRate` | rule | UNMAPPED | VERIFIED |
| 162 | `Staking.spec` | `updatePool_contained` | rule | S6-4 | VERIFIED |
| 163 | `Staking.spec` | `verify_emergencyWithdraw` | rule | S5-2 | VERIFIED |
| 164 | `sanity.spec` | `sanity` | rule | UNMAPPED | NOT_STATED |

Each `N.md` independently gives the asserted expression, identified storage, Solidity operations, falsifying counterexample, classification, report attribution, and modeling limitations. The official validators must be run against the exact published HEAD; generation alone does not constitute validation.

## Second-pass counterexample and historical-attribution exceptions

| Example | Correction | Evidence |
|---:|---|---|
| 12, 13 | UNMAPPED / NOT_STATED | In-progress LaunchEvent existential implications permit false antecedents. |
| 147 | NOT_STATED / NOT_STATED | Source `>=` is weaker than PDF page 17 `==` despite matching name. |
| 151 | NOT_STATED / INCONCLUSIVE | PDF page 18 yellow partial indicator; emergency withdrawal excluded. |
| 152, 154 | VERIFIED (historical) / INCONCLUSIVE / UNMAPPED | Unconstrained existential witness can make implication vacuous; source 154 itself says vacuous. |

These exceptions supersede any generic language in the original generated examples. Source files remain unchanged. Future reviews must inspect further quantification and method filters before treating historical marks as security evidence.

## Historic whitespace exception, not a source rewrite

The exact Git validation on `df02d3ac36b4a4b8612e15ef4a97a251479679f2` returned exit 2 with 1,168 original whitespace diagnostics: 113 in archival CVL specs, 943 in repeated historical CVL extracted property/prelude blocks, and 112 in verbatim Solidity excerpts. All three Python validators returned exit 0 on that same remote GitHub Actions checkout (run `39159408480`; HEAD and origin/main SHA are recorded in its attached artifact). Since modifying those whitespace bytes would violate the historical-preservation requirement, per-directory `.gitattributes` entries turn off only blank-at-EOL, blank-at-EOF, and space-before-tab diagnostics **for these historical verbatim text copies**. Whitespace in new Markdown, CSV and other files remains checked by the same official `git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD` command. No CVL or Solidity source body was edited. This is an explicit path-scoped archival exception, not a global bypass.

## Additional report-formula reconciliation — source wins over names

PDF pages 13–14 show a **same-sender** hypothesis for `hl_depositAdditivity` where source example 2 requires **different senders**, and a subtraction formula for `hl_noDepositFrontRun` where source example 5 asserts **deposit addition**. Neither source assertion inherits VERIFIED on name alone. Example 3 `hl_withdrawAdditivity` does match the report's arithmetic relational formula and gains historical VERIFIED, subject to all harness assumptions. PDF page 18's displayed formula for `RJPS_only_owner_and_function` compares undefined `userBalance_pre/post` while Staking source example 150 correctly compares `RJPS_pre/post`; attribution remains NOT_STATED until original Prover logs are inspected. These are **report/source mismatches**, not changes to historical CVL.
