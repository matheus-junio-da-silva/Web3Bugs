# Project 7 — Delta / AAVE V3 historical spec catalog

## Inventory and coverage

Exactly 74 active rule/invariant instances in six supplied specs, each with one separately identified source/target instance. Commented-out `canBurnAtZero` (StableDebtToken), historical `withdrawCheck` and `accruToTreasury` (pool), and commented UserConfiguration rules/invariants are excluded.

| Source spec | Active rules | Active invariants | Complete | Incomplete | VERIFIED | NOT_STATED |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| AToken.spec | 11 | 1 | 7 | 5 | 5 | 7 |
| ReserveConfiguration.spec | 20 | 0 | 13 | 7 | 0 | 20 |
| StableDebtToken.spec | 14 | 1 | 13 | 2 | 5 | 10 |
| UserConfiguration.spec | 6 | 6 | 0 | 12 | 3 | 9 |
| VariableDebtToken.spec | 13 | 1 | 13 | 1 | 5 | 9 |
| pool.spec | 1 | 0 | 0 | 1 | 0 | 1 |
| **Total** | **65** | **9** | **46** | **28** | **18** | **56** |

All 74 examples have exactly one semantic Bug Label row; **74 CSV relationship rows**. After conservative rule-by-rule report matching, 18 instances remain VERIFIED/NO_FINDING and 56 instances are NOT_STATED/NOT_STATED; thirteen prior VERIFIED attributions have been downgraded due to materially different source assertions or missing historical proof preconditions. No property is attributed VIOLATED/FINDING by name. The report's separately described Pool findings are not silently mapped to these source rules. `UNMAPPED`: 0; the active rules/invariants here state normative expected behavior.

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
- **Original report PDF preserved byte-identically:** `resources/7/AaveV3Jan2022-1.pdf` has source and destination Git blob `4e2907f9830c990c08e71a7dbe222696f4f8d150` (115,198 bytes). `reports/7.md` now contains a section-wise Markdown rendering, with normalization/paraphrase disclosures; PDF remains authoritative for exact legal and mathematical wording.

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
| 5 | AToken / `integrityMint` | The mint/burn/transfer operation fails the encoded before/after balance, supply or underlying-asset accounting assertions | S6-4 | Normative | NOT_STATED/NOT_STATED; AToken |
| 6 | AToken / `additiveMint` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | NOT_STATED/NOT_STATED; AToken |
| 7 | AToken / `integrityTransfer` | The mint/burn/transfer operation fails the encoded before/after balance, supply or underlying-asset accounting assertions | S6-4 | Normative | NOT_STATED/NOT_STATED; AToken |
| 8 | AToken / `additiveTransfer` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | VERIFIED/NO_FINDING; AToken |
| 9 | AToken / `integrityBurn` | The mint/burn/transfer operation fails the encoded before/after balance, supply or underlying-asset accounting assertions | S6-4 | Normative | NOT_STATED/NOT_STATED; AToken |
| 10 | AToken / `additiveBurn` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | NOT_STATED/NOT_STATED; AToken |
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
| 36 | StableDebtToken / `integrityTimeStamp` | A state-changing call leaves getUserLastUpdated(user) after the transaction block timestamp | S3-2 | Normative | NOT_STATED/NOT_STATED; StableDebtToken |
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
| 48 | UserConfiguration / `setBorrowing` | A borrowing/collateral setter fails to make the corresponding bit getter equal to the supplied boolean | S3-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 49 | UserConfiguration / `setBorrowingNoChangeToOther` | Changing a reserve's borrowing/collateral bit changes an unrelated reserve's borrowing or collateral bit | S3-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 50 | UserConfiguration / `setUsingAsCollateral` | A borrowing/collateral setter fails to make the corresponding bit getter equal to the supplied boolean | S3-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 51 | UserConfiguration / `setCollateralNoChangeToOther` | Changing a reserve's borrowing/collateral bit changes an unrelated reserve's borrowing or collateral bit | S3-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 52 | UserConfiguration / `isUsingAsCollateralOrBorrowing` | The combined flag disagrees with the logical OR of borrowing and collateral bits | S6-2 | Normative | VERIFIED/NO_FINDING; UserConfiguration (library; historical harness unresolved) |
| 53 | UserConfiguration / `integrityOfisUsingAsCollateralOne` | The one-reserve flag is true although two distinct reserve positions satisfy the underlying bit predicate | S6-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 54 | UserConfiguration / `integrityOfisUsingAsCollateralAny` | A particular reserve bit is true although the aggregate any-reserve flag is false | S6-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 55 | UserConfiguration / `integrityOfisBorrowingOne` | The one-reserve flag is true although two distinct reserve positions satisfy the underlying bit predicate | S6-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 56 | UserConfiguration / `integrityOfisBorrowingAny` | A particular reserve bit is true although the aggregate any-reserve flag is false | S6-2 | Normative | VERIFIED/NO_FINDING; UserConfiguration (library; historical harness unresolved) |
| 57 | UserConfiguration / `integrityOfEmpty` | isEmpty is true even though borrowing-any or a borrowing/collateral bit is true | S6-2 | Normative | VERIFIED/NO_FINDING; UserConfiguration (library; historical harness unresolved) |
| 58 | UserConfiguration / `integrityOfIsolationModeState` | getIsolationModeState reports isolation despite isUsingAsCollateralOne being false | S6-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 59 | UserConfiguration / `integrityOfSiloedBorrowingState` | getSiloedBorrowingState reports siloed borrowing despite isBorrowingOne being false | S6-2 | Normative | NOT_STATED/NOT_STATED; UserConfiguration (library; historical harness unresolved) |
| 60 | VariableDebtToken / `totalSupplyEqualsSumAllBalance` | Total supply disagrees with the CVL ghost sum of account balances after the scale-conversion helper | S6-4 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 61 | VariableDebtToken / `whoChangeTotalSupply` | A non-pool caller or a method other than mint/burn changes total supply; this restricts mutation but does not prove who the legitimate pool is independently | S5-3 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 62 | VariableDebtToken / `balanceOfChange` | An arbitrary non-view operation changes the balances of too many distinct users | S3-2 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 63 | VariableDebtToken / `nonceChangePermits` | A selector other than delegationWithSig changes the signature nonce | S3-2 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 64 | VariableDebtToken / `inverseMintBurn` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 65 | VariableDebtToken / `integrityDelegationWithSig` | A successful signature authorization fails to set the intended allowance or increment the nonce exactly once | S3-2 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 66 | VariableDebtToken / `integrityOfBurn` | The mint/burn/transfer operation fails the encoded before/after balance, supply or underlying-asset accounting assertions | S6-4 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 67 | VariableDebtToken / `additiveBurn` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 68 | VariableDebtToken / `additiveMint` | The two operation sequences produce different balances beyond the encoded equality or rounding tolerance | S6-4 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 69 | VariableDebtToken / `integrityMint` | The mint/burn/transfer operation fails the encoded before/after balance, supply or underlying-asset accounting assertions | S6-4 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 70 | VariableDebtToken / `burnZeroDoesntChangeBalance` | Burning zero changes a user's balance | S3-2 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 71 | VariableDebtToken / `burnNoChangeToOther` | A burn/mint changes an unrelated account's balance or tracked additional data | S3-2 | Normative | VERIFIED/NO_FINDING; VariableDebtToken |
| 72 | VariableDebtToken / `mintNoChangeToOther` | A burn/mint changes an unrelated account's balance or tracked additional data | S3-2 | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 73 | VariableDebtToken / `disallowedFunctionalities` | A debt-token transfer/approval method selected by disAllowedFunctions completes rather than reverting | SC | Normative | NOT_STATED/NOT_STATED; VariableDebtToken |
| 74 | pool / `getReserveNormalizedVariableDebtCheck` | When pre-existing scaled variable debt is nonzero, supply lowers the normalized variable-debt index | S3-2 | Normative | NOT_STATED/NOT_STATED; Pool |

## Closure re-extraction and semantic re-audit — 2026-10-16

**Branch:** `catalog/p07-delta-aave-v3`; existing PR #3 remains draft. **Exactly 74 original property instances** (65 rules and 9 invariants) across six source specs. Historical snapshot under `contracts/7/` was not modified.

- The 74 generated `.spec` files no longer contain the full global preamble; `methods {}` declarations are selected by transitive symbol use and modeling side effects. Necessary original `definition`, `function`, `ghost`, `hook`, `using` spans are retained literally, including historical syntax. Original per-instance dependency source ranges have been recomputed in `spec_buglabel.csv` and the example markdown.
- **46 complete / 28 incomplete remain PROVISIONAL classifications**, inherited from the first audit. They have undergone an in-source dependency-closure pass, but exact ABI/harness/linked-target closure and historical Certora execution remain unproven. The status is not an execution result.
- All 74 per-instance `.md` files now contain literal original assertions or invariants whose negation describes a falsification; no generic named-rule method invocation is passed off as a Solidity call. Implication guards, `require`s and the difference between state mutation and getter behavior are documented.
- The eight UserConfiguration instances 52–59 have been relabeled from `S3-2` to `S6-2` where their predicates compare getters/booleans without asserting a state mutation; this is a rule-level categorization, not a historical finding.
- The report explicitly records two **aggregate** ReserveConfiguration conditions; its Pool proof list covers reserve lists, EModes, caps and flags, **not** the active snapshot's `getReserveNormalizedVariableDebtCheck`. No aggregated result has been assigned to the 20 ReserveConfiguration rules or the lone Pool rule.
- The report's verified commit `a87d546` is different from the later PropertyGPT Solidity snapshot. The 2022 version lacks several later UserConfiguration/ReserveConfiguration methods, including siloed-borrowing support; historical proof results must be qualified accordingly.
- Historical source context: `aave/aave-v3-core@a87d546` contains `specs/harness/UserConfigurationHarness.sol`, `StableDebtTokenHarness.sol`, `PoolHarnessForVariableDebtToken.sol` and historical CLI scripts. These are **not** silently copied into the PropertyGPT snapshot or used to declare in-snapshot completeness.
- Findings in `results/bugs.csv` are report-level findings. **None is spuriously equated to the one active Pool rule or the other source properties.** Detection Outcome remains a separate column.

### Validation not yet evidenced

The GitHub connector permits exact Git blob/tree verification and structural CSV checks but does not provide a live checkout/terminal. The authorized Desktop Commander target is offline, and the local execution environment has no GitHub DNS connectivity. Consequently the following remain **NOT RUN**, not PASS:

```bash
python scripts/check_specs.py .
python scripts/check_contests_csv.py .
python scripts/check_contracts.py .
git diff --check
```

The PR must remain draft until the orquestrator has reviewed actual script logs and confirmed any remaining semantic/target issues. Git object and CSV checks are not substitutes for CVL2 compilation or historical Certora reproduction.


### Remote checks performed after re-extraction

- **PASS (remote literal-source comparison only):** All **74/74** extracted CVL property bodies match the text of their active source `rule` or `invariant` in the six PropertyGPT spec files. Comparison used GitHub's PR changed-file patches and original spec text, not execution of a prover.
- **PASS (remote Git-tree consistency only):** 74 Project-7 index rows reference all 250 expected files (46×3 complete files plus 28×4 incomplete files), with zero missing/orphan Project-7 example files. Original contract and spec source trees are byte-identical to PropertyGPT, and the report PDF blob matches its source SHA.
- **PASS (remote permitted-path check only):** All 390 currently changed PR file paths fall under the Project-7 source/spec/resource/report/documentation paths or the three explicitly permitted shared CSV indexes.
- **WARNING (not an executed `git diff --check`):** GitHub's diff adds lines containing trailing whitespace in **49 files**, of which 6 are original historical source specs and 43 are literal extracted CVL specs. The user-required historical byte-preservation forbids silently stripping those original whitespaces. Standard `git diff --check` may fail; its actual return code is not known because no shell execution environment is available.
- **NOT RUN:** All three official Python scripts and `git diff --check`, for reasons detailed above. Do not present the remote checks as a validator PASS.

## Historical results re-attribution (2026-10-17)

The original 31 reported VERIFIED matches were individually checked against the actual CVL assertion and the January 2022 report's verification-condition statement. Nine source properties were **downgraded** because their assertion is stronger, differently guarded or not identical to the reported condition:

- Example **5** — The source checks scaled supply deltas, positivity, and underlying-balance change under a 7×ray ghost. The report's AToken mint condition checks approximate beneficiary balance increase; it is not an exact one-to-one result.
- Example **7** — The source adds a from==to branch and stronger constraints on underlying balances; the historical AToken transfer condition does not state the entire same rule.
- Example **9** — The source has extra total-supply and system-underlying assertions and conditional branches beyond the report's burn condition.
- Example **48** — The report's setter proof explicitly requires reserveIndex < 128; this source rule omits that restriction.
- Example **49** — The report requires BOTH distinct indices to be <128; the source only checks inequality inside its implication.
- Example **50** — The report's setter proof explicitly requires reserveIndex < 128; this source rule omits that restriction.
- Example **51** — The report requires BOTH distinct indices to be <128; the source only checks inequality inside its implication.
- Example **69** — The source checks scaled supply change, positive supply growth and additional accounting as well as mint balance; the report states only the beneficiary balance increase.
- Example **72** — The source unconditionally asserts an unchanged delegating-user balance; the report conditions it on user != onBehalfOf, a materially different assertion.

Current Project-7 outcomes: **18 VERIFIED/NO_FINDING**, **56 NOT_STATED/NOT_STATED**, **zero rule-specific findings inferred from aggregate Pool or ReserveConfiguration statements**. Original source text, target snapshot and report PDF remain unchanged. No historic prover run was performed.

## Individually reviewed incomplete dependencies (2026-10-17)

The following 28 reasons supersede older generic or potentially misleading `.txt` descriptions; each example now lists exact symbols, context, source methods and missing ABI/harness requirements. The source `contracts/7/` snapshot remains untouched.

| Example | Missing or unavailable dependency |
| ---: | --- |
| 1 | scaledBalanceOfToBalanceOf(uint256) |
| 7 | using SimpleERC20 as _underlyingAsset |
| 9 | using SimpleERC20 as _underlyingAsset |
| 11 | additionalData(address) |
| 12 | additionalData(address) |
| 17 | setActive(bool); getActive() |
| 19 | setPaused(bool); getPaused() |
| 20 | setBorrowableInIsolation(bool); getBorrowableInIsolation() |
| 21 | setSiloedBorrowing(bool); getSiloedBorrowing() |
| 27 | setDebtCeiling(uint256); getDebtCeiling() |
| 31 | getIntSetterLowerBound(uint256); getIntSetterUpperBound(uint256); executeIntSetterById(uint256,uint256); executeIntGetterById(uint256) |
| 32 | getBoolSetterCompare(uint256); executeBoolSetterById(uint256,bool); executeBoolGetterById(uint256) |
| 45 | additionalData(address) |
| 46 | additionalData(address) |
| 48 | setBorrowing(uint256, bool) envfree; isBorrowing(uint256) returns bool envfree |
| 49 | setBorrowing(uint256, bool) envfree; isBorrowing(uint256) returns bool envfree; isUsingAsCollateral(uint256) returns bool envfree |
| 50 | setUsingAsCollateral(uint256, bool) envfree; isUsingAsCollateral(uint256) returns bool envfree |
| 51 | setUsingAsCollateral(uint256, bool) envfree; isBorrowing(uint256) returns bool envfree; isUsingAsCollateral(uint256) returns bool envfree |
| 52 | isUsingAsCollateralOrBorrowing(uint256) returns bool envfree; isBorrowing(uint256) returns bool envfree; isUsingAsCollateral(uint256) returns bool envfree |
| 53 | isUsingAsCollateral(uint256) returns bool envfree; isUsingAsCollateralOne() returns bool envfree |
| 54 | isUsingAsCollateral(uint256) returns bool envfree; isUsingAsCollateralAny() returns bool envfree |
| 55 | isBorrowing(uint256) returns bool envfree; isBorrowingOne() returns (bool) envfree |
| 56 | isBorrowing(uint256) returns bool envfree; isBorrowingAny() returns bool envfree |
| 57 | isUsingAsCollateralOrBorrowing(uint256) returns bool envfree; isBorrowingAny() returns bool envfree; isEmpty() returns bool envfree |
| 58 | isUsingAsCollateralOne() returns bool envfree; getIsolationModeState() returns (bool, address, uint256) envfree |
| 59 | isBorrowingOne() returns (bool) envfree; getSiloedBorrowingState() returns (bool, address) envfree |
| 60 | scaledBalanceOfToBalanceOf(uint256) |
| 74 | ATokenHarness as _aToken; getCurrScaledVariableDebt(address) |

**Classification scope:** 46 examples still meet the available-source static dependency-closure criterion, and 28 remain incomplete for the reasons above. This is a CVL/Solidity source-level classification only. Compiler compatibility, linked harness availability and the historical solver are separate, unexecuted verification obligations.

## Individual static dependency closure of all 46 complete examples — 2026-10-17

The table is an explicit symbol-level static audit of the *available snapshot*, not a claim of prover compilation or a reproduction of the historical Aave harness. All original CVL property bodies were already compared byte-literally against their source. Here, summaries and ghost/hook definitions are distinct from concrete target ABI methods; source-call-chain excerpts are counted separately. For an explanation of those full Solidity source ranges, consult each `N.md` and `N.sol`.

| ID | Property | CVL `methods` declarations included | CVL globals (definitions/ghosts/hooks) | Solidity excerpt regions | Static closure evidence |
| ---: | --- | --- | --- | ---: | --- |
| 2 | `permitIntegrity` | nonces, allowance | none | 3 | AToken target and inherited scaled-balance methods available; ghost index summary remains explicit CVL logic. |
| 3 | `mintArgsPositive` | implicit Solidity ABI | none | 2 | AToken target and inherited scaled-balance methods available; ghost index summary remains explicit CVL logic. |
| 4 | `balanceOfChange` | getReserveNormalizedIncome, balanceOf | ray, gRNI | 4 | AToken target and inherited scaled-balance methods available; ghost index summary remains explicit CVL logic. |
| 5 | `integrityMint` | handleAction, getReserveNormalizedIncome, balanceOf, scaledTotalSupply, scaledBalanceOf | ray, bound, bounded_error_eq, gRNI | 5 | AToken target and inherited scaled-balance methods available; ghost index summary remains explicit CVL logic. |
| 6 | `additiveMint` | handleAction, getReserveNormalizedIncome, balanceOf | ray, bound, bounded_error_eq, gRNI | 3 | AToken target and inherited scaled-balance methods available; ghost index summary remains explicit CVL logic. |
| 8 | `additiveTransfer` | handleAction, getReserveNormalizedIncome, balanceOf, finalizeTransfer | ray, bound, bounded_error_eq, gRNI | 4 | AToken target and inherited scaled-balance methods available; ghost index summary remains explicit CVL logic. |
| 10 | `additiveBurn` | handleAction, getReserveNormalizedIncome, balanceOf | ray, bound, bounded_error_eq, gRNI | 3 | AToken target and inherited scaled-balance methods available; ghost index summary remains explicit CVL logic. |
| 13 | `setLtvIntegrity` | setLtv, getLtv | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 14 | `setLiquidationThresholdIntegrity` | setLiquidationThreshold, getLiquidationThreshold | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 15 | `setLiquidationBonusIntegrity` | setLiquidationBonus, getLiquidationBonus | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 16 | `setDecimalsIntegrity` | setDecimals, getDecimals | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 18 | `setFrozenIntegrity` | setFrozen, getFrozen | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 22 | `setBorrowingEnabledIntegrity` | setBorrowingEnabled, getBorrowingEnabled | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 23 | `setStableRateBorrowingEnabledIntegrity` | setStableRateBorrowingEnabled, getStableRateBorrowingEnabled | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 24 | `setReserveFactorIntegrity` | setReserveFactor, getReserveFactor | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 25 | `setBorrowCapIntegrity` | setBorrowCap, getBorrowCap | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 26 | `setSupplyCapIntegrity` | setSupplyCap, getSupplyCap | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 28 | `setLiquidationProtocolFeeIntegrity` | setLiquidationProtocolFee, getLiquidationProtocolFee | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 29 | `setUnbackedMintCapIntegrity` | setUnbackedMintCap, getUnbackedMintCap | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 30 | `setEModeCategoryIntegrity` | setEModeCategory, getEModeCategory | none | 4 | Public mock wrapper pair and internal bit-packed library routines present. |
| 33 | `principalLessThanBalance` | calculateCompoundedInterest, handleAction, rayMul, rayDiv | RAY, disAllowedFunctions, mapping, calculateCompoundedInterestSummary, mapping, rayMulSummariztion, mapping, rayDivSummariztion | 3 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 34 | `integrityBurn` | calculateCompoundedInterest, handleAction, rayMul, rayDiv | RAY, mapping, calculateCompoundedInterestSummary, mapping, rayMulSummariztion, mapping, rayDivSummariztion | 3 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 35 | `integrityMint` | calculateCompoundedInterest, handleAction, rayMul, rayDiv | RAY, mapping, calculateCompoundedInterestSummary, mapping, rayMulSummariztion, mapping, rayDivSummariztion | 3 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 36 | `integrityTimeStamp` | implicit Solidity ABI | disAllowedFunctions | 1 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 37 | `integrityDelegationWithSig` | implicit Solidity ABI | none | 2 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 38 | `additiveBurn` | calculateCompoundedInterest, handleAction, rayMul, rayDiv | RAY, mapping, calculateCompoundedInterestSummary, mapping, rayMulSummariztion, mapping, rayDivSummariztion | 2 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 39 | `inverseMintBurn` | calculateCompoundedInterest, handleAction, rayMul, rayDiv | RAY, mapping, calculateCompoundedInterestSummary, mapping, rayMulSummariztion, mapping, rayDivSummariztion | 3 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 40 | `whoChangeTotalSupply` | calculateCompoundedInterest, handleAction, rayMul, rayDiv | RAY, disAllowedFunctions, mapping, calculateCompoundedInterestSummary, mapping, rayMulSummariztion, mapping, rayDivSummariztion | 3 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 41 | `nonceChangePermits` | implicit Solidity ABI | disAllowedFunctions | 2 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 42 | `additiveMint` | calculateCompoundedInterest, handleAction, rayMul, rayDiv | RAY, mapping, calculateCompoundedInterestSummary, mapping, rayMulSummariztion, mapping, rayDivSummariztion | 2 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 43 | `balanceOfChange` | calculateCompoundedInterest, handleAction, rayMul, rayDiv | RAY, disAllowedFunctions, mapping, calculateCompoundedInterestSummary, mapping, rayMulSummariztion, mapping, rayDivSummariztion | 2 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 44 | `burnZeroDoesntChangeBalance` | calculateCompoundedInterest, handleAction, rayMul, rayDiv | RAY, mapping, calculateCompoundedInterestSummary, mapping, rayMulSummariztion, mapping, rayDivSummariztion | 2 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 47 | `disallowedFunctionalities` | implicit Solidity ABI | disAllowedFunctions | 6 | Token ABI and summary definitions present; inherited delegation methods needed for signature checks are shown. |
| 61 | `whoChangeTotalSupply` | getReserveNormalizedVariableDebt, handleAction | ray, gRNVB, disAllowedFunctions | 3 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |
| 62 | `balanceOfChange` | getReserveNormalizedVariableDebt, balanceOf | ray, gRNVB, disAllowedFunctions | 3 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |
| 63 | `nonceChangePermits` | implicit Solidity ABI | disAllowedFunctions | 2 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |
| 64 | `inverseMintBurn` | getReserveNormalizedVariableDebt, handleAction, balanceOf | ray, gRNVB | 5 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |
| 65 | `integrityDelegationWithSig` | implicit Solidity ABI | none | 2 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |
| 66 | `integrityOfBurn` | getReserveNormalizedVariableDebt, handleAction, balanceOf | ray, bound, gRNVB, bounded_error_eq | 3 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |
| 67 | `additiveBurn` | getReserveNormalizedVariableDebt, handleAction, balanceOf | ray, bound, gRNVB, bounded_error_eq | 3 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |
| 68 | `additiveMint` | getReserveNormalizedVariableDebt, handleAction, balanceOf | ray, bound, gRNVB, bounded_error_eq | 3 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |
| 69 | `integrityMint` | getReserveNormalizedVariableDebt, handleAction, balanceOf | ray, bound, gRNVB, bounded_error_eq | 3 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |
| 70 | `burnZeroDoesntChangeBalance` | getReserveNormalizedVariableDebt, handleAction, balanceOf | ray, gRNVB | 3 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |
| 71 | `burnNoChangeToOther` | getReserveNormalizedVariableDebt, handleAction, balanceOf | ray, gRNVB | 3 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |
| 72 | `mintNoChangeToOther` | getReserveNormalizedVariableDebt, handleAction, balanceOf | ray, gRNVB | 4 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |
| 73 | `disallowedFunctionalities` | implicit Solidity ABI | disAllowedFunctions | 6 | VariableDebtToken target and inherited scaled-balance/delegation support present; no missing named helper identified. |

The status remains **complete only for in-snapshot static non-built-in symbol resolution**. An original report success and the future viability of `certoraRun` against a historically faithful harness are independent propositions. The three official validators and `git diff --check` have **not** been executed in this runtime because no clone-capable authorized terminal is available; their success is not asserted here.


## Final PDF formula and executable validation audit — 2026-10-17

The PDF is 8 pages; all source conditions were checked against text-layer extraction of the original PDF. Additional conservative `VERIFIED` withdrawals follow exact predicate comparisons:

- Example 6: The January 2022 report describes two mint operations versus one on the same beneficiary (up to an unspecified epsilon); the source checks two distinct beneficiaries from equal initial balances, with an explicit 3-scaled bound and a ghost normalized index.
- Example 10: The report states same-timestamp additivity of burn; this source performs two burns on one user and a separate single burn on another and asserts only bounded_error_eq(...,3) under extra distinctness guards. Equivalence of the complete conditions is not established.
- Example 36: The original PDF lists getUserLastUpdated(user) <= block.timestamp as an unconditional invariant. The source rule first requires this predicate in the pre-state and asserts its preservation only after allowed state-changing methods; it does not by itself establish unconditional reachability.
- Example 67: The report states exact burn additivity at one timestamp. The source asserts only bounded_error_eq(...,3); its exact equality assertion is explicitly commented out, so the historical exact result cannot be assigned to this literal rule.

**Project 7 final historical reporting:** 18 `VERIFIED` and 56 `NOT_STATED`, versus 31 initially attributed and 13 subsequently withdrawn. No extra `VIOLATED` or `FINDING` label is asserted for the 74 active source rules solely from a report-level issue.

### Official validator command evidence (real shell execution, before this documentation-only correction)

- Host checkout SHA: `53e44755d77cd877e8235aa1aa7e80abe2a0392c`; matching `origin/main`: `4a1bea89d88aa3b6aa165e8d81b8dd523c7afb82`.
- `python3 scripts/check_specs.py .`: **exit 0**, "Check passed! 238 spec examples and 243 Bug Label relationships are structurally consistent."
- `python3 scripts/check_contests_csv.py .`: **exit 0**, "Check passed!".
- `python3 scripts/check_contracts.py .`: **exit 0**, "Check passed!".
- `git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD`: **exit 2**, 220 trailing-whitespace diagnostics in historical original CVL files and literal per-example CVL excerpts (diagnostic log has 452 lines). Original byte identity and literal property text were not sacrificed to conceal this conflict.
- The same four commands must be rerun on the final updated HEAD to record post-correction results. The Python scripts check structural integrity, **not** theorem satisfiability or original Certora harness feasibility.

### Strict classification limitation

The 46 `complete` and 28 `incomplete` classifications are based on static dependency closure within the PropertyGPT snapshot, not on a compilation or run of the 2022 Certora harness. No external harness was silently created. The 28 missing-symbol reasons remain in the per-example `.txt` files. The difference between source commit `a87d546` and the PropertyGPT snapshot is material and unresolved at formal-equivalence level.
