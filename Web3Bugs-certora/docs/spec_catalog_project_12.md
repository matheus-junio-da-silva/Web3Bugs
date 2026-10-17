# Project 12 — AAVE Protocol V2 (Ceres) spec catalog

## Scope and Project ID exclusivity

Project ID 6 is already occupied by the unrelated **Aave Static aToken** and has not been changed. This catalog uses **Project ID 12** exclusively. Source: https://github.com/matheus-junio-da-silva/PropertyGPT/tree/main/certora_projects/aave_v2. Branch: `catalog/p12-ceres-aave-v2`. Initial commit: `a073d5fd075a9544401f723a11fde959098fca5c`.

## Coverage and classification

| Original spec | Active rules | Active invariants | Complete | Incomplete |
|---|---:|---:|---:|---:|
| `StableDebtToken.spec` | 9 | 0 | 0 | 9 |
| `VariableDebtToken.spec` | 9 | 0 | 9 | 0 |
| `UserConfiguration.spec` | 4 | 4 | 8 | 0 |
| **Total** | **22** | **4** | **17** | **9** |

All 26 active property instances have dedicated `.spec`, `.sol`, `.md` under `results/spec/{complete,incomplete}/12/` (78 primary artifacts), and the nine incomplete StableDebtToken examples each have an `.txt` reason (9 additional files). The CSV contains **26 rows for 26 unique examples**, with no multi-label duplications. This is a **source snapshot dependency closure**, not proof that historical CVL will compile under CVL2 or that historical verification settings are available. There are **9 incomplete** examples for a concrete incompatible Solidity target dependency (not for missing run flags or CVL1/CVL2 syntax). The other 17 examples remain complete for source-snapshot dependency closure.

Formal Result, **per source instance**, from `reports/12.md` and the preserved original PDF:
- VERIFIED: 21 (7 StableDebtToken; 6 VariableDebtToken; 8 UserConfiguration).
- VIOLATED: 0 (no explicit violated result for the final current source instances).
- NOT_STATED: 5 (2 StableDebtToken and 3 VariableDebtToken source supply-consistency variants absent as individually named report entries).

Detection Outcome: FINDING **0**, NO_FINDING **20**, ACCEPTED_BEHAVIOR **0**, INCONCLUSIVE **0**, NOT_STATED **6**. The historic report describes a **medium rounding defect** in the stable-debt additive-mint concept, but does not trace that defect to the exact zero-rate, interest-suppressed source rule. Example 6 is **VERIFIED / NOT_STATED**: source-appropriate Result preserved and direct Detection Outcome unknown. No Project 12 property is assigned FINDING without individual causal evidence. `results/bugs.csv` adds just AV2-01 (L2) for that documented issue; unlinked/aggregate issues remain described in the report instead of being force-linked to source examples.

| Bug Label | Examples | Semantics |
|---|---:|---|
| S3-2 | 7 | timestamp, balance noninterference, bitmap flag updates |
| S6-4 | 12 | mint/burn supply and balance conservation, inverse behavior |
| S6-2 | 4 | cross-getter bitmap consistency |
| L2 | 3 | additivity sensitive to ray rounding |
| UNMAPPED | 0 | All selected properties encode a normative postcondition or getter equivalence |

## Dependency closure and target resolution

- **StableDebtToken (examples 1–9): INCOMPLETE**. The nine rules expect the historical `StableDebtTokenHarness`. The current preserved harness invokes `StableDebtToken(pool, underlyingAsset, name, symbol, incentivesController)` as a base constructor at harness lines 7–13, but the only `StableDebtToken.sol` under the snapshot has **no matching constructor** and instead uses `initialize(ILendingPool,address,IAaveIncentivesController,uint8,string,string,bytes)` at lines 41–49. In addition, the harness declares `getIncentivesController() returns (address)` at lines 26–28 while the superclass at lines 355–357 implements a non-`virtual` `getIncentivesController() returns (IAaveIncentivesController)`. The correct original compatible parent/override environment is **absent**, not merely using an old CVL syntax. All nine rules therefore belong in `incomplete/12/` with explicit `N.txt` evidence, even though individual getters/mint/burn operations exist in the preserved parent source. The historical interest-suppression overrides are retained verbatim. Source-level formal Results from the report are **not** changed by this dependency-status correction.
- **VariableDebtToken (examples 10–18)** targets `VariableDebtToken` and uses the original `using LendingPoolHarnessForVariableDebtToken as POOL` where the rule calls POOL (source line 1). The harness's `getReserveNormalizedVariableDebt` reads a timestamp-keyed private mapping, requires the entry to equal `1e27`, and returns it (lines 157–167). The target's `mint`, `burn`, `balanceOf`, and `totalSupply` are implemented in `VariableDebtToken.sol` (lines 75–152), with scaled storage in `IncentivizedERC20.sol`. No historical link configuration is supplied; possible unreachable paths/vacuity are **not** disproved by structural closure.
- **UserConfiguration (examples 19–26)** targets `UserConfigurationHarness`, which wraps `UserConfiguration` library methods and owns one `DataTypes.UserConfigurationMap`. Required original `methods` declarations were copied selectively into each extracted spec; a declaration was not mistaken for a Solidity implementation. The bitmap library implementation and struct appear in the complete source snapshot.

CVL built-ins such as `env`, `sinvoke`, `storage`, `lastStorage`, `calldataarg`, and symbolic `method` arguments are not counted as missing project helpers. The three original specs contain **no active imports, definitions, ghosts, hooks, or rules outside the 26 listed instances**. There are 3 actual historical harness source files. Source does not include historical `.conf` scripts or replay flags; exact prover reproduction is not claimed.

## Report/source status separation and limitations

Report: `reports/12.md` (structured report-section transcription) and byte-identical `resources/12/AaveV2Dec2020.pdf` (25 pages; complete authoritative original). The source report describes verification from 2020-08-02 to 2020-10-29 and latest commit `750920303e33b66bc29862ea3b85206dda9ce786`. It defines `✔` as latest-commit verified, and `✔*` as verified **on simplified code that ignores rounding errors**. Every selected StableDebtToken and VariableDebtToken report property has the `✔*` qualifier; UserConfiguration entries #26–#30 have plain `✔`. The `✔*` label does **not** certify exact behavior of all integer rounding/index values.

- **Aggregate-versus-individual:** StableDebtToken #10 aggregate is stated as proved by report #11–#12. Source `integirtyBalanceOfTotalSupply` and `integirtyBalanceOfTotalSupplyOnBurn` split #12's concept. Neither has separate explicit report outcome; both `NOT_STATED`. VariableDebtToken #18 aggregate uses #19–#20 but the source splits #20 into generic, mint and burn rules; all three remain `NOT_STATED`. This does not deny the aggregate proof, only prevents unsupported allocation to exact source rules.
- **Historical medium issue, not individually attributed:** The report calls a rounding defect *Additive mint (Stable debt token)*. The source explicitly requires `getUserStableRate(a)==0`, its harness suppresses interest accrual, and report ✔* ignores rounding. The report does **not** prove that this exact source instance directly detected the issue. Keep the issue in `bugs.csv` but use NOT_STATED for example 6 Detection Outcome.
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
| 6 | Stable `additiveMint` | split mint differs from one combined mint | L2 | #14 ✔* / VERIFIED / NOT_STATED; historical issue is separate |
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

**Per-row review:** all 26 are normative; labels follow falsifying behavior rather than file name, report severity, or finding label. Historical AV2-01 is no longer attributed to example 6. The five aggregated rules remain NOT_STATED rather than inheriting a result. Stable / Variable / User targets are separated, report issue ≠ property ≠ Bug Label, and no extra finding is silently assigned.

## Source provenance and integrity evidence

All original `contracts/` and `specs/` source files from the PropertyGPT AAVE V2 subtree were copied into `contracts/12/`: **127 blobs**; verified by **Git tree identity** (which hashes all descendant path names, file contents and hierarchy):

- Source `certora_projects/aave_v2/contracts` SHA-1 tree `2a239836b37faafa2d5b5d3ed7f63f8b7b624cde` = destination `contracts/12/contracts`.
- Source `certora_projects/aave_v2/specs` SHA-1 tree `c34bd13f4ec6ab61263bfc767c6b7b2564ecb41d` = destination `contracts/12/specs`.
- Source `AaveV2Dec2020.pdf` Git blob SHA-1 `705d0961134f5a0b9d48c15723a5cde367c7e003` = destination `resources/12/AaveV2Dec2020.pdf` blob; preserved byte-for-byte.
- Original spec blobs: `StableDebtToken.spec a486d335352d73d4d81495447d29be20b9916e31`, `UserConfiguration.spec 41a4f93e1323157efb5411cb72ebeb7a5d60f68a`, `VariableDebtToken.spec eb19d1b4f435b67d52f2486fd99335d173883d1b`.

## Structural audit and validation limitations

The GitHub repository APIs confirmed 26 Project 12 CSV rows and 26 each `.spec`, `.sol`, `.md`; 17 complete examples and 9 incomplete examples additionally require nine `.txt` reasons. No example is promoted to complete solely because a function name appears in `methods {}`. Source block extraction was scripted and every active source block was checked against its known starting declaration before writing.

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
- 9 incomplete examples: `results/spec/incomplete/12/1.*` through `9.*`, each with `.txt`
- 17 complete examples: `results/spec/complete/12/10.*` through `26.*`
- Original source snapshot: `contracts/12/contracts/` and `contracts/12/specs/`
- Historical PDF: `resources/12/AaveV2Dec2020.pdf`
- Relevant report summary: `reports/12.md`

## 2026-10-17 status correction — incompatible historical StableDebtToken parent

The exhaustive current snapshot supplies all symbol names required by the nine stable rules, but its Solidity class versions are not mutually compatible: `StableDebtTokenHarness.sol:7-13` invokes a nonexistent base constructor and `:26-28` conflicts with the current inherited getter at `StableDebtToken.sol:355-357`. This is a **missing historical compatible target implementation**, not absence of CVL1-to-CVL2 migration. No invented replacement is permitted; all nine stable properties are now `incomplete`. The original CVL text, Solidity excerpts, source snapshot, report Result and per-instance Bug Labels are preserved. Each `N.txt` records concrete missing signatures and searched paths.

## Current execution blockade

At this workspace on 2026-10-17, `test -d /mnt/data/Web3Bugs-certora` returned exit **1**, and `git ls-remote https://github.com/matheus-junio-da-silva/Web3Bugs.git HEAD` returned exit **128** with `Could not resolve host: github.com`. The registered Desktop Commander machine remained offline. **The four mandatory project validators cannot be executed against a checked-out repository here.** Their actual test exit codes are unavailable; do not report PASS. This Draft PR remains blocked. Merge SHA and GitHub API-level integrity checks are reported separately, not substituted for CLI validations.
