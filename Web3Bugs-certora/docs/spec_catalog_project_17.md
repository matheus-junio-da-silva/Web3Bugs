# Project 17 — Compound Money Market V2
Source: matheus-junio-da-silva/PropertyGPT, certora_projects/compound_moneymarket.
Snapshot source SHA: 687f654c679ed45ab127b7949e2a29c8f5e491b9.
PDF SHA-256: cb48b1c159df4ef3d603f84afc2e7fa9da6c2c0b72f9760e6d962807f4177a1a.

Legacy Specify: exactly 41 executable top-level property blocks; alias .spclnk entries are configurations, not properties.
Historical report gives aggregate assurances; source blocks are never treated as newly proved.

## Per-property reconstruction

Distribution: {'incomplete': 27, 'complete': 14}. Historical outcomes: {'NOT_STATED': 32, 'VERIFIED': 9}.


| # | CVL declaration | Property | Status | Label | Result | Provenance/dependency note |
|---:|---|---|---|---|---|---|
| 1 | compound.cvl:38-70 | _setOriginationFee | incomplete | S5-3 | NOT_STATED | The historical V1 MoneyMarket contract with supply(address,uint256), withdraw(address,uint256), _setOriginationFee, _set |
| 2 | compound.cvl:72-104 | _setPendingAdmin | incomplete | S5-3 | NOT_STATED | The historical V1 MoneyMarket contract with supply(address,uint256), withdraw(address,uint256), _setOriginationFee, _set |
| 3 | compound.cvl:106-147 | _acceptAdmin | incomplete | S5-3 | NOT_STATED | The historical V1 MoneyMarket contract with supply(address,uint256), withdraw(address,uint256), _setOriginationFee, _set |
| 4 | compound.cvl:150-186 | invariantRequireAdminToChangeAdmin | incomplete | S5-3 | NOT_STATED | The historical V1 MoneyMarket contract with supply(address,uint256), withdraw(address,uint256), _setOriginationFee, _set |
| 5 | compound.cvl:188-233 | _setOracle | incomplete | S5-3 | NOT_STATED | The historical V1 MoneyMarket contract with supply(address,uint256), withdraw(address,uint256), _setOriginationFee, _set |
| 6 | compound.cvl:235-266 | _setMaxAssets | incomplete | S5-3 | NOT_STATED | The historical V1 MoneyMarket contract with supply(address,uint256), withdraw(address,uint256), _setOriginationFee, _set |
| 7 | accrueInterest.cvl:12-77 | accrueInterest | incomplete | S6-3 | VERIFIED | The synthetic interestRateModelGetBorrowRate() wrapper declared in CVL is absent from the CToken/CErc20Certora ABI. The  |
| 8 | borrowAndRepayFresh.cvl:20-122 | borrowFresh | complete | S6-4 | VERIFIED | All called method selectors located in project snapshot |
| 9 | borrowAndRepayFresh.cvl:124-257 | repayBorrowFresh | complete | S6-4 | VERIFIED | All called method selectors located in project snapshot |
| 10 | mintAndRedeemFresh.cvl:30-147 | mintFresh | complete | S6-4 | VERIFIED | All called method selectors located in project snapshot |
| 11 | mintAndRedeemFresh.cvl:149-271 | mintFresh_extended | complete | S6-4 | NOT_STATED | All called method selectors located in project snapshot |
| 12 | mintAndRedeemFresh.cvl:274-400 | redeemFresh | complete | S6-4 | VERIFIED | All called method selectors located in project snapshot |
| 13 | mintAndRedeemFresh.cvl:402-423 | mintThenRedeem | complete | S6-4 | NOT_STATED | All called method selectors located in project snapshot |
| 14 | liquidateFresh.cvl:25-219 | liquidateBorrowFresh | complete | S6-4 | VERIFIED | All called method selectors located in project snapshot |
| 15 | liquidateFresh.cvl:221-331 | seize | complete | S6-4 | VERIFIED | All called method selectors located in project snapshot |
| 16 | admin_setCollateralFactor.cvl:11-101 | _setCollateralFactor | incomplete | S5-3 | NOT_STATED | getCollateralFactorREMOVE_ME(address) and getMarketListedREMOVE_ME(address) are CVL workarounds for struct getters witho |
| 17 | _setMarketPriceOracle.cvl:7-63 | _setMarketPriceOracle | incomplete | S5-3 | NOT_STATED | The historical _setMarketPriceOracle(address,address) entrypoint is absent; Comptroller._setPriceOracle(PriceOracle) is  |
| 18 | general.cvl:12-44 | _setPendingAdmin | complete | S5-3 | NOT_STATED | All called method selectors located in project snapshot |
| 19 | general.cvl:46-87 | _acceptAdmin | complete | S5-3 | NOT_STATED | All called method selectors located in project snapshot |
| 20 | general.cvl:90-126 | invariantRequireAdminToChangeAdmin | complete | S5-3 | NOT_STATED | All called method selectors located in project snapshot |
| 21 | general.cvl:128-167 | _setComptroller | complete | S5-3 | NOT_STATED | All called method selectors located in project snapshot |
| 22 | frame.cvl:70-85 | frame_balanceOf | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 23 | frame.cvl:87-102 | frame_borrowBalanceStored | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 24 | frame.cvl:104-119 | frame_borrowIndex | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 25 | frame.cvl:121-136 | frame_borrowRatePerBlock | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 26 | frame.cvl:138-153 | frame_comptroller | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 27 | frame.cvl:155-170 | frame_exchangeRateStored | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 28 | frame.cvl:172-189 | frame_getAccountSnapshot | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 29 | frame.cvl:191-206 | frame_getCash | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 30 | frame.cvl:208-223 | frame_initialExchangeRateMantissa | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 31 | frame.cvl:225-240 | frame_interestRateModel | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 32 | frame.cvl:242-257 | frame_isCToken | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 33 | frame.cvl:259-274 | frame_pendingAdmin | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 34 | frame.cvl:276-291 | frame_reserveFactorMantissa | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 35 | frame.cvl:293-308 | frame_supplyRatePerBlock | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 36 | frame.cvl:310-325 | frame_totalBorrows | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 37 | frame.cvl:327-342 | frame_totalReserves | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 38 | frame.cvl:344-359 | frame_totalSupply | incomplete | UNMAPPED | NOT_STATED | CVL-called methods lack an implementation in the declared target and its included snapshot ABI: f. |
| 39 | eip20.cvl:18-154 | transferFrom | complete | S6-4 | VERIFIED | All called method selectors located in project snapshot |
| 40 | _setMarketPolicyHook.cvl:7-72 | _setMarketPolicyHook | incomplete | S5-3 | NOT_STATED | The historical _setMarketPolicyHook(address,address) and policyHook field of the asserted market tuple are missing from  |
| 41 | maximillion.cvl:8-33 | repayBehalf | complete | S6-4 | VERIFIED | All called method selectors located in project snapshot |

## Snapshot preservation & second-review method

The source's contracts/, spec/formal/, scenario/ and .spclnk files are copied unchanged. Every extracted property block is asserted literally present in its N.spec; CVL method signatures come from the original methods block. This program independently recounts the same 41 top-level declarations and checks each assertion and copied literal block. Dynamic method f and historically absent helpers are never fabricated.

## PDF limitations and findings

The report summary pages 2–3 claim correctness for specified operations, under modular proof, synthetic Comptroller assumptions and ERC20 modeling. Earlier bugs fixed before release include zero-output exchange rounding, role constraints, false-return ERC20 assumptions and the Maximillion stored/current interest mistake. Those historical findings are not assigned mechanically to any individual CSV result or outcome. Appendix sources may differ from V2 snapshot or be named generically; see each example.

## Configurations and exclusions

Five .spclnk files configure linked external contracts and targets; they do not introduce additional named properties. The dummy.cvl file has zero rules. .scen files and .scen.old are execution scenarios, not active CVL rule declarations. compound.cvl is preserved despite historical V1 ABI incompatibility; frame.cvl probes are included despite being diagnostic rather than normative.

## Reproduction

Run the generator against the SHA-pinned PropertyGPT source with poppler-utils; then from Web3Bugs-certora execute python3 scripts/check_contracts.py ., python3 scripts/check_contests_csv.py ., python3 scripts/check_specs.py . and repository-root git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD. No Certora prover rerun is asserted.
