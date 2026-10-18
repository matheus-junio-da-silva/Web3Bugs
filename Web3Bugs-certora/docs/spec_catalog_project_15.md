# HELIX — Project 15 / AAVE GHO Core

## Provenance verified against reviewed commit

- Archived source: PropertyGPT/certora_projects/gho-core at Git commit 687f654c679ed45ab127b7949e2a29c8f5e491b9
- Historic Certora reviewed commit (aave/gho-core): ce49fb0c94cfebf0159222ceb288e4f9a55d305f
- All 22 archived Solidity Git blobs are identical to that reviewed commit.
- Eight of nine CVL spec blobs match exactly. The exception ghoDiscountRateStrategy.spec is shortened;
  its only surviving active rule limitOnDiscountRate is literally identical to the reviewed version.
- Report publication: March 7, 2023; review work January 30 – February 28, 2023.
- PDF direct official provenance: https://certora.cdn.prismic.io/certora/a227c693-7aa3-471f-a7b2-7148c06a2110_Aave_Gho_Formal_Verification_Report.pdf
- PDF SHA256: ced8ba5de87ae727c0df889d5e916f32a759394465acf1ce83b1afddf832df06
- Original report preserved at resources/15/Aave_Gho_Formal_Verification_Report.pdf.
- PDF transcript at reports/15.md is non-authoritative for visual glyphs; original PDF is canonical.

## Inventory and result boundaries

- Exactly 116 source declarations: VariableDebtToken 22, flashMinter 6, ghoAToken 7, ghoDiscountRateStrategy 1, ghoToken 28, ghoVariableDebtToken 25, set 27.
- erc20.spec and summarizations.spec are helper imports with zero active properties.
- All 116 instances are conservatively incomplete owing to unresolved source-era Solidity dependencies, historical mocks and original Prover config; each example records its specific context. CVL syntax migration is not the reason.
- Exact-target report VERIFIED attributions: 64
- Explicit NOT_STATED: 52 (including diagnostics, generic imported specs and rules without individual report evidence).
- Violated active source instances: 0. The report's violated timelock property is not an active source declaration.
- Detection Outcome NO_FINDING follows only individually verified properties without an attributed named finding.
- New spec index relationship rows: 116, strictly additive. No new bugs.csv row; four report findings preserved separately, not guessed from matching themes.

## Individual report/source mismatches

- onlyRebalanceCanUpdateUserDiscountRate: VIOLATED in PDF, absent from archived active CVL.
- integrityOfMint_cantDecreaseInterestWithMint: TIMEOUT in PDF, absent from archived active CVL.
- integrityOfUpdateDiscountDistribution_discountRate: VERIFIED in PDF, absent from archived active CVL.
- OnlyFacilitatorManagerAlterFacilitatorExistence: VERIFIED in PDF, absent from archived active CVL.
- OnlyBucketManagerCanChangeCapacity: VERIFIED in PDF, absent from archived active CVL.

## Semantic/verification assumptions

- The report assumes Aave V3 Pool correctness; setter-initialized references exist when checked.
- It bounds loop unrolling to two iterations and assumes token amounts WAD, normalized index RAY and rate BPS.
- Both imported set.spec and VariableDebtToken.spec contain many executable rules absent from the PDF's per-contract table. Those remain NOT_STATED rather than receiving generic reported status.
- Diagnostic cover_len rules and should_fail probes carry UNMAPPED instead of fabricated security labels.
- The report lists a Low-severity rebalance timelock bypass under onlyRebalanceCanUpdateUserDiscountRate; after a removal commit it is no longer a true invariant, but that rule is not active in the source snapshot.
- The report also documents Low maxFlashLoan/EIP3156 compliance, Low accumulated interest effects and an Informational WadRayMath convention. These report findings are distinct from Result/Detection Outcome in extracted CVL.
- The published report mentions additional rules absent in PropertyGPT's reduced discount spec; do not add them to this snapshot.
- Historical Solidity and CVL sources were preserved byte-for-byte, not replaced by current deployed contracts.

## Coverage matrix

| ID | Archived spec | Property | Target | Result | Bug Label |
| ---: | --- | --- | --- | --- | --- |
| 1 | VariableDebtToken.spec | totalSupplyEqualsSumAllBalance | GhoVariableDebtToken | NOT_STATED | S6-4 |
| 2 | VariableDebtToken.spec | whoChangeTotalSupply | GhoVariableDebtToken | NOT_STATED | UNMAPPED |
| 3 | VariableDebtToken.spec | balanceOfChange | GhoVariableDebtToken | NOT_STATED | UNMAPPED |
| 4 | VariableDebtToken.spec | balanceOfAtMost3Change | GhoVariableDebtToken | NOT_STATED | S6-4 |
| 5 | VariableDebtToken.spec | nonceChangePermits | GhoVariableDebtToken | NOT_STATED | UNMAPPED |
| 6 | VariableDebtToken.spec | inverseMintBurn | GhoVariableDebtToken | NOT_STATED | S2-3 |
| 7 | VariableDebtToken.spec | integrityDelegationWithSig | GhoVariableDebtToken | NOT_STATED | UNMAPPED |
| 8 | VariableDebtToken.spec | integrityOfBurn | GhoVariableDebtToken | NOT_STATED | S6-4 |
| 9 | VariableDebtToken.spec | integrityOfBurn_exact_suply_should_fail | GhoVariableDebtToken | NOT_STATED | UNMAPPED |
| 10 | VariableDebtToken.spec | integrityOfBurn_exact_balance_should_fail | GhoVariableDebtToken | NOT_STATED | UNMAPPED |
| 11 | VariableDebtToken.spec | additiveBurn | GhoVariableDebtToken | NOT_STATED | S6-4 |
| 12 | VariableDebtToken.spec | additiveBurn_should_fail | GhoVariableDebtToken | NOT_STATED | UNMAPPED |
| 13 | VariableDebtToken.spec | additiveMint | GhoVariableDebtToken | NOT_STATED | S6-4 |
| 14 | VariableDebtToken.spec | additiveMint_excact_should_fail | GhoVariableDebtToken | NOT_STATED | UNMAPPED |
| 15 | VariableDebtToken.spec | integrityMint | GhoVariableDebtToken | NOT_STATED | S6-4 |
| 16 | VariableDebtToken.spec | integrityMint_underlying | GhoVariableDebtToken | NOT_STATED | S6-4 |
| 17 | VariableDebtToken.spec | integrityMint_atoken | GhoVariableDebtToken | NOT_STATED | S6-4 |
| 18 | VariableDebtToken.spec | integrityMint_exact_should_fail | GhoVariableDebtToken | NOT_STATED | UNMAPPED |
| 19 | VariableDebtToken.spec | burnZeroDoesntChangeBalance | GhoVariableDebtToken | VERIFIED | S6-4 |
| 20 | VariableDebtToken.spec | burnNoChangeToOther | GhoVariableDebtToken | NOT_STATED | S6-4 |
| 21 | VariableDebtToken.spec | mintNoChangeToOther | GhoVariableDebtToken | NOT_STATED | S6-4 |
| 22 | VariableDebtToken.spec | disallowedFunctionalities | GhoVariableDebtToken | VERIFIED | S5-2 |
| 23 | flashMinter.spec | balanceOfFlashMinterGrows | GhoFlashMinter | VERIFIED | S6-4 |
| 24 | flashMinter.spec | integrityOfTreasurySet | GhoFlashMinter | VERIFIED | S3-2 |
| 25 | flashMinter.spec | integrityOfFeeSet | GhoFlashMinter | VERIFIED | S3-2 |
| 26 | flashMinter.spec | availableLiquidityDoesntChange | GhoFlashMinter | VERIFIED | S6-4 |
| 27 | flashMinter.spec | integrityOfDistributeFeesToTreasury | GhoFlashMinter | VERIFIED | S6-4 |
| 28 | flashMinter.spec | feeSimulationEqualsActualFee | GhoFlashMinter | VERIFIED | S6-4 |
| 29 | ghoAToken.spec | noMint | GhoAToken | VERIFIED | S5-2 |
| 30 | ghoAToken.spec | noBurn | GhoAToken | VERIFIED | S5-2 |
| 31 | ghoAToken.spec | noTransfer | GhoAToken | VERIFIED | S5-2 |
| 32 | ghoAToken.spec | transferUnderlyingToCantExceedCapacity | GhoAToken | VERIFIED | S6-4 |
| 33 | ghoAToken.spec | totalSupplyAlwaysZero | GhoAToken | VERIFIED | S6-4 |
| 34 | ghoAToken.spec | userBalanceAlwaysZero | GhoAToken | VERIFIED | S6-4 |
| 35 | ghoAToken.spec | level_does_not_decrease_after_transferUnderlyingTo_followed_by_handleRepayment | GhoAToken | VERIFIED | S6-4 |
| 36 | ghoDiscountRateStrategy.spec | limitOnDiscountRate | GhoDiscountRateStrategy | VERIFIED | S6-2 |
| 37 | ghoToken.spec | length_leq_max_uint160 | GhoToken | VERIFIED | UNMAPPED |
| 38 | ghoToken.spec | inv_balanceOf_leq_totalSupply | GhoToken | VERIFIED | S6-4 |
| 39 | ghoToken.spec | total_supply_eq_sumAllLevel | GhoToken | VERIFIED | S6-4 |
| 40 | ghoToken.spec | sumAllBalance_eq_totalSupply | GhoToken | VERIFIED | S6-4 |
| 41 | ghoToken.spec | sumAllLevel_eq_sumAllBalance | GhoToken | VERIFIED | S6-4 |
| 42 | ghoToken.spec | inv_valid_capacity | GhoToken | VERIFIED | S6-4 |
| 43 | ghoToken.spec | inv_valid_level | GhoToken | VERIFIED | S6-4 |
| 44 | ghoToken.spec | address_in_set_values_iff_in_set_indexes | GhoToken | VERIFIED | S2-3 |
| 45 | ghoToken.spec | addr_in_set_iff_in_map | GhoToken | VERIFIED | S2-3 |
| 46 | ghoToken.spec | addr_in_set_list_iff_in_map | GhoToken | NOT_STATED | S2-3 |
| 47 | ghoToken.spec | level_leq_capacity | GhoToken | VERIFIED | S6-4 |
| 48 | ghoToken.spec | mint_after_burn | GhoToken | VERIFIED | S6-4 |
| 49 | ghoToken.spec | burn_after_mint | GhoToken | VERIFIED | S6-4 |
| 50 | ghoToken.spec | level_unchanged_after_mint_followed_by_burn | GhoToken | VERIFIED | S6-4 |
| 51 | ghoToken.spec | level_after_mint | GhoToken | VERIFIED | S6-4 |
| 52 | ghoToken.spec | level_after_burn | GhoToken | VERIFIED | S6-4 |
| 53 | ghoToken.spec | facilitator_in_list_after_setFacilitatorBucketCapacity | GhoToken | VERIFIED | S3-2 |
| 54 | ghoToken.spec | getFacilitatorBucketCapacity_after_setFacilitatorBucketCapacity | GhoToken | VERIFIED | S3-2 |
| 55 | ghoToken.spec | facilitator_in_list_after_addFacilitator | GhoToken | VERIFIED | UNMAPPED |
| 56 | ghoToken.spec | facilitator_in_list_after_mint_and_burn | GhoToken | VERIFIED | S6-4 |
| 57 | ghoToken.spec | address_not_in_list_after_removeFacilitator | GhoToken | VERIFIED | S2-3 |
| 58 | ghoToken.spec | balance_after_mint | GhoToken | VERIFIED | S6-4 |
| 59 | ghoToken.spec | balance_after_burn | GhoToken | VERIFIED | S6-4 |
| 60 | ghoToken.spec | mintLimitedByFacilitatorRemainingCapacity | GhoToken | VERIFIED | S3-2 |
| 61 | ghoToken.spec | burnLimitedByFacilitatorLevel | GhoToken | VERIFIED | S3-2 |
| 62 | ghoToken.spec | ARRAY_IS_INVERSE_OF_MAP_Invariant | GhoToken | NOT_STATED | S2-3 |
| 63 | ghoToken.spec | addressSetInvariant | GhoToken | NOT_STATED | S2-3 |
| 64 | ghoToken.spec | address_not_in_list_after_removeFacilitator_CASE_SPLIT_zero_address | GhoToken | NOT_STATED | S2-3 |
| 65 | ghoVariableDebtToken.spec | discountCantExceed100Percent | GhoVariableDebtToken | VERIFIED | S6-4 |
| 66 | ghoVariableDebtToken.spec | nonMintFunctionCantIncreaseBalance | GhoVariableDebtToken | VERIFIED | S6-4 |
| 67 | ghoVariableDebtToken.spec | nonMintFunctionCantIncreaseScaledBalance | GhoVariableDebtToken | VERIFIED | S6-4 |
| 68 | ghoVariableDebtToken.spec | debtTokenIsNotTransferable | GhoVariableDebtToken | VERIFIED | S5-2 |
| 69 | ghoVariableDebtToken.spec | onlyCertainFunctionsCanModifyScaledBalance | GhoVariableDebtToken | VERIFIED | S6-4 |
| 70 | ghoVariableDebtToken.spec | userAccumulatedDebtInterestWontDecrease | GhoVariableDebtToken | VERIFIED | S6-4 |
| 71 | ghoVariableDebtToken.spec | userCantNullifyItsDebt | GhoVariableDebtToken | VERIFIED | S6-4 |
| 72 | ghoVariableDebtToken.spec | integrityOfMint_updateDiscountRate | GhoVariableDebtToken | VERIFIED | S3-2 |
| 73 | ghoVariableDebtToken.spec | integrityOfMint_updateIndex | GhoVariableDebtToken | VERIFIED | S3-2 |
| 74 | ghoVariableDebtToken.spec | integrityOfMint_updateScaledBalance_fixedIndex | GhoVariableDebtToken | NOT_STATED | S6-4 |
| 75 | ghoVariableDebtToken.spec | integrityOfMint_userIsolation | GhoVariableDebtToken | VERIFIED | S6-4 |
| 76 | ghoVariableDebtToken.spec | onlyMintForUserCanIncreaseUsersBalance | GhoVariableDebtToken | VERIFIED | S6-4 |
| 77 | ghoVariableDebtToken.spec | integrityOfBurn_updateDiscountRate | GhoVariableDebtToken | VERIFIED | S3-2 |
| 78 | ghoVariableDebtToken.spec | integrityOfBurn_updateIndex | GhoVariableDebtToken | VERIFIED | S3-2 |
| 79 | ghoVariableDebtToken.spec | integrityOfBurn_fixedIndex | GhoVariableDebtToken | VERIFIED | S6-4 |
| 80 | ghoVariableDebtToken.spec | integrityOfBurn_fullRepay_concrete | GhoVariableDebtToken | VERIFIED | S6-4 |
| 81 | ghoVariableDebtToken.spec | integrityOfBurn_userIsolation | GhoVariableDebtToken | VERIFIED | S6-4 |
| 82 | ghoVariableDebtToken.spec | integrityOfUpdateDiscountDistribution_updateIndex | GhoVariableDebtToken | VERIFIED | S3-2 |
| 83 | ghoVariableDebtToken.spec | integrityOfUpdateDiscountDistribution_userIsolation | GhoVariableDebtToken | VERIFIED | S6-4 |
| 84 | ghoVariableDebtToken.spec | integrityOfRebalanceUserDiscountPercent_updateDiscountRate | GhoVariableDebtToken | VERIFIED | S3-2 |
| 85 | ghoVariableDebtToken.spec | integrityOfRebalanceUserDiscountPercent_updateIndex | GhoVariableDebtToken | VERIFIED | S3-2 |
| 86 | ghoVariableDebtToken.spec | integrityOfRebalanceUserDiscountPercent_userIsolation | GhoVariableDebtToken | VERIFIED | S6-4 |
| 87 | ghoVariableDebtToken.spec | integrityOfBalanceOf_fullDiscount | GhoVariableDebtToken | VERIFIED | S6-4 |
| 88 | ghoVariableDebtToken.spec | integrityOfBalanceOf_noDiscount | GhoVariableDebtToken | VERIFIED | S6-4 |
| 89 | ghoVariableDebtToken.spec | integrityOfBalanceOf_zeroScaledBalance | GhoVariableDebtToken | VERIFIED | S6-4 |
| 90 | set.spec | setInvariant | GhoToken | NOT_STATED | UNMAPPED |
| 91 | set.spec | addressSetInvariant | GhoToken | NOT_STATED | S2-3 |
| 92 | set.spec | api_add_succeeded | GhoToken | NOT_STATED | S2-3 |
| 93 | set.spec | api_add_failed_contains | GhoToken | NOT_STATED | S2-3 |
| 94 | set.spec | api_add_failed_at | GhoToken | NOT_STATED | S2-3 |
| 95 | set.spec | api_address_contained_after_add | GhoToken | NOT_STATED | S2-3 |
| 96 | set.spec | api_remove_succeeded_contains | GhoToken | NOT_STATED | S2-3 |
| 97 | set.spec | api_remove_failed | GhoToken | NOT_STATED | S2-3 |
| 98 | set.spec | api_remove_succeeded_at | GhoToken | NOT_STATED | S2-3 |
| 99 | set.spec | api_not_contains_after_remove | GhoToken | NOT_STATED | S2-3 |
| 100 | set.spec | cover_at_contains | GhoToken | NOT_STATED | UNMAPPED |
| 101 | set.spec | cover_len0 | GhoToken | NOT_STATED | UNMAPPED |
| 102 | set.spec | cover_len1 | GhoToken | NOT_STATED | UNMAPPED |
| 103 | set.spec | cover_len2 | GhoToken | NOT_STATED | UNMAPPED |
| 104 | set.spec | cover_len3 | GhoToken | NOT_STATED | UNMAPPED |
| 105 | set.spec | cover_len4 | GhoToken | NOT_STATED | UNMAPPED |
| 106 | set.spec | cover_len5 | GhoToken | NOT_STATED | UNMAPPED |
| 107 | set.spec | cover_len6 | GhoToken | NOT_STATED | UNMAPPED |
| 108 | set.spec | cover_len7 | GhoToken | NOT_STATED | UNMAPPED |
| 109 | set.spec | cover_len8 | GhoToken | NOT_STATED | UNMAPPED |
| 110 | set.spec | cover_len16 | GhoToken | NOT_STATED | UNMAPPED |
| 111 | set.spec | cover_len32 | GhoToken | NOT_STATED | UNMAPPED |
| 112 | set.spec | cover_len64 | GhoToken | NOT_STATED | UNMAPPED |
| 113 | set.spec | cover_len128 | GhoToken | NOT_STATED | UNMAPPED |
| 114 | set.spec | cover_len256 | GhoToken | NOT_STATED | UNMAPPED |
| 115 | set.spec | cover_len512 | GhoToken | NOT_STATED | UNMAPPED |
| 116 | set.spec | cover_len1024 | GhoToken | NOT_STATED | UNMAPPED |

## Required reproducible checks

- python scripts/check_specs.py . (in Web3Bugs-certora)
- python scripts/check_contests_csv.py . (in Web3Bugs-certora)
- python scripts/check_contracts.py . (in Web3Bugs-certora)
- git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD (Git root)
- Structural PASS does not mean Certora Prover was rerun. CI logs supply actual exit codes and checkout SHA.
- Local ZIP inspection could not run because the supplied local Python/container infrastructure failed; a real GitHub Actions checkout is used instead.
