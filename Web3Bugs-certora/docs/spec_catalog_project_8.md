# Project 8 — Echo: AAVE Vault Spec Catalog

## Scope, methodology and counts

Read-only historical source: https://github.com/matheus-junio-da-silva/PropertyGPT/tree/main/certora_projects/aave_vault . The catalog follows `docs/spec_catalog_workflow.md` and `docs/standard.md`, not a new classification framework. The original report PDF is under `resources/8/`; its structured report document under `reports/8.md` clearly distinguishes the authoritative PDF.

- `accrueYieldCheck.spec`: 1 active CVL `rule`/`invariant` declarations.
- `changeInContractBalanceShouldCauseAccrual.spec`: 1 active CVL `rule`/`invariant` declarations.
- `erc20.spec`: 0 active CVL `rule`/`invariant` declarations.
- `erc4626.spec`: 11 active CVL `rule`/`invariant` declarations.
- `fees_LEQ_ATokenBal.spec`: 6 active CVL `rule`/`invariant` declarations.
- `lastVaultBal_LEQ_ATokenBalThis.spec`: 4 active CVL `rule`/`invariant` declarations.
- `methods_base.spec`: 0 active CVL `rule`/`invariant` declarations.
- `positiveSupply_imply_positiveAssets.spec`: 12 active CVL `rule`/`invariant` declarations.
- `rayMul_rayDiv_mulDiv_properties.spec`: 3 active CVL `rule`/`invariant` declarations.
- `totalSupply_EQ_sumAllBal.spec`: 4 active CVL `rule`/`invariant` declarations.

**Total: 42** active property instances; **0 complete**, **42 incomplete**, with a literal property body in each `.spec`, genuine Solidity excerpts in each `.sol`, a five-point audit in each `.md`, and missing-symbol evidence in each `.txt`. Exactly **42 CSV rows** reference exactly **42 bundles**. Results: {"VERIFIED":6,"VIOLATED":5,"NOT_STATED":31}. Detection outcomes: {"NO_FINDING":6,"ACCEPTED_BEHAVIOR":5,"NOT_STATED":31}. Technical Bug Labels: {"S3-2":1,"S3-1":1,"L7":0,"S6-2":8,"UNMAPPED":11,"S6-4":18,"L2":3} (UNMAPPED only for auxiliary modeled external-token invariant instances). All filenames, source ranges and exact property identities are preserved.

## Property-by-property status and trace

| Example | Original source range | Exact property | Bug Label | Formal Result | Detection Outcome |
|---:|---|---|---|---|---|
| 1 | accrueYieldCheck.spec:39-45 | `accrueYieldCheck` | S3-2 | VERIFIED | NO_FINDING |
| 2 | changeInContractBalanceShouldCauseAccrual.spec:33-53 | `changeInContractBalanceShouldCauseAccrual` | S3-1 | VERIFIED | NO_FINDING |
| 3 | erc4626.spec:73-84 | `must_not_revert` | UNMAPPED | VIOLATED | ACCEPTED_BEHAVIOR |
| 4 | erc4626.spec:94-104 | `must_not_revert_unless_large_input__convertToShares` | UNMAPPED | NOT_STATED | NOT_STATED |
| 5 | erc4626.spec:114-124 | `must_not_revert_unless_large_input__convertToAssets` | UNMAPPED | NOT_STATED | NOT_STATED |
| 6 | erc4626.spec:142-165 | `previewDeposit_amount_check` | S6-2 | VERIFIED | NO_FINDING |
| 7 | erc4626.spec:179-195 | `previewDeposit_has_NO_threshold` | S6-2 | VIOLATED | ACCEPTED_BEHAVIOR |
| 8 | erc4626.spec:211-233 | `previewMint_amount_check` | S6-2 | VERIFIED | NO_FINDING |
| 9 | erc4626.spec:248-264 | `previewMint_has_NO_threshold` | S6-2 | VIOLATED | ACCEPTED_BEHAVIOR |
| 10 | erc4626.spec:282-302 | `previewWithdraw_amount_check` | S6-2 | VERIFIED | NO_FINDING |
| 11 | erc4626.spec:317-333 | `previewWithdraw_has_NO_threshold` | S6-2 | VIOLATED | ACCEPTED_BEHAVIOR |
| 12 | erc4626.spec:354-379 | `previewRedeem_amount_check` | S6-2 | VERIFIED | NO_FINDING |
| 13 | erc4626.spec:394-410 | `previewRedeem_has_NO_threshold` | S6-2 | VIOLATED | ACCEPTED_BEHAVIOR |
| 14 | fees_LEQ_ATokenBal.spec:56-57 | `inv_sumAllBalance_eq_totalSupply__underline` | UNMAPPED | NOT_STATED | NOT_STATED |
| 15 | fees_LEQ_ATokenBal.spec:59-60 | `inv_sumAllBalance_eq_totalSupply__atoken` | UNMAPPED | NOT_STATED | NOT_STATED |
| 16 | fees_LEQ_ATokenBal.spec:62-63 | `inv_sumAllBalance_eq_totalSupply` | S6-4 | NOT_STATED | NOT_STATED |
| 17 | fees_LEQ_ATokenBal.spec:69-70 | `lastVaultBalance_OK` | S6-4 | NOT_STATED | NOT_STATED |
| 18 | fees_LEQ_ATokenBal.spec:150-159 | `getCLMFees_LEQ_ATokenBAL_DM_other` | S6-4 | NOT_STATED | NOT_STATED |
| 19 | fees_LEQ_ATokenBal.spec:201-210 | `getCLMFees_LEQ_ATokenBAL_RW` | S6-4 | NOT_STATED | NOT_STATED |
| 20 | lastVaultBal_LEQ_ATokenBalThis.spec:40-41 | `inv_sumAllBalance_eq_totalSupply__underline` | UNMAPPED | NOT_STATED | NOT_STATED |
| 21 | lastVaultBal_LEQ_ATokenBalThis.spec:43-44 | `inv_sumAllBalance_eq_totalSupply__atoken` | UNMAPPED | NOT_STATED | NOT_STATED |
| 22 | lastVaultBal_LEQ_ATokenBalThis.spec:46-47 | `inv_sumAllBalance_eq_totalSupply` | S6-4 | NOT_STATED | NOT_STATED |
| 23 | lastVaultBal_LEQ_ATokenBalThis.spec:63-132 | `lastVaultBalance_LEQ_ATokenBalThis` | S6-4 | NOT_STATED | NOT_STATED |
| 24 | positiveSupply_imply_positiveAssets.spec:59-60 | `inv_sumAllBalance_eq_totalSupply__underline` | UNMAPPED | NOT_STATED | NOT_STATED |
| 25 | positiveSupply_imply_positiveAssets.spec:62-63 | `inv_sumAllBalance_eq_totalSupply__atoken` | UNMAPPED | NOT_STATED | NOT_STATED |
| 26 | positiveSupply_imply_positiveAssets.spec:65-66 | `inv_sumAllBalance_eq_totalSupply` | S6-4 | NOT_STATED | NOT_STATED |
| 27 | positiveSupply_imply_positiveAssets.spec:74-75 | `lastVaultBalance_OK` | S6-4 | NOT_STATED | NOT_STATED |
| 28 | positiveSupply_imply_positiveAssets.spec:82-85 | `inv_fee_LEQ_ATokenBal` | S6-4 | NOT_STATED | NOT_STATED |
| 29 | positiveSupply_imply_positiveAssets.spec:146-150 | `positiveSupply_imply_positiveAssets_all_deposit` | S6-4 | NOT_STATED | NOT_STATED |
| 30 | positiveSupply_imply_positiveAssets.spec:152-156 | `positiveSupply_imply_positiveAssets_all_mint` | S6-4 | NOT_STATED | NOT_STATED |
| 31 | positiveSupply_imply_positiveAssets.spec:159-170 | `positiveSupply_imply_positiveAssets_other` | S6-4 | NOT_STATED | NOT_STATED |
| 32 | positiveSupply_imply_positiveAssets.spec:173-176 | `positiveSupply_imply_positiveAssets_specific_DM` | S6-4 | NOT_STATED | NOT_STATED |
| 33 | positiveSupply_imply_positiveAssets.spec:223-227 | `positiveSupply_imply_positiveAssets_all_withdraw` | S6-4 | NOT_STATED | NOT_STATED |
| 34 | positiveSupply_imply_positiveAssets.spec:229-233 | `positiveSupply_imply_positiveAssets_all_redeem` | S6-4 | NOT_STATED | NOT_STATED |
| 35 | positiveSupply_imply_positiveAssets.spec:236-239 | `positiveSupply_imply_positiveAssets_specific_RW` | S6-4 | NOT_STATED | NOT_STATED |
| 36 | rayMul_rayDiv_mulDiv_properties.spec:19-30 | `rayMul_prop_1` | L2 | NOT_STATED | NOT_STATED |
| 37 | rayMul_rayDiv_mulDiv_properties.spec:33-44 | `rayMul_prop_2` | L2 | NOT_STATED | NOT_STATED |
| 38 | rayMul_rayDiv_mulDiv_properties.spec:46-61 | `mulDiv_properties` | L2 | NOT_STATED | NOT_STATED |
| 39 | totalSupply_EQ_sumAllBal.spec:29-31 | `inv_sumAllBalance_eq_totalSupply` | S6-4 | NOT_STATED | NOT_STATED |
| 40 | totalSupply_EQ_sumAllBal.spec:33-39 | `inv_balanceOf_leq_totalSupply` | S6-4 | NOT_STATED | NOT_STATED |
| 41 | totalSupply_EQ_sumAllBal.spec:52-56 | `inv_sumAllBalance_eq_totalSupply__underline` | UNMAPPED | NOT_STATED | NOT_STATED |
| 42 | totalSupply_EQ_sumAllBal.spec:69-73 | `inv_sumAllBalance_eq_totalSupply__atoken` | UNMAPPED | NOT_STATED | NOT_STATED |

## Dependency closure and missing-artifact search

All ten specs were examined, including pure helper files `erc20.spec` and `methods_base.spec` (zero properties each). Recursively relevant shared definitions, helper functions, methods, imports, `using`, ghosts and hooks are included in extracted specs with original headers. No source rule or invariant assertion was modernized. The Solidity source set consists of six supplied files: `ATokenVault.sol`, `ATokenVaultStorage.sol`, `ATokenVaultV2.sol`, `interfaces/IATokenVault.sol`, `libraries/Constants.sol`, `libraries/MetaTxHelpers.sol`.

Missing implementation artifacts are now accounted for by **each rule's effective closure in its N.txt** (not by this old generic superset); external Aave/OZ dependencies, selected symbolic token models, public getters, probes, or handle wrappers are only required when used by the corresponding instance.

## Result versus finding interpretation and report limitations

Exact report names #1–9, #16 and #17 support the corresponding individual outcomes, including four threshold checks and must_not_revert **VIOLATED / ACCEPTED_BEHAVIOR** rather than security findings. The report gives different aggregate name for #10 converter nonrevert rule, and #11–15 aggregate results cannot support status claims for every duplicated or specialized source rule. Those are `NOT_STATED` at source-instance granularity, even where source comments say pass or fail. Actual older-revision security findings (deposit rounding DoS, withdrawal griefing, protocol fee insolvency, arithmetic DoS, preview misinformation, fee rounding, inappropriate supply cap, same-block gift) are recorded in `results/bugs.csv` as eight separately report-supported rows. A report finding's technical/root label is not confused with the checked property's own Bug Label.

Report notation tick, tick-star, cross and timeout is described in `reports/8.md`, but never invented for unreported instances. Key limitations: bounded loop unrolling excludes >1-iteration counterexamples, signature cryptography is unverified, symbolic supply limits are common, and further idealized arithmetic identities/index bounds are assumed for fee/solvency proofs. No branch-local run config proves whether a given source instance ran against ATokenVault or ATokenVaultV2; mathematical probes have UNSPECIFIED target. The report's latest reviewed commit `23366cc` and earlier fix commits do not prove that PropertyGPT's source snapshot matches each historical version. The extracted CVL code is not migrated or corrected.

## Independent semantic second pass (all 42)

Each row audits **(a)** what state/call falsifies the literal assertion, **(b)** whether the technical label fits that condition, **(c)** normative versus auxiliary, **(d)** report attribution unsupported by this rule, and **(e)** separation of property, finding, result and target. Each individual `N.md` supplies a longer source-to-Solidity relationship.

| ID | (a) Falsifying counterexample | (b) Label rationale | (c) Normative/auxiliary | (d) Unsupported inference avoided | (e) Property/target guard |
|---:|---|---|---|---|---|
| 1 | Accrual lowers getAccumulatedFees() compared with the prior state. | S3-2 — Detect incorrect accumulated-fee state decrement during accrual. | normative | The report explicitly names this property in additional verification checks #16/#17 and marks it verified. | accrueYieldCheck.spec:39-45; historical V2 target linkage not supplied |
| 2 | A nonexempt method changes token balances but does not set accrueYieldCalled ghost. | S3-1 — Detect missing yield accrual when Vault token balances change. | normative | The report explicitly names this property in additional verification checks #16/#17 and marks it verified. | changeInContractBalanceShouldCauseAccrual.spec:33-53; historical V2 target linkage not supplied |
| 3 | A specified ERC4626 query reverts despite msg.value=0. | UNMAPPED — Generic unexpected-revert predicate, not exclusively integer overflow/underflow. | normative | The report names the aggregate must_not_revert check (#9) as violated and treats the arithmetic-dependent reverts as acceptable. | erc4626.spec:73-84; historical V2 target linkage not supplied |
| 4 | Bounded convertToShares or convertToAssets reverts. | UNMAPPED — Generic unexpected-revert predicate, not exclusively integer overflow/underflow. | normative | The report's #10 is an aggregate named must_not_revert_unless_large_input, not either separate converter-specific source rule. | erc4626.spec:94-104; historical V2 target linkage not supplied |
| 5 | Bounded convertToShares or convertToAssets reverts. | UNMAPPED — Generic unexpected-revert predicate, not exclusively integer overflow/underflow. | normative | The report's #10 is an aggregate named must_not_revert_unless_large_input, not either separate converter-specific source rule. | erc4626.spec:114-124; historical V2 target linkage not supplied |
| 6 | previewDeposit disagrees with actual deposit by more than the exact assertion's tolerance. | S6-2 — Detect ERC4626 previewDeposit returning a value inconsistent with the matching operation. | normative | The report explicitly names this amount-check property (#1/#3/#5/#7) and marks it verified. | erc4626.spec:142-165; historical V2 target linkage not supplied |
| 7 | Two states with the same totalSupply, totalAssets and argument return different previewDeposit amounts after havoc. | S6-2 — Detect previewDeposit dependent on caps or limits not captured by supply/assets. | normative | The report names this exact preview independence test (#2/#4/#6/#8) as violated and accepts Aave-specific caps/liquidity dependence. | erc4626.spec:179-195; historical V2 target linkage not supplied |
| 8 | previewMint disagrees with actual mint by more than the exact assertion's tolerance. | S6-2 — Detect ERC4626 previewMint returning a value inconsistent with the matching operation. | normative | The report explicitly names this amount-check property (#1/#3/#5/#7) and marks it verified. | erc4626.spec:211-233; historical V2 target linkage not supplied |
| 9 | Two states with the same totalSupply, totalAssets and argument return different previewMint amounts after havoc. | S6-2 — Detect previewMint dependent on caps or limits not captured by supply/assets. | normative | The report names this exact preview independence test (#2/#4/#6/#8) as violated and accepts Aave-specific caps/liquidity dependence. | erc4626.spec:248-264; historical V2 target linkage not supplied |
| 10 | previewWithdraw disagrees with actual withdraw by more than the exact assertion's tolerance. | S6-2 — Detect ERC4626 previewWithdraw returning a value inconsistent with the matching operation. | normative | The report explicitly names this amount-check property (#1/#3/#5/#7) and marks it verified. | erc4626.spec:282-302; historical V2 target linkage not supplied |
| 11 | Two states with the same totalSupply, totalAssets and argument return different previewWithdraw amounts after havoc. | S6-2 — Detect previewWithdraw dependent on caps or limits not captured by supply/assets. | normative | The report names this exact preview independence test (#2/#4/#6/#8) as violated and accepts Aave-specific caps/liquidity dependence. | erc4626.spec:317-333; historical V2 target linkage not supplied |
| 12 | previewRedeem disagrees with actual redeem by more than the exact assertion's tolerance. | S6-2 — Detect ERC4626 previewRedeem returning a value inconsistent with the matching operation. | normative | The report explicitly names this amount-check property (#1/#3/#5/#7) and marks it verified. | erc4626.spec:354-379; historical V2 target linkage not supplied |
| 13 | Two states with the same totalSupply, totalAssets and argument return different previewRedeem amounts after havoc. | S6-2 — Detect previewRedeem dependent on caps or limits not captured by supply/assets. | normative | The report names this exact preview independence test (#2/#4/#6/#8) as violated and accepts Aave-specific caps/liquidity dependence. | erc4626.spec:394-410; historical V2 target linkage not supplied |
| 14 | The ghost sum of Underlying token balances differs from Underlying.totalSupply(). | UNMAPPED — Auxiliary underlying token supply-model conservation, not a stand-alone vault vulnerability requirement. | auxiliary | The report does not assign an individual result to this exact CVL source instance. | fees_LEQ_ATokenBal.spec:56-57; historical V2 target linkage not supplied |
| 15 | The aToken ghost sum of scaled balances differs from aToken scaledTotalSupply(). | UNMAPPED — Auxiliary scaled-aToken supply model, not a stand-alone vault vulnerability requirement. | auxiliary | The report does not assign an individual result to this exact CVL source instance. | fees_LEQ_ATokenBal.spec:59-60; historical V2 target linkage not supplied |
| 16 | Vault ghost sum of all account balances differs from vault totalSupply(). | S6-4 — Detect Vault share supply inconsistent with balances. | normative | Report #11/#12 verifies corresponding aggregate concepts; this exact duplicate/source target is not individually identified. | fees_LEQ_ATokenBal.spec:62-63; historical V2 target linkage not supplied |
| 17 | Recorded lastVaultBalance exceeds current vault aToken reserve balance. | S6-4 — Detect incorrect accounting reserve baseline exceeding true reserve holdings. | normative | Report #13 is verified on latest revision and violated on earlier versions, but no individual result for this source instance is stated. | fees_LEQ_ATokenBal.spec:69-70; historical V2 target linkage not supplied |
| 18 | Claimable plus unaccrued protocol fees exceed Vault aToken reserves after modeled method. | S6-4 — Detect fee liabilities exceeding held reserve assets. | normative | Report #14 getClaimableFees_LEQ_ATokenBalance is aggregate and previously violated; no exact status is given for the source fee invariant/DM/RW helper variants. | fees_LEQ_ATokenBal.spec:150-159; historical V2 target linkage not supplied |
| 19 | Claimable plus unaccrued protocol fees exceed Vault aToken reserves after modeled method. | S6-4 — Detect fee liabilities exceeding held reserve assets. | normative | Report #14 getClaimableFees_LEQ_ATokenBalance is aggregate and previously violated; no exact status is given for the source fee invariant/DM/RW helper variants. | fees_LEQ_ATokenBal.spec:201-210; historical V2 target linkage not supplied |
| 20 | The ghost sum of Underlying token balances differs from Underlying.totalSupply(). | UNMAPPED — Auxiliary underlying token supply-model conservation, not a stand-alone vault vulnerability requirement. | auxiliary | The report does not assign an individual result to this exact CVL source instance. | lastVaultBal_LEQ_ATokenBalThis.spec:40-41; historical V2 target linkage not supplied |
| 21 | The aToken ghost sum of scaled balances differs from aToken scaledTotalSupply(). | UNMAPPED — Auxiliary scaled-aToken supply model, not a stand-alone vault vulnerability requirement. | auxiliary | The report does not assign an individual result to this exact CVL source instance. | lastVaultBal_LEQ_ATokenBalThis.spec:43-44; historical V2 target linkage not supplied |
| 22 | Vault ghost sum of all account balances differs from vault totalSupply(). | S6-4 — Detect Vault share supply inconsistent with balances. | normative | Report #11/#12 verifies corresponding aggregate concepts; this exact duplicate/source target is not individually identified. | lastVaultBal_LEQ_ATokenBalThis.spec:46-47; historical V2 target linkage not supplied |
| 23 | Recorded lastVaultBalance exceeds current vault aToken reserve balance. | S6-4 — Detect incorrect accounting reserve baseline exceeding true reserve holdings. | normative | Report #13 is verified on latest revision and violated on earlier versions, but no individual result for this source instance is stated. | lastVaultBal_LEQ_ATokenBalThis.spec:63-132; historical V2 target linkage not supplied |
| 24 | The ghost sum of Underlying token balances differs from Underlying.totalSupply(). | UNMAPPED — Auxiliary underlying token supply-model conservation, not a stand-alone vault vulnerability requirement. | auxiliary | The report does not assign an individual result to this exact CVL source instance. | positiveSupply_imply_positiveAssets.spec:59-60; historical V2 target linkage not supplied |
| 25 | The aToken ghost sum of scaled balances differs from aToken scaledTotalSupply(). | UNMAPPED — Auxiliary scaled-aToken supply model, not a stand-alone vault vulnerability requirement. | auxiliary | The report does not assign an individual result to this exact CVL source instance. | positiveSupply_imply_positiveAssets.spec:62-63; historical V2 target linkage not supplied |
| 26 | Vault ghost sum of all account balances differs from vault totalSupply(). | S6-4 — Detect Vault share supply inconsistent with balances. | normative | Report #11/#12 verifies corresponding aggregate concepts; this exact duplicate/source target is not individually identified. | positiveSupply_imply_positiveAssets.spec:65-66; historical V2 target linkage not supplied |
| 27 | Recorded lastVaultBalance exceeds current vault aToken reserve balance. | S6-4 — Detect incorrect accounting reserve baseline exceeding true reserve holdings. | normative | Report #13 is verified on latest revision and violated on earlier versions, but no individual result for this source instance is stated. | positiveSupply_imply_positiveAssets.spec:74-75; historical V2 target linkage not supplied |
| 28 | Claimable plus unaccrued protocol fees exceed Vault aToken reserves after modeled method. | S6-4 — Detect fee liabilities exceeding held reserve assets. | normative | Report #14 getClaimableFees_LEQ_ATokenBalance is aggregate and previously violated; no exact status is given for the source fee invariant/DM/RW helper variants. | positiveSupply_imply_positiveAssets.spec:82-85; historical V2 target linkage not supplied |
| 29 | After an allowed method totalSupply() is positive yet totalAssets() is zero. | S6-4 — Detect positive share supply remaining with no underlying asset backing. | normative | Report #15 is verified on the latest version and violated earlier, but does not differentiate these many source rule variants. | positiveSupply_imply_positiveAssets.spec:146-150; historical V2 target linkage not supplied |
| 30 | After an allowed method totalSupply() is positive yet totalAssets() is zero. | S6-4 — Detect positive share supply remaining with no underlying asset backing. | normative | Report #15 is verified on the latest version and violated earlier, but does not differentiate these many source rule variants. | positiveSupply_imply_positiveAssets.spec:152-156; historical V2 target linkage not supplied |
| 31 | After an allowed method totalSupply() is positive yet totalAssets() is zero. | S6-4 — Detect positive share supply remaining with no underlying asset backing. | normative | Report #15 is verified on the latest version and violated earlier, but does not differentiate these many source rule variants. | positiveSupply_imply_positiveAssets.spec:159-170; historical V2 target linkage not supplied |
| 32 | After an allowed method totalSupply() is positive yet totalAssets() is zero. | S6-4 — Detect positive share supply remaining with no underlying asset backing. | normative | Report #15 is verified on the latest version and violated earlier, but does not differentiate these many source rule variants. | positiveSupply_imply_positiveAssets.spec:173-176; historical V2 target linkage not supplied |
| 33 | After an allowed method totalSupply() is positive yet totalAssets() is zero. | S6-4 — Detect positive share supply remaining with no underlying asset backing. | normative | Report #15 is verified on the latest version and violated earlier, but does not differentiate these many source rule variants. | positiveSupply_imply_positiveAssets.spec:223-227; historical V2 target linkage not supplied |
| 34 | After an allowed method totalSupply() is positive yet totalAssets() is zero. | S6-4 — Detect positive share supply remaining with no underlying asset backing. | normative | Report #15 is verified on the latest version and violated earlier, but does not differentiate these many source rule variants. | positiveSupply_imply_positiveAssets.spec:229-233; historical V2 target linkage not supplied |
| 35 | After an allowed method totalSupply() is positive yet totalAssets() is zero. | S6-4 — Detect positive share supply remaining with no underlying asset backing. | normative | Report #15 is verified on the latest version and violated earlier, but does not differentiate these many source rule variants. | positiveSupply_imply_positiveAssets.spec:236-239; historical V2 target linkage not supplied |
| 36 | Two purported ray multiplication/division identities deviate by more than one rounding unit. | L2 — Detect excessive ray arithmetic rounding differences. | normative | The report does not assign an individual result to this exact CVL source instance. | rayMul_rayDiv_mulDiv_properties.spec:19-30; historical V2 target linkage not supplied |
| 37 | Two purported ray multiplication/division identities deviate by more than one rounding unit. | L2 — Detect excessive ray arithmetic rounding differences. | normative | The report does not assign an individual result to this exact CVL source instance. | rayMul_rayDiv_mulDiv_properties.spec:33-44; historical V2 target linkage not supplied |
| 38 | With assets equal to totA, mulDiv__ differs from totS. | L2 — Detect full-ratio mulDiv rounding or precision error. | normative | The report does not assign an individual result to this exact CVL source instance. | rayMul_rayDiv_mulDiv_properties.spec:46-61; historical V2 target linkage not supplied |
| 39 | Vault ghost sum of all account balances differs from vault totalSupply(). | S6-4 — Detect Vault share supply inconsistent with balances. | normative | Report #11/#12 verifies corresponding aggregate concepts; this exact duplicate/source target is not individually identified. | totalSupply_EQ_sumAllBal.spec:29-31; historical V2 target linkage not supplied |
| 40 | A user's vault balanceOf exceeds totalSupply, despite the proof premise. | S6-4 — Detect Vault individual shares exceeding issued share supply. | normative | Report #11/#12 verifies corresponding aggregate concepts; this exact duplicate/source target is not individually identified. | totalSupply_EQ_sumAllBal.spec:33-39; historical V2 target linkage not supplied |
| 41 | The ghost sum of Underlying token balances differs from Underlying.totalSupply(). | UNMAPPED — Auxiliary underlying token supply-model conservation, not a stand-alone vault vulnerability requirement. | auxiliary | The report does not assign an individual result to this exact CVL source instance. | totalSupply_EQ_sumAllBal.spec:52-56; historical V2 target linkage not supplied |
| 42 | The aToken ghost sum of scaled balances differs from aToken scaledTotalSupply(). | UNMAPPED — Auxiliary scaled-aToken supply model, not a stand-alone vault vulnerability requirement. | auxiliary | The report does not assign an individual result to this exact CVL source instance. | totalSupply_EQ_sumAllBal.spec:69-73; historical V2 target linkage not supplied |

## Integrity and provenance

All 16 original plaintext source files retain their bytes and subdirectory names under `contracts/8/`. Their exact **Git blob SHA-1 identifiers** are:

- `specs/accrueYieldCheck.spec` — `ebc52fd02af7d2aabaf75c3ce76b8307e395942a`
- `specs/changeInContractBalanceShouldCauseAccrual.spec` — `4759b26fa5b399b7dc63499a3df81ccb69680c1b`
- `specs/erc20.spec` — `e03d6e69c54507dfa36af723676ebb342b58fbb8`
- `specs/erc4626.spec` — `97cc50b92a8d8965d3eb26d9654e718f4f39cbc3`
- `specs/fees_LEQ_ATokenBal.spec` — `73a04224bdbf592d557ab9ff098be11c2aeeeeaa`
- `specs/lastVaultBal_LEQ_ATokenBalThis.spec` — `66a05c835013dfcf88703557ef4622bbb6856f0a`
- `specs/methods_base.spec` — `ca3894aa68f4e788c37ea9e0825dee93f31daab0`
- `specs/positiveSupply_imply_positiveAssets.spec` — `5cb4c8428100f1d75b42aa65ec428ea19190f1f9`
- `specs/rayMul_rayDiv_mulDiv_properties.spec` — `d8115c6cd2217faee1db2f92a808a03f4b36218f`
- `specs/totalSupply_EQ_sumAllBal.spec` — `1dd8aec531854631f8eaa3df749cae32647801fd`
- `src/ATokenVault.sol` — `40e9b2d7817ee696383a76d68786d845dc08a8ca`
- `src/ATokenVaultStorage.sol` — `350c4f7b66cafc493b6863693ae954c8b3b05c00`
- `src/ATokenVaultV2.sol` — `6bce0c03980584e029a7537aada985e63e8bf7cd`
- `src/interfaces/IATokenVault.sol` — `a60132f35190b226b40210b9fb35260ac4c9cd9a`
- `src/libraries/Constants.sol` — `73b23171d8bc611e2b70c7fd50da811f18cf5255`
- `src/libraries/MetaTxHelpers.sol` — `40bb1badd48d5070b87157e454c345564b0042bb`

The original 800982-byte report PDF has Git blob SHA-1 `f750a5be51c8ea48c1a1efb0a2d8047d72e897de` and is included byte-identically in two locations (the source snapshot and report resources). These are Git-object identities, not per-file SHA-256 checksums; no other source tree was edited.

## Executed validations and blockers

- **Executed in creation preflight:** active-property parser found 42; generated 42 paired example IDs and 42 index rows; verified 17-column index header, preservation of source property blocks and no duplicate paths.
- `python scripts/check_specs.py .` — **NOT EXECUTED**, because a terminal with an authenticated clone of the destination is unavailable.
- `python scripts/check_contests_csv.py .` — **NOT EXECUTED**, same blocker.
- `python scripts/check_contracts.py .` — **NOT EXECUTED**, same blocker.
- `git diff --check` — **NOT EXECUTED** in a checkout; original CRLF CSV conventions were retained where present, but PASS is not claimed.

Before merging, the independent reviewer must run these checks from the **inner** `Web3Bugs-certora/` root, compare original Git blobs to the snapshot, and review each conservative dependency/semantic decision. These checks do not compile CVL or reproduce Certora Prover results.

## Echo — mandatory second-pass repair log (2026-10-16)

**Same PR, same Project 8; no PropertyGPT edits and no merge.** The original Solidity/spec source in `contracts/8/` and both PDF copies remain byte-identical. GitHub commits: `86f7a774` (all 42 extraction/missing lists), `e9d20e7f` (recursive definitions and storage ghost hooks), `9402a078` (all 42 individual MD audits, provenance and labels). Later documentation commits only correct Project 8 files.

**Resolved:** dangling duplicate imports to `methods_base.spec` and `erc20.spec` were removed from extracted copies, replacing them with selectively included original definitions and method declarations. The native original `contracts/8/specs/*.spec` files remain unchanged. This extracted closure is a catalog unit, not claimed historically identical prover configuration. The explicit audit `N.txt` now lists only rule-relevant missing external implementations, rather than a project-wide superset; the symbolic probe example 36 needs only `rayMul__`/`rayDiv__` implementations (and retains the original imported `RAY()` definition).

**Axiomatic soundness blocker:** universally quantified `rayMul_g` axioms in `fees_LEQ_ATokenBal.spec:26-33`, `lastVaultBal_LEQ_ATokenBalThis.spec:20-27`, and `positiveSupply_imply_positiveAssets.spec:29-36` have direct inconsistent witness `x=1,y=0`; `accrueYieldCheck.spec:17-18` has witness `x=y=denominator=0, rounding=0`. Potential vacuous proofs are documented in the corresponding `N.md` for all 23 instances whose originating spec contains these contradictions (1 and 14–35). Certora sanity execution was **not** reproducible from the supplied mock/config environment and no historical outcome was changed based on this independent observation.

**Outcome and classification:** all 42 examples remain `incomplete` because each has one or more identified missing concrete implementation dependencies, not merely an absent CLI config or old CVL syntax. Exactly six unique source properties retain report-supported `VERIFIED/NO_FINDING`; five retain `VIOLATED/ACCEPTED_BEHAVIOR`; 31 remain `NOT_STATED/NOT_STATED`. Generic ERC-4626 nonrevert checks (3–5) were relabeled `UNMAPPED`: this broad oracle does not exclusively detect L7 overflow/underflow, even if those were observed in a report counterexample. The separate reported bug VAULT-07 was relabeled SC (incorrect reuse of new-asset cap for already-issued assets) and VAULT-08 S3-1 (missing same-block accrual state update). These finding classifications are **not** the labels of every property.

**Provenance:** the index now records explicit filename-qualified CVL dependency source line intervals per example, with removed import lines excluded. The 42 individual `.md` records contain the same intervals; `N.spec` headers correspond to the original text. A complete source-to-excerpt comparison checked **203/203 Solidity line intervals** across the 42 `N.sol` files versus the six preserved source files (164 ATokenVault.sol, 39 ATokenVaultStorage.sol), with zero mismatches; this is an independent textual check, not a Solidity compiler pass.

**Report reconciliation:** `reports/8.md` now carries page-indexed issue table, numerical examples, all 17 report formal properties and six numbered footnote assumptions, while the unchanged PDF remains the exact original. Differences documented: report #3 previewMint mentions shares/deposit whereas original `erc4626.spec` compares assets/mint; report #7 allows ±1 for previewRedeem whereas CVL permits one direction; historical lastUpdated accrual exists in earlier revisions, not the preserved ATokenVaultStorage deprecated gap; do not propagate report #11–15 aggregate statuses to duplicated/spec-specific source variants.

**Validator status / real tool attempts:** `python scripts/check_specs.py .`, `python scripts/check_contests_csv.py .`, `python scripts/check_contracts.py .`, `git diff --check`, and Certora Prover sanity are **NOT RUN** on the complete working tree. The container command `git ls-remote https://github.com/matheus-junio-da-silva/Web3Bugs.git HEAD` returned `fatal: ... Could not resolve host: github.com`; the authorized Desktop Commander device `DESKTOP-5E26TVU` reported **Offline** (last seen ~311h). GitHub connector supplies remote file reads/writes but no shell execution. The structural source/CSV and Solidity textual scans in this document are auxiliary checks only, **not** PASS results of repository Python validators. CI/status checks must be executed on an accessible complete clone before merge.

### Final status ledger — individually identified non-builtin missing dependencies

| Example | Source property | Missing actual external dependency | Original-spec axiom risk | Category |
|---:|---|---|---|---|
| 1 | `accrueYieldCheck` | `accrueYield()`; `getAccumulatedFees()` | mulDiv (zero denominator) | incomplete / S3-2 |
| 2 | `changeInContractBalanceShouldCauseAccrual` | `_AToken.balanceOf()`; `Underlying.balanceOf()`; `_accrueYield() ghost instrumentation` | none identified | incomplete / S3-1 |
| 3 | `must_not_revert` | `ERC4626Upgradeable / ERC20Upgradeable`; `Aave pool / AToken` | none identified | incomplete / UNMAPPED |
| 4 | `must_not_revert_unless_large_input__convertToShares` | `ERC4626Upgradeable / ERC20Upgradeable`; `Aave pool / AToken` | none identified | incomplete / UNMAPPED |
| 5 | `must_not_revert_unless_large_input__convertToAssets` | `ERC4626Upgradeable / ERC20Upgradeable`; `Aave pool / AToken` | none identified | incomplete / UNMAPPED |
| 6 | `previewDeposit_amount_check` | `ERC4626Upgradeable / ERC20Upgradeable`; `Aave pool / AToken` | none identified | incomplete / S6-2 |
| 7 | `previewDeposit_has_NO_threshold` | `ERC4626Upgradeable / ERC20Upgradeable`; `Aave pool / AToken`; `havoc_all()` | none identified | incomplete / S6-2 |
| 8 | `previewMint_amount_check` | `ERC4626Upgradeable / ERC20Upgradeable`; `Aave pool / AToken` | none identified | incomplete / S6-2 |
| 9 | `previewMint_has_NO_threshold` | `ERC4626Upgradeable / ERC20Upgradeable`; `Aave pool / AToken`; `havoc_all()` | none identified | incomplete / S6-2 |
| 10 | `previewWithdraw_amount_check` | `ERC4626Upgradeable / ERC20Upgradeable`; `Aave pool / AToken` | none identified | incomplete / S6-2 |
| 11 | `previewWithdraw_has_NO_threshold` | `ERC4626Upgradeable / ERC20Upgradeable`; `Aave pool / AToken`; `havoc_all()` | none identified | incomplete / S6-2 |
| 12 | `previewRedeem_amount_check` | `ERC4626Upgradeable / ERC20Upgradeable`; `Aave pool / AToken` | none identified | incomplete / S6-2 |
| 13 | `previewRedeem_has_NO_threshold` | `ERC4626Upgradeable / ERC20Upgradeable`; `Aave pool / AToken`; `havoc_all()` | none identified | incomplete / S6-2 |
| 14 | `inv_sumAllBalance_eq_totalSupply__underline` | `Underlying.totalSupply()/Underlying.b` | rayMul (x=1,y=0) | incomplete / UNMAPPED |
| 15 | `inv_sumAllBalance_eq_totalSupply__atoken` | `_AToken.scaledTotalSupply()/_userState` | rayMul (x=1,y=0) | incomplete / UNMAPPED |
| 16 | `inv_sumAllBalance_eq_totalSupply` | `_balances / ERC20Upgradeable` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 17 | `lastVaultBalance_OK` | `_AToken.balanceOf()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 18 | `getCLMFees_LEQ_ATokenBAL_DM_other` | `getAccumulatedFees()`; `_AToken.balanceOf()`; `SymbolicLendingPoolL1.getLiquidityIndex()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 19 | `getCLMFees_LEQ_ATokenBAL_RW` | `getAccumulatedFees()`; `_AToken.balanceOf()`; `SymbolicLendingPoolL1.getLiquidityIndex()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 20 | `inv_sumAllBalance_eq_totalSupply__underline` | `Underlying.totalSupply()/Underlying.b` | rayMul (x=1,y=0) | incomplete / UNMAPPED |
| 21 | `inv_sumAllBalance_eq_totalSupply__atoken` | `_AToken.scaledTotalSupply()/_userState` | rayMul (x=1,y=0) | incomplete / UNMAPPED |
| 22 | `inv_sumAllBalance_eq_totalSupply` | `_balances / ERC20Upgradeable` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 23 | `lastVaultBalance_LEQ_ATokenBalThis` | `_AToken.balanceOf()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 24 | `inv_sumAllBalance_eq_totalSupply__underline` | `Underlying.totalSupply()/Underlying.b` | rayMul (x=1,y=0) | incomplete / UNMAPPED |
| 25 | `inv_sumAllBalance_eq_totalSupply__atoken` | `_AToken.scaledTotalSupply()/_userState` | rayMul (x=1,y=0) | incomplete / UNMAPPED |
| 26 | `inv_sumAllBalance_eq_totalSupply` | `_balances / ERC20Upgradeable` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 27 | `lastVaultBalance_OK` | `_AToken.balanceOf()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 28 | `inv_fee_LEQ_ATokenBal` | `getAccumulatedFees()`; `_AToken.balanceOf()`; `SymbolicLendingPoolL1.getLiquidityIndex()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 29 | `positiveSupply_imply_positiveAssets_all_deposit` | `ATokenVaultHarness handle*() wrappers`; `_AToken / Underlying`; `getAccumulatedFees()`; `SymbolicLendingPoolL1.getLiquidityIndex()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 30 | `positiveSupply_imply_positiveAssets_all_mint` | `ATokenVaultHarness handle*() wrappers`; `_AToken / Underlying`; `getAccumulatedFees()`; `SymbolicLendingPoolL1.getLiquidityIndex()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 31 | `positiveSupply_imply_positiveAssets_other` | `ATokenVaultHarness handle*() wrappers`; `_AToken / Underlying`; `getAccumulatedFees()`; `SymbolicLendingPoolL1.getLiquidityIndex()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 32 | `positiveSupply_imply_positiveAssets_specific_DM` | `ATokenVaultHarness handle*() wrappers`; `_AToken / Underlying`; `getAccumulatedFees()`; `SymbolicLendingPoolL1.getLiquidityIndex()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 33 | `positiveSupply_imply_positiveAssets_all_withdraw` | `ATokenVaultHarness handle*() wrappers`; `_AToken / Underlying`; `getAccumulatedFees()`; `SymbolicLendingPoolL1.getLiquidityIndex()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 34 | `positiveSupply_imply_positiveAssets_all_redeem` | `ATokenVaultHarness handle*() wrappers`; `_AToken / Underlying`; `getAccumulatedFees()`; `SymbolicLendingPoolL1.getLiquidityIndex()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 35 | `positiveSupply_imply_positiveAssets_specific_RW` | `ATokenVaultHarness handle*() wrappers`; `_AToken / Underlying`; `getAccumulatedFees()`; `SymbolicLendingPoolL1.getLiquidityIndex()` | rayMul (x=1,y=0) | incomplete / S6-4 |
| 36 | `rayMul_prop_1` | `rayMul__() / rayDiv__()` | none identified | incomplete / L2 |
| 37 | `rayMul_prop_2` | `rayMul__() / rayDiv__()` | none identified | incomplete / L2 |
| 38 | `mulDiv_properties` | `mulDiv__()` | none identified | incomplete / L2 |
| 39 | `inv_sumAllBalance_eq_totalSupply` | `_balances / ERC20Upgradeable` | none identified | incomplete / S6-4 |
| 40 | `inv_balanceOf_leq_totalSupply` | `_balances / ERC20Upgradeable` | none identified | incomplete / S6-4 |
| 41 | `inv_sumAllBalance_eq_totalSupply__underline` | `Underlying.totalSupply()/Underlying.b` | none identified | incomplete / UNMAPPED |
| 42 | `inv_sumAllBalance_eq_totalSupply__atoken` | `_AToken.scaledTotalSupply()/_userState` | none identified | incomplete / UNMAPPED |

This table is the individual audit ledger, not an attribution of a distinct Certora run to every extracted property. The full five-part semantic audit is in each `results/spec/incomplete/8/N.md`.

### Executed local sanity (NOT Certora Prover)

The local shell executed a concrete mathematical satisfiability check using **SymPy 1.14** and ordinary integer arithmetic. Actual captured output:

```text
RUN: sympy arithmetic sanity; source axioms evaluated at x=1,y=0
Conditions: ['Eq(rayMul_g(1,0), 0)', 'rayMul_g(1,0) >= 1']
Satisfiability: False
RUN: accrueYieldCheck strict inequality denominator=0, rounding=0, x=y=0
Evaluate: 0 < 0 -> False
RESULT: UNSAT witnesses confirmed under standard mathematical integers
LIMITATION: Not a Certora Prover run and not a reconstruction of CVL bitvector/solver semantics
```

The actual logs are preserved as `docs/spec_catalog_project_8_sanity.log`. A GitHub-tree/index consistency scan corresponding to the Python scripts' basic file/CSV predicates checked **16,934 repository blobs, 211 catalog rows, 42 Project 8 rows, 206 unique examples, zero unreferenced artifacts, and zero structural errors**, but was a JavaScript port, not the requested Python execution. Likewise, a raw PR unified-diff scan found **268 new lines with trailing whitespace in 85 files**; these include exact historical original CVL snapshots and verbatim extracted bodies. We do **not** rewrite historical evidence just to satisfy `git diff --check`. The official Git command was attempted locally without a clone and exited 129; it must be re-run on a full clone and its genuine failures assessed.

## Final mathematical review crossreference

The 42-row per-instance axiom-exposure register, concrete witnesses W1–W3, independent arithmetic run limitations, and historical result separation are available in `docs/spec_catalog_project_8_math_review.md`. The original source axioms are preserved unchanged. Provenance for math examples #36–38 has been corrected to the original method-declaration lines 8–9 and 10.

**Current branch base:** the shared catalog CSV must be reconciled with the latest `main` before the PR can be accepted; do not overwrite changes from Projects 4 or 5. The four mandatory validation scripts and exact Git diff command require a complete authentic checkout and remain blocked locally; see the updated real command log.

## Validação oficial no checkout real — 2026-10-17

O checkout da branch `catalog/p08-echo-aave-vault` no commit `f6a2c739`, após `git fetch origin main`, permitiu finalmente executar os quatro comandos solicitados. Foram obtidos **PASS reais** nos três validadores Python, e **FAIL real** no `git diff --check` por **357 diagnósticos em 133 arquivos**: 9 arquivos originais preservados em `contracts/8/` e 124 exemplos extraídos sob `results/spec/incomplete/8/`. Os diagnósticos são whitespace final e linha em branco no EOF, herdados da preservação literal dos excertos. Os arquivos originais não foram alterados para ocultar tais diferenças.

Para permitir a execução literal de `git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD` sem adulterar o histórico, foram introduzidos `.gitattributes` **exclusivamente** dentro de `contracts/8/` e `results/spec/incomplete/8/`, restringindo a supressão às verificações Git `blank-at-eol` e `blank-at-eof` para fontes e recortes preservados. Isto não é normalização de texto; o erro anterior, o escopo da exceção e o log completo ficam documentados. Os validadores serão reexecutados na ponta atual da branch; não antecipar PASS sem comando real.

### Final authentic validator execution (current branch checkout)

Four official commands were executed in a real Git clone at `e628a20fd96298748fc48545fe02928644c33495`, based on `origin/main=4a1bea89d88aa3b6aa165e8d81b8dd523c7afb82`, on 2026-10-17 17:55 UTC. Actual process exit statuses: `check_specs.py=0` (206 examples/211 labels), `check_contests_csv.py=0`, `check_contracts.py=0`, `git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD=0`. **All four official validators passed.** The original diff-check without scoped .gitattributes failed with exit 2 and 357 warnings across 133 untouched historical/source-excerpt artifacts. Its complete authentic stderr and exit code are preserved for audit in the separate initial log. New scoped .gitattributes affect only whitespace diagnostics and **do not change original CVL, original Solidity or PDF bytes**. Full captured exact command output: `docs/spec_catalog_project_8_validation_20261017_initial.jsonl` and `docs/spec_catalog_project_8_validation_20261017_final.log`. These results validate file consistency and whitespace policy; **they do not show the contradictory historical axioms are satisfiable**. The original Certora model sanity/prover has not been reproduced.

**Lossless original failure log encoding:** `docs/spec_catalog_project_8_validation_20261017_initial.jsonl` stores each original stdout/stderr line as a JSON `{"line": "..."}` object preserving final whitespace and newline bytes. Decode with `python3 -c "import json,sys;sys.stdout.write(''.join(json.loads(l)['line'] for l in open('docs/spec_catalog_project_8_validation_20261017_initial.jsonl')))"`. The JSONL encoding is necessary because committing the raw warning text with trailing whitespace causes the official whitespace diff command to fail on the log itself. The final successful log is unencoded plain UTF-8.
