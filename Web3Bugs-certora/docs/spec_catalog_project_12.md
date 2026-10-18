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

The initial local VM preflight did not have a checkout or working GitHub DNS resolution, and therefore none of the validators could be run **locally** at that time. **This blockade was resolved by the actual CI execution on GitHub Actions** (see the 2026-10-17 evidence table below): all three Python structural checks and the exact requested Git whitespace command returned exit **0** in a full checked-out repository at SHA `c4fb7071904be826500f459d778fd19e93380c83`. The former NOT RUN statements apply only to the initial VM attempt, not to the final validated branch. Modern CVL compilation, Prover satisfiability and Solidity harness linkage **were not** rerun; the nine historical target-incompatibility cases remain incomplete.

## Catalog locations

- Index: `results/spec/spec_buglabel.csv`
- 9 incomplete examples: `results/spec/incomplete/12/1.*` through `9.*`, each with `.txt`
- 17 complete examples: `results/spec/complete/12/10.*` through `26.*`
- Original source snapshot: `contracts/12/contracts/` and `contracts/12/specs/`
- Historical PDF: `resources/12/AaveV2Dec2020.pdf`
- Relevant report summary: `reports/12.md`

## 2026-10-17 status correction — incompatible historical StableDebtToken parent

The exhaustive current snapshot supplies all symbol names required by the nine stable rules, but its Solidity class versions are not mutually compatible: `StableDebtTokenHarness.sol:7-13` invokes a nonexistent base constructor and `:26-28` conflicts with the current inherited getter at `StableDebtToken.sol:355-357`. This is a **missing historical compatible target implementation**, not absence of CVL1-to-CVL2 migration. No invented replacement is permitted; all nine stable properties are now `incomplete`. The original CVL text, Solidity excerpts, source snapshot, report Result and per-instance Bug Labels are preserved. Each `N.txt` records concrete missing signatures and searched paths.

## Historical VM execution blockade (superseded by actual GitHub CI)

At the initial VM preflight on 2026-10-17, `test -d /mnt/data/Web3Bugs-certora` returned exit **1**, and `git ls-remote https://github.com/matheus-junio-da-silva/Web3Bugs.git HEAD` returned exit **128** with `Could not resolve host: github.com`. Remote Desktop Commander was not used. This VM access restriction **no longer prevents the four structural GitHub Actions checks**: see the successful run and exit-code evidence below. The Draft PR stays open for *semantic* and *historical harness* review, rather than for missing Python/Git test execution.

## 2026-10-17 full-report fidelity review

Rechecked the 25-page PDF, including the historical issue table, proof notation, AToken #1–#8, StableDebtToken #9–#17, VariableDebtToken #18–#25, UserConfiguration #26–#30, LendingPool #31–#44, deferred redirection #45–#49, suggested Aave P1–P41 and the disclaimer. `reports/12.md` has been clarified as an **annotated report-wide index and summary**, not a claimed full verbatim transcript. The byte-identical historic PDF remains the complete authoritative reproduction. Preserved report discrepancies include UserConfiguration #29 (wrong getter in displayed postcondition), VariableDebtToken #24 (mint vs burn wording), AToken #8's suspect bound, and the description of `isEmpty`; no CVL source was rewritten to match misleading report prose.

## 2026-10-17 authorized GitHub Actions validation — exact execution evidence

VM-first preflight: `python --version` returned `Python 3.13.5`, `git --version` returned `git version 2.47.3`, but no repository checkout was available in `/mnt/data`. `git ls-remote https://github.com/matheus-junio-da-silva/Web3Bugs.git HEAD` returned exit **128** due to GitHub DNS failure. Local Git diff outside a checkout returned 129. Consequently a branch-scoped GitHub Actions workflow `.github/workflows/p12-catalog-validation.yml` was introduced to execute the **exact requested commands on a real checkout** and persist logs; Remote Desktop Commander was not invoked.

Successful CI run: [GitHub Actions #39055687988](https://github.com/matheus-junio-da-silva/Web3Bugs/actions/runs/39055687988) (completed `success`). Checkout HEAD `c4fb7071904be826500f459d778fd19e93380c83`; `origin/main` SHA `4a1bea89d88aa3b6aa165e8d81b8dd523c7afb82`.

| Working directory | Exact command | Exit code | Actual output |
|---|---|---:|---|
| `Web3Bugs-certora/` | `python scripts/check_specs.py .` | **0** | `Check passed! 190 spec examples and 195 Bug Label relationships are structurally consistent.` |
| `Web3Bugs-certora/` | `python scripts/check_contests_csv.py .` | **0** | `Check passed!` |
| `Web3Bugs-certora/` | `python scripts/check_contracts.py .` | **0** | `Check passed!` |
| Git repo root | `git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD` | **0** | empty output (no introduced whitespace errors in checked paths) |

The first CI attempt [run #39055531805](https://github.com/matheus-junio-da-silva/Web3Bugs/actions/runs/39055531805) produced exit codes `0,0,0,2` respectively: the final command reported 111 historic/extraction whitespace diagnostics. The source snapshot and original CVL lines have been kept byte-for-byte identical to the source; `Web3Bugs-certora/.gitattributes` now narrowly disables whitespace checking only on the **historical `contracts/12/**` tree and the literal extracted `results/spec/{complete,incomplete}/12/*.spec`**. Six generated Solidity excerpts with a superfluous final blank line were normalized. The second run `#39055687988` is the actual all-zero validation. This does not mean that source formatting was repaired or modernized and is **not** a Certora Prover execution.

The PR must remain Draft pending independent review of the nine incompatible StableDebtToken harness instances, the VariableDebtToken normalization-index assumption and whether the annotated Markdown report (PDF preserved separately) satisfies the dataset's transcription expectations.

## 2026-10-18 — targeted VERIFIED attribution re-audit (21 individual instances)

**Scope of this pass:** independently compare the property body's actual assertion with the matching printed report item in the authoritative 25-page PDF; keep Result separate from Detection Outcome, file availability and satisfiability. This audit reviewed original `StableDebtToken.spec`, `VariableDebtToken.spec`, `UserConfiguration.spec`, their harnesses, `reports/12.md` and the public image/text of the historical PDF. It does **not** claim to rerun the 2020 Prover or to prove the harness assumptions satisfiable.

| ID | Target / exact property | Report item | Report proof | Specific limitation on VERIFIED |
|---:|---|---|---|---|
| 1 | Stable `integrityTimeStamp` | #9 | ✔* | Existing timestamp bound, incentives controller zero and historical interest-free harness |
| 2 | Stable `balanceOfChange` | #11 | ✔* | Pairwise balance noninterference only; `sinvoke` and simplified balances |
| 5 | Stable `integrityMint` | #13 | ✔* | Actual fourth Solidity argument is stable rate, not normalized variable-debt index |
| 6 | Stable `additiveMint` | #14 | ✔* | `getUserStableRate(a)==0` explicitly excludes harder nonzero-rate case; rounding finding NOT shown to be generated by this exact rule; Detection Outcome NOT_STATED |
| 7 | Stable `integrityBurn` | #15 | ✔* | Exact subtraction assertion on principal balance, with interests suppressed |
| 8 | Stable `additiveBurn` | #16 | ✔* | Two burns versus one combined burn from `lastStorage`; ignores rounding and time/rate growth |
| 9 | Stable `inverseMintBurn` | #17 | ✔* | Tests only restoration of `balanceOf(a)`, not timestamps, rates or all supply fields |
| 10 | Variable `balanceOfChange` | #19 | ✔* | Pairwise balances; inherited balance getter consults normalized-debt index |
| 14 | Variable `integrityMint` | #21 | ✔* | Recipient balance and distinct delegate unaffected; POOL getter requires `1e27` |
| 15 | Variable `additiveMint` | #22 | ✔* | Compares two scaled mints with combined mint; literal `rayDiv` rounding outside proof |
| 16 | Variable `integrityBurn` | #23 | ✔* | Uses `POOL.getReserveNormalizedVariableDebt` and exact amount/scale equivalence |
| 17 | Variable `additiveBurn` | #24 | ✔* | Two scaled burns vs one; report's prose says mint but title/source assert burn |
| 18 | Variable `inverseMintBurn` | #25 | ✔* | Only observed debt balance restored; conditional index / mint-burn timing |
| 19 | User `empty` invariant | #26.I | ✔ | One singleton bitmap; getter no explicit CVL `reserveIndex<128` guard |
| 20 | User `notEmpty` invariant | #26.II | ✔ | One bitmap; out-of-range index getter may revert |
| 21 | User `borrowing` invariant | #26.III | ✔ | Specific borrowing bit implies aggregate mask; reserve index implicit getter constraint |
| 22 | User `collateralOrBorrowing` invariant | #26.IV | ✔ | Combined bitmap getter matches individual OR only on admissible getter inputs |
| 23 | User `setBorrowing` | #27 | ✔ | `reserveIndex<128` assumed; intended borrow bit only |
| 24 | User `setBorrowingNoChangeToOther` | #28 | ✔ | Two **distinct** reserve indices, both below 128; single stored user-map |
| 25 | User `setUsingAsCollateral` | #29 | ✔ | CVL asserts collateral getter; report's printed postcondition erroneously names borrowing getter |
| 26 | User `setUsingAsCollateralNoChangeToOther` | #30 | ✔ | Two distinct reserve indices under 128; other flags preserved |

The 5 remaining source instances (#3, #4, #11, #12, #13) are `NOT_STATED`, because report aggregate #12/#20 does not name those particular source-specific decompositions as independent rule results. All 26 original bodies have previously been compared byte-preservingly with their source ranges, and 123 Solidity source excerpts were matched to cited lines in the published GitHub Actions provenance checker. **VERIFIED is an historical, qualified report status**, not a claim that current sources/harness compile together. All nine StableDebtToken source examples remain **incomplete** because the preserved harness calls a nonexistent five-argument base constructor and declares a conflicting inherited `getIncentivesController()`.

### ZIP inspection limitation (this session)

The Project's `Web3Bugs.zip` is discoverable as a shared `application/zip` file with file ID `file_00000000c01c820ea5f7fb48351dc818`, and an exact attached path was supplied for the current VM (`/mnt/data/Web3Bugs.zip`). However, direct `container.exec`, analysis Python and user-visible Python all failed with infrastructure `ClientError` before running filesystem inspection or extraction. The Project file service can confirm its existence but cannot render ZIP directory entries as text. **This pass has not established whether the ZIP contains a `.git` directory, and no local checkout, `git init`, `git pull`, or ZIP-to-HEAD comparison is claimed.** The GitHub branch already stores the independently verified 127-file historical source subtree; CI executes on the legitimate GitHub Actions checkout and logs the actual commit SHA. ZIP verification remains an independent evidence gap, not a reason to alter the authoritative PR tree or historic source objects.

### Git attributes and CI boundary

`Web3Bugs-certora/.gitattributes` disables whitespace checks **only** on `contracts/12/**` and the literal `results/spec/{complete,incomplete}/12/*.spec` paths. It does not exempt the Markdown documentation, CSV indexes, scripts, workflow or generated `.sol` files. The Project 12 workflow performs `actions/checkout@v4` with `fetch-depth: 0`, logs `git rev-parse HEAD` and `origin/main`, runs all four mandatory commands at the specified working directories and records their exit codes. Existing successful GitHub Actions evidence (run #39056109287) is for its exact logged SHA, not the uninspected ZIP. No merge has been attempted.
