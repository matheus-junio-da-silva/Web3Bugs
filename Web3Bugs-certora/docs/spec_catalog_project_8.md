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

**Total: 42** active property instances; **0 complete**, **42 incomplete**, with a literal property body in each `.spec`, genuine Solidity excerpts in each `.sol`, a five-point audit in each `.md`, and missing-symbol evidence in each `.txt`. Exactly **42 CSV rows** reference exactly **42 bundles**. Results: {"VERIFIED":6,"VIOLATED":5,"NOT_STATED":31}. Detection outcomes: {"NO_FINDING":6,"ACCEPTED_BEHAVIOR":5,"NOT_STATED":31}. Technical Bug Labels: {"S3-2":1,"S3-1":1,"L7":3,"S6-2":8,"UNMAPPED":8,"S6-4":18,"L2":3} (UNMAPPED only for auxiliary modeled external-token invariant instances). All filenames, source ranges and exact property identities are preserved.

## Property-by-property status and trace

| Example | Original source range | Exact property | Bug Label | Formal Result | Detection Outcome |
|---:|---|---|---|---|---|
| 1 | accrueYieldCheck.spec:39-45 | `accrueYieldCheck` | S3-2 | VERIFIED | NO_FINDING |
| 2 | changeInContractBalanceShouldCauseAccrual.spec:33-53 | `changeInContractBalanceShouldCauseAccrual` | S3-1 | VERIFIED | NO_FINDING |
| 3 | erc4626.spec:73-84 | `must_not_revert` | L7 | VIOLATED | ACCEPTED_BEHAVIOR |
| 4 | erc4626.spec:94-104 | `must_not_revert_unless_large_input__convertToShares` | L7 | NOT_STATED | NOT_STATED |
| 5 | erc4626.spec:114-124 | `must_not_revert_unless_large_input__convertToAssets` | L7 | NOT_STATED | NOT_STATED |
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

Required historical implementations that are absent include `AToken` (scaled balance and `_userState` hooks), `DummyERC20_aTokenUnderlying` (`Underlying.b`), `SymbolicLendingPoolL1`, `ATokenVaultHarness` typed signatures and entrypoint wrappers, getter `getAccumulatedFees`, external `accrueYield`, `havoc_all`, arithmetic probes `rayMul__`, `rayDiv__`, `mulDiv__`, plus required external OpenZeppelin/Aave dependencies. Internal `_accrueYield` is not a substitute for a missing external harness, and storage `_s.accumulatedFees` is not a declared external getter. No original verifier run scripts, .conf, package/link map, target assignments or pinned dependency checkout exist within the source snapshot. All 42 text explanations name absent dependencies and search scope. This is independent of CVL1/CVL2 syntax age; `complete` would mean only dependency closure, not a reproducible historical prover run.

## Result versus finding interpretation and report limitations

Exact report names #1–9, #16 and #17 support the corresponding individual outcomes, including four threshold checks and must_not_revert **VIOLATED / ACCEPTED_BEHAVIOR** rather than security findings. The report gives different aggregate name for #10 converter nonrevert rule, and #11–15 aggregate results cannot support status claims for every duplicated or specialized source rule. Those are `NOT_STATED` at source-instance granularity, even where source comments say pass or fail. Actual older-revision security findings (deposit rounding DoS, withdrawal griefing, protocol fee insolvency, arithmetic DoS, preview misinformation, fee rounding, inappropriate supply cap, same-block gift) are recorded in `results/bugs.csv` as eight separately report-supported rows. A report finding's technical/root label is not confused with the checked property's own Bug Label.

Report notation tick, tick-star, cross and timeout is described in `reports/8.md`, but never invented for unreported instances. Key limitations: bounded loop unrolling excludes >1-iteration counterexamples, signature cryptography is unverified, symbolic supply limits are common, and further idealized arithmetic identities/index bounds are assumed for fee/solvency proofs. No branch-local run config proves whether a given source instance ran against ATokenVault or ATokenVaultV2; mathematical probes have UNSPECIFIED target. The report's latest reviewed commit `23366cc` and earlier fix commits do not prove that PropertyGPT's source snapshot matches each historical version. The extracted CVL code is not migrated or corrected.

## Independent semantic second pass (all 42)

Each row audits **(a)** what state/call falsifies the literal assertion, **(b)** whether the technical label fits that condition, **(c)** normative versus auxiliary, **(d)** report attribution unsupported by this rule, and **(e)** separation of property, finding, result and target. Each individual `N.md` supplies a longer source-to-Solidity relationship.

| ID | (a) Falsifying counterexample | (b) Label rationale | (c) Normative/auxiliary | (d) Unsupported inference avoided | (e) Property/target guard |
|---:|---|---|---|---|---|
| 1 | Accrual lowers getAccumulatedFees() compared with the prior state. | S3-2 — Detect incorrect accumulated-fee state decrement during accrual. | normative | The report explicitly names this property in additional verification checks #16/#17 and marks it verified. | accrueYieldCheck.spec:39-45; historical V2 target linkage not supplied |
| 2 | A nonexempt method changes token balances but does not set accrueYieldCalled ghost. | S3-1 — Detect missing yield accrual when Vault token balances change. | normative | The report explicitly names this property in additional verification checks #16/#17 and marks it verified. | changeInContractBalanceShouldCauseAccrual.spec:33-53; historical V2 target linkage not supplied |
| 3 | A specified ERC4626 query reverts despite msg.value=0. | L7 — Detect arithmetic reverts in nonreverting ERC4626 view methods. | normative | The report names the aggregate must_not_revert check (#9) as violated and treats the arithmetic-dependent reverts as acceptable. | erc4626.spec:73-84; historical V2 target linkage not supplied |
| 4 | Bounded convertToShares or convertToAssets reverts. | L7 — Detect unexpected arithmetic revert for bounded asset/share conversion. | normative | The report's #10 is an aggregate named must_not_revert_unless_large_input, not either separate converter-specific source rule. | erc4626.spec:94-104; historical V2 target linkage not supplied |
| 5 | Bounded convertToShares or convertToAssets reverts. | L7 — Detect unexpected arithmetic revert for bounded asset/share conversion. | normative | The report's #10 is an aggregate named must_not_revert_unless_large_input, not either separate converter-specific source rule. | erc4626.spec:114-124; historical V2 target linkage not supplied |
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
