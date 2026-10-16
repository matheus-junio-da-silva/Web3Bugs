# Project 7 — Delta / AAVE V3 historical spec catalog

## Inventory and coverage

Exactly 74 active rule/invariant instances in six supplied specs, each with one separately identified source/target instance. Commented-out `canBurnAtZero` (StableDebtToken), historical `withdrawCheck` and `accruToTreasury` (pool), and commented UserConfiguration rules/invariants are excluded.

| Source spec | Active rules | Active invariants | Complete | Incomplete | VERIFIED | NOT_STATED |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| AToken.spec | 11 | 1 | 7 | 5 | 10 | 2 |
| ReserveConfiguration.spec | 20 | 0 | 13 | 7 | 0 | 20 |
| StableDebtToken.spec | 14 | 1 | 13 | 2 | 6 | 9 |
| UserConfiguration.spec | 6 | 6 | 0 | 12 | 7 | 5 |
| VariableDebtToken.spec | 13 | 1 | 13 | 1 | 8 | 6 |
| pool.spec | 1 | 0 | 0 | 1 | 0 | 1 |
| **Total** | **65** | **9** | **46** | **28** | **31** | **43** |

All 74 examples have exactly one semantic Bug Label row; **74 CSV relationship rows**. All 31 individually report-matched rules have Detection Outcome NO_FINDING; all 43 unmatched have NOT_STATED. No property is attributed VIOLATED/FINDING by name. The report's separately described Pool findings are not silently mapped to these source rules. `UNMAPPED`: 0; the active rules/invariants here state normative expected behavior.

## Original evidence and textual snapshot integrity

- Source tree: https://github.com/matheus-junio-da-silva/PropertyGPT/tree/main/certora_projects/aave_v3
- Original historical report: https://hackmd.io/Do1H0F5SRhiQjxUVIlN1qA and https://github.com/matheus-junio-da-silva/PropertyGPT/blob/main/certora_projects/aave_v3/AaveV3Jan2022-1.pdf
- Fetched contracts source subtree SHA: `2f36249e11c994137e189dae465162945a6fe80e` (128 Solidity/text blobs); specs subtree SHA: `391f188fd008c13359580d42c1437ff5da1bcaf3` (six source specs); per-spec Git blobs listed below.
- `AToken.spec`: `fe5488dc0e0b245a0d4e71fd188f5cc1cb1e17b7`
- `ReserveConfiguration.spec`: `887f1effbb634dfb692c804c47f993a0961e5d09`
- `StableDebtToken.spec`: `fbff132d9b033fac51db9585026ae089eb2ce166`
- `UserConfiguration.spec`: `b89918ce07d8401857f643333730b0a1fcb49d9a`
- `VariableDebtToken.spec`: `89afd41f9732ef3c8f487e46059a8f1154f8e013`
- `pool.spec`: `a94fa404a2cb416ee5a0d6a19e295c5ed7680d20`
- The Git object storage does not accept binary fetching through the available connector. The original PDF has source Git blob SHA `4e2907f9830c990c08e71a7dbe222696f4f8d150` but **the PDF has not been copied or byte-verified**. Do not mark the entire provenance requirement complete. Source text files are prepared as exact UTF-8 content; compare Git blobs after commit.

## Missing dependency evidence

- **AToken.spec**: 5 incomplete instance(s), with individual `.txt` documenting exact symbols, references and searched directories.
- **ReserveConfiguration.spec**: 7 incomplete instance(s), with individual `.txt` documenting exact symbols, references and searched directories.
- **StableDebtToken.spec**: 2 incomplete instance(s), with individual `.txt` documenting exact symbols, references and searched directories.
- **UserConfiguration.spec**: 12 incomplete instance(s), with individual `.txt` documenting exact symbols, references and searched directories.
- **VariableDebtToken.spec**: 1 incomplete instance(s), with individual `.txt` documenting exact symbols, references and searched directories.
- **pool.spec**: 1 incomplete instance(s), with individual `.txt` documenting exact symbols, references and searched directories.
Missing items include AToken linked `SimpleERC20`, `scaledBalanceOfToBalanceOf`, `additionalData` getter; ReserveConfiguration absent mock wrappers and ID-dispatch setters/getters; UserConfiguration historical map-backed harness; Pool `ATokenHarness` and `getCurrScaledVariableDebt`. Cross-project substitutes were not used.

## Report statements and assumptions

The Certora report dates its work from November 12, 2021 to January 24, 2022 and identifies reviewed commit `a87d546`. The report indicates unit accumulation rates (no interest accumulation), arbitrary deterministic hashes, loop unrolling that misses violations requiring more than one iteration, external-call effects abstracted without changes to the target's state, and absence of incentives-controller usage. Some code has explicit `NONDET`, `ALWAYS`, `DISPATCHER`, ray summarization and fixed `gRNI/gRNVB` assumptions. These are preservation/precision limits, not safety guarantees. CVL1/CVL2 compatibility and original prover configuration are not reproduced.

The source/report relation is notably non-bijective: ReserveConfiguration's report uses an aggregate setter/getter formula, whereas source contains eighteen separate setter rules plus two selector-ID rules; individual result remains NOT_STATED. The report describes multiple Pool conditions and findings not represented as active rules in the supplied `pool.spec` (whose sole active normalized-variable-debt-index rule is not individually reported). Stable/Variable/AToken results are matched only when the description is uniquely corresponding to a source rule, and are **not** inferred across tokens.

## Formal outcome and finding separation

The report describes critical health-factor, high isolation-collateral and EMode price-feed, medium EMode liquidation-bonus and aToken-interest-rate, low reserve-list duplication, and recommendation-level isolation-mode behavior. These describe verification/audit work outside the exact active CVL rule set supplied here. No unsupported individual finding or result is invented for the 74 active rules. Finding labels are not substituted for property labels.

## Reproduction and validation status

**BLOCKED:** the GitHub connector's UTF-8-only reader cannot fetch the PDF's binary bytes; the remote Desktop Commander computer is offline, and the local container cannot resolve GitHub. Hence the source PDF and a faithful PDF-to-Markdown report transcription are not available through this session; the real `python scripts/check_specs.py .`, `python scripts/check_contests_csv.py .`, `python scripts/check_contracts.py .`, and `git diff --check` were **not executed**. These must not be reported as PASS; an independent checkout with those utilities is required before merge. The present semantic inventory and source-specific audit do not replace them. This PR, if opened, is subject to remediation of the report/validation blockers.

## Individual semantic second audit

Columns explicitly record (a) false assertion/counterexample, (b) label, (c) normative/diagnostic classification, (d) report attribution, and (e) source rule and target separation; no aggregate status is propagated without an individual correspondence.

| Example | Source instance | Counterexample making assertion false | Bug Label justification | Nature | Report attribution and target check |
| --- | --- | --- | --- | --- | --- |
| 1 | AToken / `totalSupplyEqualsSumAllBalance` | Total supply disagrees with the CVL ghost sum of account balances after the scale-conversion helper | S6-4 | Normative | NOT_STATED/NOT_STATED; AToken |
| 2 | AToken / `permitIntegrity` | A successful signature authorization fails to set the intended allowance or increment the nonce exactly once | S3-2 | Normative | NOT_STATED/NOT_STATED; AToken |
| 3 | AToken / `mintArgsPositive` | A successful mint of zero would violate the mandatory rejection of an invalid amount | SE-4 | Normative | VERIFIED/NO_FINDING; AToken |
| 4 | AToken / `balanceOfChange` | An arbitrary non-view operation changes the balances of too many distinct users | S3-2 | Normative | VERIFIED/NO_FINDING; AToken |
| 5 | AToken / `integrityMint` | The mint/burn/transfer operation fails the encoded before/after balance, supply or underlying-asset accounting assertions | S6-4 | Normative | VERIFIED/NO_FINDING; AToken |
| 6 | AToken / `additiveMint` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | VERIFIED/NO_FINDING; AToken |
| 7 | AToken / `integrityTransfer` | The mint/burn/transfer operation fails the encoded before/after balance, supply or underlying-asset accounting assertions | S6-4 | Normative | VERIFIED/NO_FINDING; AToken |
| 8 | AToken / `additiveTransfer` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | VERIFIED/NO_FINDING; AToken |
| 9 | AToken / `integrityBurn` | The mint/burn/transfer operation fails the encoded before/after balance, supply or underlying-asset accounting assertions | S6-4 | Normative | VERIFIED/NO_FINDING; AToken |
| 10 | AToken / `additiveBurn` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | VERIFIED/NO_FINDING; AToken |
| 11 | AToken / `burnNoChangeToOther` | A burn/mint changes an unrelated account's balance or tracked additional data | S3-2 | Normative | VERIFIED/NO_FINDING; AToken |
| 12 | AToken / `mintNoChangeToOther` | A burn/mint changes an unrelated account's balance or tracked additional data | S3-2 | Normative | VERIFIED/NO_FINDING; AToken |
| 13 | ReserveConfiguration / `setLtvIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 14 | ReserveConfiguration / `setLiquidationThresholdIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 15 | ReserveConfiguration / `setLiquidationBonusIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 16 | ReserveConfiguration / `setDecimalsIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 17 | ReserveConfiguration / `setActiveIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 18 | ReserveConfiguration / `setFrozenIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 19 | ReserveConfiguration / `setPausedIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 20 | ReserveConfiguration / `setBorrowableInIsolationIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 21 | ReserveConfiguration / `setSiloedBorrowingIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 22 | ReserveConfiguration / `setBorrowingEnabledIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 23 | ReserveConfiguration / `setStableRateBorrowingEnabledIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 24 | ReserveConfiguration / `setReserveFactorIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 25 | ReserveConfiguration / `setBorrowCapIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 26 | ReserveConfiguration / `setSupplyCapIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 27 | ReserveConfiguration / `setDebtCeilingIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 28 | ReserveConfiguration / `setLiquidationProtocolFeeIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 29 | ReserveConfiguration / `setUnbackedMintCapIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 30 | ReserveConfiguration / `setEModeCategoryIntegrity` | The reserve setter's paired getter returns a different value than the value just supplied | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 31 | ReserveConfiguration / `integrityAndIndependencyOfIntSetters` | Setting one selected reserve-configuration field changes an unrelated field or fails to store the requested value | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 32 | ReserveConfiguration / `integrityAndIndependencyOfBoolSetters` | Setting one selected reserve-configuration field changes an unrelated field or fails to store the requested value | S3-2 | Normative | NOT_STATED/NOT_STATED; MockReserveConfiguration |
| 33 | StableDebtToken / `principalLessThanBalance` | A debt account's principal balance is greater than its compounded balance | S6-4 | Normative | NOT_STATED/NOT_STATED; StableDebtToken |
| 34 | StableDebtToken / `integrityBurn` | The mint/burn/transfer operation fails the encoded before/after balance, supply or underlying-asset accounting assertions | S6-4 | Normative | VERIFIED/NO_FINDING; StableDebtToken |
| 35 | StableDebtToken / `integrityMint` | The mint/burn/transfer operation fails the encoded before/after balance, supply or underlying-asset accounting assertions | S6-4 | Normative | VERIFIED/NO_FINDING; StableDebtToken |
| 36 | StableDebtToken / `integrityTimeStamp` | A state-changing call leaves getUserLastUpdated(user) after the transaction block timestamp | S3-2 | Normative | VERIFIED/NO_FINDING; StableDebtToken |
| 37 | StableDebtToken / `integrityDelegationWithSig` | A successful signature authorization fails to set the intended allowance or increment the nonce exactly once | S3-2 | Normative | NOT_STATED/NOT_STATED; StableDebtToken |
| 38 | StableDebtToken / `additiveBurn` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | VERIFIED/NO_FINDING; StableDebtToken |
| 39 | StableDebtToken / `inverseMintBurn` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | VERIFIED/NO_FINDING; StableDebtToken |
| 40 | StableDebtToken / `whoChangeTotalSupply` | A non-pool caller or a method other than mint/burn changes total supply; this restricts mutation but does not prove who the legitimate pool is independently | S5-3 | Normative | NOT_STATED/NOT_STATED; StableDebtToken |
| 41 | StableDebtToken / `nonceChangePermits` | A selector other than delegationWithSig changes the signature nonce | S3-2 | Normative | NOT_STATED/NOT_STATED; StableDebtToken |
| 42 | StableDebtToken / `additiveMint` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | NOT_STATED/NOT_STATED; StableDebtToken |
| 43 | StableDebtToken / `balanceOfChange` | An arbitrary non-view operation changes the balances of too many distinct users | S3-2 | Normative | VERIFIED/NO_FINDING; StableDebtToken |
| 44 | StableDebtToken / `burnZeroDoesntChangeBalance` | Burning zero changes a user's balance | S3-2 | Normative | NOT_STATED/NOT_STATED; StableDebtToken |
| 45 | StableDebtToken / `burnNoChangeToOther` | A burn/mint changes an unrelated account's balance or tracked additional data | S3-2 | Normative | NOT_STATED/NOT_STATED; StableDebtToken |
| 46 | StableDebtToken / `mintNoChangeToOther` | A burn/mint changes an unrelated account's balance or tracked additional data | S3-2 | Normative | NOT_STATED/NOT_STATED; StableDebtToken |
| 47 | StableDebtToken / `disallowedFunctionalities` | A debt-token transfer/approval method selected by disAllowedFunctions completes rather than reverting | SC | Normative | NOT_STATED/NOT_STATED; StableDebtToken |
| 48 | UserConfiguration / `setBorrowing` | A borrowing/collateral setter fails to make the corresponding bit getter equal to the supplied boolean | S3-2 | Normative | VERIFIED/NO_FINDING; UserConfiguration (library; historical harness unresolved) |
| 49 | UserConfiguration / `setBorrowingNoChangeToOther` | Changing a reserve's borrowing/collateral bit changes an unrelated reserve's borrowing or collateral bit | S3-2 | Normative | VERIFIED/NO_FINDING; UserConfiguration (library; historical harness unresolved) |
| 50 | UserConfiguration / `setUsingAsCollateral` | A borrowing/collateral setter fails to make the corresponding bit getter equal to the supplied boolean | S3-2 | Normative | VERIFIED/NO_FINDING; UserConfiguration (library; historical harness unresolved) |
| 51 | UserConfiguration / `setCollateralNoChangeToOther` | Changing a reserve's borrowing/collateral bit changes an unrelated reserve's borrowing or collateral bit | S3-2 | Normative | VERIFIED/NO_FINDING; UserConfiguration (library; historical harness unresolved) |
| 52 | UserConfiguration / `isUsingAsCollateralOrBorrowing` | The combined flag disagrees with the logical OR of borrowing and collateral bits | S3-2 | Normative | VERIFIED/NO_FINDING; UserConfiguration (library; historical harness unresolved) |
| 53 | UserConfiguration / `integrityOfisUsingAsCollateralOne` | The one-reserve flag is true although two distinct reserve positions satisfy the underlying bit predicate | S3-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 54 | UserConfiguration / `integrityOfisUsingAsCollateralAny` | A particular reserve bit is true although the aggregate any-reserve flag is false | S3-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 55 | UserConfiguration / `integrityOfisBorrowingOne` | The one-reserve flag is true although two distinct reserve positions satisfy the underlying bit predicate | S3-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 56 | UserConfiguration / `integrityOfisBorrowingAny` | A particular reserve bit is true although the aggregate any-reserve flag is false | S3-2 | Normative | VERIFIED/NO_FINDING; UserConfiguration (library; historical harness unresolved) |
| 57 | UserConfiguration / `integrityOfEmpty` | isEmpty is true even though borrowing-any or a borrowing/collateral bit is true | S3-2 | Normative | VERIFIED/NO_FINDING; UserConfiguration (library; historical harness unresolved) |
| 58 | UserConfiguration / `integrityOfIsolationModeState` | getIsolationModeState reports isolation despite isUsingAsCollateralOne being false | S3-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 59 | UserConfiguration / `integrityOfSiloedBorrowingState` | getSiloedBorrowingState reports siloed borrowing despite isBorrowingOne being false | S3-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 60 | VariableDebtToken / `totalSupplyEqualsSumAllBalance` | Total supply disagrees with the CVL ghost sum of account balances after the scale-conversion helper | S6-4 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 61 | VariableDebtToken / `whoChangeTotalSupply` | A non-pool caller or a method other than mint/burn changes total supply; this restricts mutation but does not prove who the legitimate pool is independently | S5-3 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 62 | VariableDebtToken / `balanceOfChange` | An arbitrary non-view operation changes the balances of too many distinct users | S3-2 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 63 | VariableDebtToken / `nonceChangePermits` | A selector other than delegationWithSig changes the signature nonce | S3-2 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 64 | VariableDebtToken / `inverseMintBurn` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 65 | VariableDebtToken / `integrityDelegationWithSig` | A successful signature authorization fails to set the intended allowance or increment the nonce exactly once | S3-2 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 66 | VariableDebtToken / `integrityOfBurn` | The mint/burn/transfer operation fails the encoded before/after balance, supply or underlying-asset accounting assertions | S6-4 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 67 | VariableDebtToken / `additiveBurn` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 68 | VariableDebtToken / `additiveMint` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 69 | VariableDebtToken / `integrityMint` | The mint/burn/transfer operation fails the encoded before/after balance, supply or underlying-asset accounting assertions | S6-4 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 70 | VariableDebtToken / `burnZeroDoesntChangeBalance` | Burning zero changes a user's balance | S3-2 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 71 | VariableDebtToken / `burnNoChangeToOther` | A burn/mint changes an unrelated account's balance or tracked additional data | S3-2 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 72 | VariableDebtToken / `mintNoChangeToOther` | A burn/mint changes an unrelated account's balance or tracked additional data | S3-2 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 73 | VariableDebtToken / `disallowedFunctionalities` | A debt-token transfer/approval method selected by disAllowedFunctions completes rather than reverting | SC | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 74 | pool / `getReserveNormalizedVariableDebtCheck` | When pre-existing scaled variable debt is nonzero, supply lowers the normalized variable-debt index | S3-2 | Normative | NOT_STATED/NOT_STATED; Pool |
