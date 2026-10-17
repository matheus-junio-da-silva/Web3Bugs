# Project 12 — AAVE Protocol V2 (Ceres) spec catalog

## Scope and Project ID exclusivity

Project ID 6 is already occupied by the unrelated **Aave Static aToken** and has not been changed. This catalog uses **Project ID 12** exclusively. Source: https://github.com/matheus-junio-da-silva/PropertyGPT/tree/main/certora_projects/aave_v2. Branch: `catalog/p12-ceres-aave-v2`. Initial commit: `a073d5fd075a9544401f723a11fde959098fca5c`.

## Coverage and classification

| Original spec | Active rules | Active invariants | Complete | Incomplete |
|---|---:|---:|---:|---:|
| `StableDebtToken.spec` | 9 | 0 | 9 | 0 |
| `VariableDebtToken.spec` | 9 | 0 | 9 | 0 |
| `UserConfiguration.spec` | 4 | 4 | 8 | 0 |
| **Total** | **22** | **4** | **26** | **0** |

All 26 active property instances have dedicated `.spec`, `.sol`, `.md` under `results/spec/complete/12/` (78 artifact files). The CSV contains **26 rows for 26 unique examples**, with no multi-label duplications. This is a **source snapshot dependency closure**, not proof that historical CVL will compile under CVL2 or that historical verification settings are available. There are zero `incomplete/12/` examples and consequently no `N.txt` files: missing run configurations alone do not justify `incomplete`.

Formal Result, **per source instance**, from `reports/12.md` and the preserved original PDF:
- VERIFIED: 21 (7 StableDebtToken; 6 VariableDebtToken; 8 UserConfiguration).
- VIOLATED: 0 (no explicit violated result for the final current source instances).
- NOT_STATED: 5 (2 StableDebtToken and 3 VariableDebtToken source supply-consistency variants absent as individually named report entries).

Detection Outcome: FINDING **1**, NO_FINDING **20**, ACCEPTED_BEHAVIOR **0**, INCONCLUSIVE **0**, NOT_STATED **5**. `FINDING` for StableDebtToken `additiveMint` records a **historical** medium rounding issue named in the report while the latest simplified report table says `✔*`. No other report finding is assigned to a source rule without individual evidence. `results/bugs.csv` adds just AV2-01 (L2) for that documented issue; unlinked/aggregate issues remain described in the report instead of being force-linked to source examples.

| Bug Label | Examples | Semantics |
|---|---:|---|
| S3-2 | 7 | timestamp, balance noninterference, bitmap flag updates |
| S6-4 | 12 | mint/burn supply and balance conservation, inverse behavior |
| S6-2 | 4 | cross-getter bitmap consistency |
| L2 | 3 | additivity sensitive to ray rounding |
| UNMAPPED | 0 | All selected properties encode a normative postcondition or getter equivalence |

## Dependency closure and target resolution

- **StableDebtToken (examples 1–9)** targets `StableDebtTokenHarness` inheriting `StableDebtToken`, not `VariableDebtToken`. The harness implements `getIncentivesController` and `rayWadMul` and overrides `balanceOf` and `_calcTotalSupply` to use principal, non-interest-accruing totals (harness lines 15–32). `getUserLastUpdated` uses an original `methods` declaration from `StableDebtToken.spec` lines 1–3 and an actual Solidity getter in `StableDebtToken.sol` lines 89–91. Other calls are implemented in the target/base source. No missing CVL definition/import/ghost/hook was identified. However, the historical harness's getter may conflict with some modern Solidity inherited API/override expectations; its present source does not imply historical rebuild success.
- **VariableDebtToken (examples 10–18)** targets `VariableDebtToken` and uses the original `using LendingPoolHarnessForVariableDebtToken as POOL` where the rule calls POOL (source line 1). The harness's `getReserveNormalizedVariableDebt` reads a timestamp-keyed private mapping, requires the entry to equal `1e27`, and returns it (lines 157–167). The target's `mint`, `burn`, `balanceOf`, and `totalSupply` are implemented in `VariableDebtToken.sol` (lines 75–152), with scaled storage in `IncentivizedERC20.sol`. No historical link configuration is supplied; possible unreachable paths/vacuity are **not** disproved by structural closure.
- **UserConfiguration (examples 19–26)** targets `UserConfigurationHarness`, which wraps `UserConfiguration` library methods and owns one `DataTypes.UserConfigurationMap`. Required original `methods` declarations were copied selectively into each extracted spec; a declaration was not mistaken for a Solidity implementation. The bitmap library implementation and struct appear in the complete source snapshot.

CVL built-ins such as `env`, `sinvoke`, `storage`, `lastStorage`, `calldataarg`, and symbolic `method` arguments are not counted as missing project helpers. The three original specs contain **no active imports, definitions, ghosts, hooks, or rules outside the 26 listed instances**. There are 3 actual historical harness source files. Source does not include historical `.conf` scripts or replay flags; exact prover reproduction is not claimed.

## Report/source status separation and limitations

Report: `reports/12.md` (structured report-section transcription) and byte-identical `resources/12/AaveV2Dec2020.pdf` (25 pages; complete authoritative original). The source report describes verification from 2020-08-02 to 2020-10-29 and latest commit `750920303e33b66bc29862ea3b85206dda9ce786`. It defines `✔` as latest-commit verified, and `✔*` as verified **on simplified code that ignores rounding errors**. Every selected StableDebtToken and VariableDebtToken report property has the `✔*` qualifier; UserConfiguration entries #26–#30 have plain `✔`. The `✔*` label does **not** certify exact behavior of all integer rounding/index values.

- **Aggregate-versus-individual:** StableDebtToken #10 aggregate is stated as proved by report #11–#12. Source `integirtyBalanceOfTotalSupply` and `integirtyBalanceOfTotalSupplyOnBurn` split #12's concept. Neither has separate explicit report outcome; both `NOT_STATED`. VariableDebtToken #18 aggregate uses #19–#20 but the source splits #20 into generic, mint and burn rules; all three remain `NOT_STATED`. This does not deny the aggregate proof, only prevents unsupported allocation to exact source rules.
- **Historical medium issue:** `additiveMint` StableDebtToken is individually associated with report's medium additive-mint rounding issue. The source specifically assumes `getUserStableRate(a)==0` and the harness removes interest. Thus latest ✔* and historical finding are not a logical contradiction.
- **Report typo:** UserConfiguration report #29 prints `isBorrowing(u,r)=b` after setUsingAsCollateral, while the source assertion demands `isUsingAsCollateral(r)=b`. The original source is preserved; no silent repair.
- **Variable debt #24 typo:** The report titles it additivity of burn but a prose sentence calls it minting. Source executes only burn, which controls mapping.
- **Stable argument interpretation:** In the source `mint(...,index)` the fourth symbolic argument called `index` is **the Solidity stable rate**, not a normalized variable debt index; the extracted CVL spelling is retained without correction.
- **Conservation arithmetic:** Stable and Variable generic supply-consistency rules use subtraction of before and after values whose domain/underflow assumptions are not explicit. The Stable burn rule has special zero-supply cases. Do not paraphrase these as an unrestricted mathematical identity.
- **Index bounds:** UserConfiguration setter rules constrain `reserveIndex<128` and noninterference constrains both indices. The four getter invariants do **not** explicitly assume the bound, though Solidity library getters require it, limiting what the proof status can be interpreted to cover.
- **Partiality:** `balanceOfChange` in both tokens checks two distinct accounts only, and cannot establish global total-supply equivalence alone. `inverseMintBurn` only checks an account's reported balance, not restoration of every state field or debt rate.

## Second semantic audit (26/26)

Columns: (a) falsifying counterexample; (b) defensible property label; (c) normative versus diagnostic; (d) report attribution; (e) target and aggregate separation.

| # | Source property | What falsifies the assertion? | Label | Report item / Result / Outcome |
|---:|---|---|---|---|
| 1 | Stable `integrityTimeStamp` | last-update timestamp later than modeled block after f | S3-2 | #9 ✔* / VERIFIED / NO_FINDING |
| 2 | Stable `balanceOfChange` | two different users' balances both change after one f | S3-2 | #11 ✔* / VERIFIED / NO_FINDING |
| 3 | Stable `integirtyBalanceOfTotalSupply` | non-burn user/supply deltas disagree | S6-4 | aggregate #12 / NOT_STATED / NOT_STATED |
| 4 | Stable `integirtyBalanceOfTotalSupplyOnBurn` | burn's supply-zero branch or balance/supply delta condition fails | S6-4 | aggregate #12 / NOT_STATED / NOT_STATED |
| 5 | Stable `integrityMint` | account credit differs from minted x | S6-4 | #13 ✔* / VERIFIED / NO_FINDING |
| 6 | Stable `additiveMint` | split mint differs from one combined mint | L2 | #14 ✔*; historic medium rounding issue / VERIFIED / FINDING |
| 7 | Stable `integrityBurn` | burn changes balance by wrong amount | S6-4 | #15 ✔* / VERIFIED / NO_FINDING |
| 8 | Stable `additiveBurn` | two burns differ from a combined burn | S6-4 | #16 ✔* / VERIFIED / NO_FINDING |
| 9 | Stable `inverseMintBurn` | mint followed by equal burn fails to restore balance | S6-4 | #17 ✔* / VERIFIED / NO_FINDING |
| 10 | Variable `balanceOfChange` | two distinct users' balances both change after one f | S3-2 | #19 ✔* / VERIFIED / NO_FINDING |
| 11 | Variable `integirtyBalanceOfTotalSupply` | non-mint/non-burn balance and supply deltas disagree | S6-4 | aggregate #20 / NOT_STATED / NOT_STATED |
| 12 | Variable `integirtyBalanceOfTotalSupplyOnBurn` | balance and supply burn deltas disagree | S6-4 | aggregate #20 / NOT_STATED / NOT_STATED |
| 13 | Variable `integirtyBalanceOfTotalSupplyOnMint` | minted balance and supply increments disagree | S6-4 | aggregate #20 / NOT_STATED / NOT_STATED |
| 14 | Variable `integrityMint` | recipient credit wrong or distinct delegate's balance changes | S6-4 | #21 ✔* / VERIFIED / NO_FINDING |
| 15 | Variable `additiveMint` | two scaled mints differ from one combined mint | L2 | #22 ✔* / VERIFIED / NO_FINDING |
| 16 | Variable `integrityBurn` | observed debt reduction differs from burn amount | S6-4 | #23 ✔* / VERIFIED / NO_FINDING |
| 17 | Variable `additiveBurn` | two scaled burns differ from a combined burn | L2 | #24 ✔* / VERIFIED / NO_FINDING |
| 18 | Variable `inverseMintBurn` | mint/burn sequence fails to restore balance | S6-4 | #25 ✔* / VERIFIED / NO_FINDING |
| 19 | User `empty` | empty flag true while borrow or collateral set | S6-2 | #26.I ✔ / VERIFIED / NO_FINDING |
| 20 | User `notEmpty` | borrow/collateral present while empty flag true | S6-2 | #26.II ✔ / VERIFIED / NO_FINDING |
| 21 | User `borrowing` | reserve borrow true while aggregate borrow false | S6-2 | #26.III ✔ / VERIFIED / NO_FINDING |
| 22 | User `collateralOrBorrowing` | combined getter differs from OR of individual flags | S6-2 | #26.IV ✔ / VERIFIED / NO_FINDING |
| 23 | User `setBorrowing` | same reserve's borrow flag differs from input | S3-2 | #27 ✔ / VERIFIED / NO_FINDING |
| 24 | User `setBorrowingNoChangeToOther` | other reserve's borrow or collateral flag changes | S3-2 | #28 ✔ / VERIFIED / NO_FINDING |
| 25 | User `setUsingAsCollateral` | same reserve's collateral flag differs from input | S3-2 | #29 ✔ (report typo) / VERIFIED / NO_FINDING |
| 26 | User `setUsingAsCollateralNoChangeToOther` | other reserve's borrow/collateral flag changes | S3-2 | #30 ✔ / VERIFIED / NO_FINDING |

**Per-row review:** all 26 are normative; labels follow falsifying behavior rather than file name, report severity, or finding label. The five aggregated rules remain NOT_STATED rather than inheriting a result. Stable / Variable / User targets are separated, report issue ≠ property ≠ Bug Label, and no extra finding is silently assigned.

## Source provenance and integrity evidence

All original `contracts/` and `specs/` source files from the PropertyGPT AAVE V2 subtree were copied into `contracts/12/`: **127 blobs**; verified by **Git tree identity** (which hashes all descendant path names, file contents and hierarchy):

- Source `certora_projects/aave_v2/contracts` SHA-1 tree `2a239836b37faafa2d5b5d3ed7f63f8b7b624cde` = destination `contracts/12/contracts`.
- Source `certora_projects/aave_v2/specs` SHA-1 tree `c34bd13f4ec6ab61263bfc767c6b7b2564ecb41d` = destination `contracts/12/specs`.
- Source `AaveV2Dec2020.pdf` Git blob SHA-1 `705d0961134f5a0b9d48c15723a5cde367c7e003` = destination `resources/12/AaveV2Dec2020.pdf` blob; preserved byte-for-byte.
- Original spec blobs: `StableDebtToken.spec a486d335352d73d4d81495447d29be20b9916e31`, `UserConfiguration.spec 41a4f93e1323157efb5411cb72ebeb7a5d60f68a`, `VariableDebtToken.spec eb19d1b4f435b67d52f2486fd99335d173883d1b`.

## Structural audit and validation limitations

The GitHub repository APIs confirm 26 Project 12 CSV rows, 26 individual `.spec` files, 26 `.sol` files, 26 `.md` files, and no missing artifact paths within `complete/12/`. Source block extraction was scripted and every active source block was checked against its known starting declaration before writing.

**Required CLI validators were NOT executed** on a complete local repository. Attempting to clone both public repositories in the available Python/container environment failed with `fatal: unable to access https://github.com/...: Could not resolve host: github.com`. An alternate authorized Desktop Commander device was reported offline, so the full project working tree was unavailable for local execution. Consequently **no PASS is claimed** for:
```sh
python scripts/check_specs.py .
python scripts/check_contests_csv.py .
python scripts/check_contracts.py .
git diff --check
```
Nor has CVL parsing, compilation, satisfiability or prover verification been rerun. This is a material release gate: do not mark the PR ready for review until those checks actually run and an independent semantic reviewer accepts the limitations above.

## Catalog locations

- Index: `results/spec/spec_buglabel.csv`
- 26 complete examples: `results/spec/complete/12/1.*` through `26.*`
- Original source snapshot: `contracts/12/contracts/` and `contracts/12/specs/`
- Historical PDF: `resources/12/AaveV2Dec2020.pdf`
- Relevant report summary: `reports/12.md`
