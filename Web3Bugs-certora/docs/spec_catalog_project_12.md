# Project 12 — AAVE V2 (Ceres): preliminary source inventory

> **Status: IN PROGRESS — NOT A COMPLETED CATALOG.** This document does not claim that property/result mappings or validator checks are complete.

## Project ID collision and assignment

Project ID 6 is already allocated on `main` to **Aave Static aToken** (existing `contracts/6/`, `reports/6.md`, `resources/6/` and 32 catalog examples). AAVE V2 therefore uses **Project ID 12** to avoid overwriting evidence. IDs 7–11 have been described as assignments for other agents. Source project remains `PropertyGPT/certora_projects/aave_v2/`.

## Source-level property inventory (26)

- `specs/StableDebtToken.spec` — **9 rules**: `integrityTimeStamp` (lines 5–12), `balanceOfChange` (21–36), `integirtyBalanceOfTotalSupply` (42–56), `integirtyBalanceOfTotalSupplyOnBurn` (62–101), `integrityMint` (106–116), `additiveMint` (126–142), `integrityBurn` (144–153), `additiveBurn` (155–167), `inverseMintBurn` (174–184).
- `specs/UserConfiguration.spec` — **4 invariants**: `empty` (11–12), `notEmpty` (14–15), `borrowing` (18–19), `collateralOrBorrowing` (21–22); **4 rules**: `setBorrowing` (26–32), `setBorrowingNoChangeToOther` (34–44), `setUsingAsCollateral` (47–53), `setUsingAsCollateralNoChangeToOther` (56–66).
- `specs/VariableDebtToken.spec` — **9 rules**: `balanceOfChange` (6–20), `integirtyBalanceOfTotalSupply` (26–41), `integirtyBalanceOfTotalSupplyOnBurn` (46–60), `integirtyBalanceOfTotalSupplyOnMint` (65–79), `integrityMint` (90–102), `additiveMint` (108–121), `integrityBurn` (129–138), `additiveBurn` (143–156), `inverseMintBurn` (164–174).

The historical spelling `integirty` is preserved. The identically named rules of StableDebtToken and VariableDebtToken are separate instances with potentially different semantics and outcomes.

## Known harnesses

- `specs/harness/StableDebtTokenHarness.sol`: replaces `balanceOf` and `_calcTotalSupply` with simplified forms that **do not accrue interest** (lines 15–24); adds `getIncentivesController` (26–28) and `rayWadMul` (30–32). Its semantics limit the strength of accounting claims.
- `specs/harness/UserConfigurationHarness.sol`: public wrappers (15–41) for library functions of `UserConfiguration`. The `init_state()` wrapper (46) has an empty body.
- `specs/harness/LendingPoolHarnessForVariableDebtToken.sol`: wraps the lending pool and uses a special `getReserveNormalizedVariableDebt` requiring the timestamp-indexed mapping equal `1e27` (157–167).

## Semantic observations requiring review

- StableDebtToken `additiveMint` explicitly assumes a **zero user stable rate** (source lines 122–130). Do not generalize to all rates.
- Both token specs assert balance-change conservation using before/after subtraction, requiring careful treatment of arithmetic underflow and environmental assumptions.
- `VariableDebtToken.spec` explicitly binds `LendingPoolHarnessForVariableDebtToken as POOL` (line 1); follow this binding rather than treating the normalization index as an unconstrained standard pool implementation.
- The `UserConfiguration` rules use `reserveIndex < 128` whereas invariants do not include the same visible range precondition; assess reachability separately.
- Do not assign `VERIFIED`, `VIOLATED`, `FINDING`, `NO_FINDING`, or Web3Bugs labels without an individual report/code-level confirmation.

## Provenance and unresolved tasks

Source: https://github.com/matheus-junio-da-silva/PropertyGPT/tree/main/certora_projects/aave_v2

Report source: `certora_projects/aave_v2/AaveV2Dec2020.pdf` (Git blob SHA `705d0961134f5a0b9d48c15723a5cde367c7e003`; **not yet transcribed or copied**). Source specs have Git blob SHA-1s `a486d335352d73d4d81495447d29be20b9916e31`, `41a4f93e1323157efb5411cb72ebeb7a5d60f68a`, and `eb19d1b4f435b67d52f2486fd99335d173883d1b`, respectively.

Still required: immutable copy and byte-identity audit of the entire source snapshot; full report reading and faithful report preservation; one extracted source/solidity/documentation triple for each of 26 source properties; individual dependency closure, Bug Label, result and outcome evidence; index updates; checks `check_specs.py`, `check_contests_csv.py`, `check_contracts.py`, and `git diff --check`. **None of these checks have been executed; no evidence of PASS is claimed.**

**No PR should be opened as a completed catalog until these are resolved.**
