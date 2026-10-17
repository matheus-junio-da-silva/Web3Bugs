# Project 13 — Notional Finance V2: Historical Certora property catalog

## Provenance and scope

Source: PropertyGPT main, certora_projects/notional_finance_v2/. All 131 original files (15 original CVL specs, harnesses, contract libraries, scripts, configs and original PDF) were compared byte for byte after copying to contracts/13; the binary PDF is also preserved in resources/13. Git blob SHA of original PDF: 5269fea4100575c12ea03e8480e15674bd3a7c34. A page-indexed PDF text-layer transcript is reports/13.md, but the PDF remains authoritative for layout and formula formatting.

The original PDF describes work undertaken June 28 through September 19, 2021. The catalog contest month 2021-11 derives from the supplied November 1, 2021 PDF filename, not from those work dates. Source metadata is historical; no modern replacements are used.

## Complete active declaration inventory

58 active declarations: 58 unique source-file/target instances; all 58 are currently incomplete due unavailable original external dependency/toolchain snapshots. Each has N.spec, N.sol, N.md, N.txt. Additional declarations in comments, including oldAccountContext commented-out proposals, are excluded. notes.spec has no active rule/invariant. sanity.spec contains one active diagnostic rule. oldAccountContext.spec has four active declarations, preserved independently despite duplicate names.

The user-provided Notional report has 13 substantive (1 High, 6 Medium, 6 Low) issues and 13 recommendations. All 26 descriptions remain in the report transcript. Only 13 substantive findings are indexed in results/bugs.csv; recommendations without a substantive security issue are not force-mapped to a vulnerability label. These 13 report findings are NOT mechanically linked to any one of the CVL instances.

## Verification targets and contexts

Historical scripts establish: runAccountContext -> GetterSetterHarness/SetAccountContext.spec; runAccountPortfolio -> AccountPortfolioHarness/AccountPortfolio.spec; runActiveCurrencies -> AccountPortfolioHarness/ActiveCurrencies.spec; runPortfolio -> AccountPortfolioHarness/Portfolio.spec; runDateTime -> DateTimeHarness/DateTime.spec; runLiquidityCurve -> LiquidityCurveHarness/LiquidityCurve.spec; runSettlement -> SettlementHarness/Settlement.spec; runValuation -> ValuationHarness/Valuation.spec; runGovenanceOwner -> GovernanceActionHarness/GovernanceOwner.spec; runSanity -> FreeCollateralExternal/sanity.spec.
The source has no run-script evidence for oldAccountContext, cashGroupGetterSetters or the GovernanceAction.spec getter/setter rules: any selected harness for these is explicitly an inference. The Balances.spec contains placeholder rules and no source run target: UNRESOLVED is preserved. No target is substituted by a modern contract.

The .conf files invoke optimistic_loop, bounded loop iterations, bitvector SMT, plainInjectivity hashing and staging; the scripts use historic solc 0.7.5, Brownie-installed OpenZeppelin 3.4.0 and compound-finance. The report additionally states global market/balance contexts, mocked ERC20/asset tokens, and simplified ABDK math for the applicable proofs. The historical package/prover environment cannot be reconstructed solely from this snapshot.

## Formal results and audit interpretations

VERIFIED: 7; VIOLATED: 0; NOT_STATED: 51. Results are assigned only to unique source instances whose executable properties and historical script targets can be aligned with specific numbered report propositions; no aggregate report success is spread across duplicate or draft instances. NO_FINDING is used for the individually reported verified properties not explicitly attributed to one of the 13 substantive findings. No new prover proofs were run.

## Semantic review and proof scope

Report checkmarks are historical results only. The source rule settlementRatesAreNeverReset has an assert whose zero-prestate branch contradicts its after-rate-positive assert; no non-vacuity claim can be made. The root verify.sh explicitly excludes impliedRatesDoNotChangeOnRemoveLiquidity even though the report marks removing-liquidity rate preservation as verified; this discrepancy is preserved. GovernanceOwner filters all non-view methods, not just governance, so its source scope is broader than the report heading. CashGroup uses an undeclared marketIndex. updateDepositParametersSetsProperly has no executable assert; it is UNMAPPED. sanity and generic assert-false rules are diagnostics; they are not successful security proofs. The oldAccountContext variant never inherits the newer spec results. The Valuation bitmap asset accounting rule has source assumptions commented out and may fail for unrelated feasible inputs; original CVL is never altered.

## Property-by-property index

| Example | Source property | Bug Label | Formal Result | Detection Outcome | Historical target |
| ---: | --- | --- | --- | --- | --- |
| 1 | sanity | UNMAPPED | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 2 | nonZeroAssetArrayLength | S3-2 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 3 | integrityAssetArrayLength | S3-2 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 4 | enablingBitmapCannotLeaveBehindAssets | S5-2 | VERIFIED | NO_FINDING | AccountPortfolioHarness |
| 5 | bitmapPortfoliosCannotHaveAssetArray | S3-2 | VERIFIED | NO_FINDING | AccountPortfolioHarness |
| 6 | activeCurrenciesAreNotDuplicatedAndSorted | S2-3 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 7 | bitmapCurrencyIsNotDuplicatedInActiveCurrencies | UNMAPPED | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 8 | depositsMustIncreaseCashBalance | S6-4 | NOT_STATED | NOT_STATED | UNRESOLVED |
| 9 | withdrawsMustDecreaseCashBalance | UNMAPPED | NOT_STATED | NOT_STATED | UNRESOLVED |
| 10 | cannotWithdrawToNegativeCashBalance | UNMAPPED | NOT_STATED | NOT_STATED | UNRESOLVED |
| 11 | cannotWithdrawToNegativeFreeCollateral | UNMAPPED | NOT_STATED | NOT_STATED | UNRESOLVED |
| 12 | contractCannotHoldUnderlyingAssets | UNMAPPED | NOT_STATED | NOT_STATED | UNRESOLVED |
| 13 | mintingNTokensMustIncreaseBalanceAndSupply | UNMAPPED | NOT_STATED | NOT_STATED | UNRESOLVED |
| 14 | redeemNTokensMustDecreaseBalanceAndSupply | UNMAPPED | NOT_STATED | NOT_STATED | UNRESOLVED |
| 15 | transferNTokensMustNotChangeTotalSupply | UNMAPPED | NOT_STATED | NOT_STATED | UNRESOLVED |
| 16 | cannotHaveNegativeNTokenBalance | UNMAPPED | NOT_STATED | NOT_STATED | UNRESOLVED |
| 17 | nTokenBalanceChangeMustMintIncentives | UNMAPPED | NOT_STATED | NOT_STATED | UNRESOLVED |
| 18 | assetArrayLengthAlwaysMatchesActual | S3-2 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 19 | activeCurrencyAssetFlagsMatchActual | S3-2 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 20 | minSettlementTimeMatchesActualForAssetArray | S3-2 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 21 | hasPortfolioDebtMatchesActual | S3-2 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 22 | allBitmapBitsAreValid | S6-4 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 23 | activeCurrencyBalanceFlagsMatchActual | S3-2 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 24 | hasCashDebtMatchesActual | S3-2 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 25 | getAndSetAccountContext | S3-2 | NOT_STATED | NOT_STATED | GetterSetterHarness |
| 26 | noChangeToOther | S3-2 | NOT_STATED | NOT_STATED | GetterSetterHarness |
| 27 | bitNumAndMaturitiesMustMatch | S6-2 | NOT_STATED | NOT_STATED | DateTimeHarness |
| 28 | bitNumValidMaturitiesMustBeExact | S6-2 | NOT_STATED | NOT_STATED | DateTimeHarness |
| 29 | validMarketMaturitesHaveAnIndex | S6-2 | VERIFIED | NO_FINDING | DateTimeHarness |
| 30 | oracleRatesAreBlendedIntoTheRateWindow | S6-4 | NOT_STATED | NOT_STATED | LiquidityCurveHarness |
| 31 | oracleRatesBlandedIntoRateWindow | S6-4 | NOT_STATED | NOT_STATED | LiquidityCurveHarness |
| 32 | executeTradeMovesImpliedRates | S6-4 | VERIFIED | NO_FINDING | LiquidityCurveHarness |
| 33 | testAssetCash | S6-4 | NOT_STATED | NOT_STATED | LiquidityCurveHarness |
| 34 | impliedRatesDoNotChangeOnAddLiquidity | S3-2 | VERIFIED | NO_FINDING | LiquidityCurveHarness |
| 35 | impliedRatesDoNotChangeOnRemoveLiquidity | S3-2 | VERIFIED | NO_FINDING | LiquidityCurveHarness |
| 36 | impliedRateSlippageDoesNotChangeWithTime | S6-4 | NOT_STATED | NOT_STATED | LiquidityCurveHarness |
| 37 | sanity | UNMAPPED | NOT_STATED | NOT_STATED | LiquidityCurveHarness |
| 38 | settleAssetsDeletesSettleableAssets | S3-2 | NOT_STATED | NOT_STATED | SettlementHarness |
| 39 | settlementRatesAreNeverReset | S3-2 | NOT_STATED | NOT_STATED | SettlementHarness |
| 40 | settlingBitmapAssetsDoesNotLoseTrack | S6-4 | NOT_STATED | NOT_STATED | SettlementHarness |
| 41 | calculateOracleRateIsBetweenOnChainRates | S6-4 | NOT_STATED | NOT_STATED | ValuationHarness |
| 42 | presentValueDecreasesForLongerMaturities | S6-2 | NOT_STATED | NOT_STATED | ValuationHarness |
| 43 | riskAdjustedPresentValueDecreasesForLongerMaturities | S6-2 | NOT_STATED | NOT_STATED | ValuationHarness |
| 44 | riskAdjustedPresentValueIsLessThanPresentValue | S6-2 | NOT_STATED | NOT_STATED | ValuationHarness |
| 45 | riskAdjustedLiquidityTokenValueMatchesClaims | S6-4 | NOT_STATED | NOT_STATED | ValuationHarness |
| 46 | liquidityTokenValueMatchesClaims | S6-4 | NOT_STATED | NOT_STATED | ValuationHarness |
| 47 | portfolioIsAlwaysSorted | S3-2 | NOT_STATED | NOT_STATED | ValuationHarness |
| 48 | netCashGroupValueAccountsForAllAssets | S6-4 | NOT_STATED | NOT_STATED | ValuationHarness |
| 49 | ifCashNetPresentValueAccountsForAllAssets | S6-4 | NOT_STATED | NOT_STATED | ValuationHarness |
| 50 | cashGroupGetterSetters | S6-2 | NOT_STATED | NOT_STATED | CashGroupHarness |
| 51 | updateDepositParametersSetsProperly | UNMAPPED | NOT_STATED | NOT_STATED | GovernanceActionHarness |
| 52 | updateIncentiveEmissionRateSetsProperly | S3-2 | NOT_STATED | NOT_STATED | GovernanceActionHarness |
| 53 | onlyOwnerCanUpdateGovernace | S5-3 | VERIFIED | NO_FINDING | GovernanceActionHarness |
| 54 | enablingBitmapCannotLeaveBehindAssets | S5-2 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 55 | bitmapPortfoliosCannotHaveAssetArray | S3-2 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 56 | activeCurrenciesAreNotDuplicatedAndSorted | S2-3 | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 57 | bitmapCurrencyIsNotDuplicatedInActiveCurrencies | UNMAPPED | NOT_STATED | NOT_STATED | AccountPortfolioHarness |
| 58 | r | UNMAPPED | NOT_STATED | NOT_STATED | FreeCollateralExternal |

## Label distribution

S2-3: 2; S3-2: 18; S5-2: 2; S5-3: 1; S6-2: 7; S6-4: 13; UNMAPPED: 15

## Dependency and validation limitations

All samples retain original CVL exactly with original line ranges and available directly/recur­sively required definitions. Incomplete means historical source compilation dependencies remain unavailable, not merely CVL1-to-CVL2 migration. Some historical rules are aspirational or diagnostic and are documented as such.

Native required tests and the Git diff whitespace check must be run against the committed HEAD, and their actual stdout/stderr, SHA and exit codes recorded. A native validator PASS is not itself a Prover proof.

## Two withheld report-result attributions

- Example 7: The published bitmap-uniqueness proposition has a checkmark, but the executable source implication is a tautology and cannot detect a duplicate; neither the exact historical proof run nor this body-to-report identity is established. Original result for this source is NOT_STATED.

- Example 39: The PDF marks the general settlement-rates-never-reset proposition verified; the active CVL asserts a different, contradictory zero-prestate implication, so the original checkmark cannot be propagated as the result of this exact formula. Original result for this source is NOT_STATED.

## Additional variant-semantic correction

Example 57 (oldAccountContext.spec) is also tautological. The label is UNMAPPED, consistent with the source-level weakness in Example 7, but no formal result or target context is propagated between the two instances.
