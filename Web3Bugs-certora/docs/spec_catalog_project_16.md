# Project 16 — AAVE Rescue Mission Phase 1 (historical alias)

## Project identity and evidence

The Project ID **16** was absent from `main`'s contest registry, catalog paths, and branch search before starting the exclusive branch `catalog/p16-ceres-aave-rescue-mission`. **This is not a different security audit:** Project 3 already contains the identical original `PropertyGPT/certora_projects/aave_rescue_mission` snapshot and the same PDF. Project 16 is an expressly disclosed second catalog ID for the **same three original properties**. Nothing in Project 3 has been modified or reinterpreted as an additional proof.

- Original PropertyGPT main tree: `687f654c679ed45ab127b7949e2a29c8f5e491b9`.
- Original PDF Git blob: `074b15f58a63d749569d9d456155153dbc795f38`, at `resources/16/Rescue-Mission-Phase-1.pdf`.
- Original `rescueLendMigrator.spec` blob: `4d8b8b6d9f3861921a054a86af8a33e7b05cd9dc`.
- Original `rescueSTKAAVE.spec` blob: `972b8536f78c3647ff2c68961015181fac4c46ea`.

All source Solidity, interfaces, dependencies, and original specs under `contracts/16` retain the same Git object identities as the existing byte-verified Project 3 snapshot. The report transcription `reports/16.md` is based on the already checked five-page Project 3 report, with the catalog metadata changed for Project 16; **the unmodified PDF remains authoritative**. The history and historical findings are referenced to Project 3 instead of falsely counted twice in `results/bugs.csv`.

## Exact active CVL inventory and source ranges

There are **three** active source properties: one `invariant` and one `rule` in `rescueLendMigrator.spec`, and one `invariant` in `rescueSTKAAVE.spec`. The commented-out `rule LendIsBackedByAave` in the migrator source is NOT counted. The declared ghost `lend_to_aave` has no active initializer axiom or use by these three properties. Neither spec imports another CVL spec.

| N | Source property | Source lines | Target | Status | Result | Detection Outcome | Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `LendIsBackedByAave` (invariant) | 19–27 | `LendToAaveMigrator` | incomplete | VIOLATED | FINDING | S6-4 |
| 2 | `LendIsBackedByAaveIncInitialize` (rule) | 41–61 | `LendToAaveMigrator`, with `AaveTokenV2` | incomplete | VERIFIED | NO_FINDING | S6-4 |
| 3 | `StkAaveIsBackedByAave` (invariant) | 9–19 | `StakedTokenV2Rev4` | incomplete | VERIFIED | FINDING | S6-4 |

Coverage: **3 / 3 active**; **0 complete / 3 incomplete**; three CVL-to-label CSV rows. The result statuses are report marks attached to the named properties, not new Certora runs. All three technical Bug Labels concern collateral/backing accounting (S6-4), independent of the reported finding labels. Project 3 already holds the **three historical issue rows**. No new issue rows were added for ID 16 to avoid double-counting the *same* PDF findings.

## Second semantic review

**Example 1 — LEND backing.** The inequality is `(LEND1.totalSupply() - LEND1.balanceOf(LEND1)) / LEND_AAVE_RATIO() <= AAVE1.balanceOf(currentContract)`. In Solidity, `AAVE` and `LEND` are public immutable token references; `LEND_AAVE_RATIO` is a public immutable getter (not a missing stub); `_totalLendMigrated` tracks migrated LEND. The migrator's `initialize` transfers AAVE to the distributor and LEND to the LEND-token address, whereas `migrateFromLEND` receives LEND and sends AAVE to the migrator's caller. The initializer subtracts `lendToAaveAmount` in its Solidity `require`, but the CVL invariant does not deduct this not-yet-burned balance. A permitted post-state in which the amount required to back circulating LEND exceeds AAVE held by the migrator is a counterexample. Source restriction: preservation excludes LEND and AAVE token contract callers. The report explicitly marks this named rule **❌** and identifies two associated potential issues, while also stating later mitigations passed verification; do **not** replace the explicitly violated result with the report-wide success claim.

**Example 2 — coordinated initialization.** The rule assumes the same backing relation in the prestate. If `f.selector` matches `initialize(address,uint256,uint256,uint256)`, it invokes migrator `initialize` and then `AAVE_ORIG.initialize` with the same `lendToAaveAmount`; in other cases it executes arbitrary `f(e,args)`. Only after this sequence does it assert the inequality. The paired AAVE initializer transfers the LEND balance into the LEND-token address, changing the circulating-supply term. A counterexample is a pre-backed state and allowed selected transition with insufficient poststate AAVE. **The ✔ here does not prove safety between two asynchronous real governance transactions or against arbitrary interleavings.** The source declares `env e2` but passes `e` into `AAVE_ORIG.initialize`; this is preserved, not repaired. The report explicitly verifies this named extension but does not link it to the two named LEND findings.

**Example 3 — stkAAVE backing.** The invariant requires `totalSupply() <= STAKED_TOKEN1.balanceOf(currentContract)`. The inherited ERC20 `totalSupply`, `_mint` and `_burn` supply the liability behavior; concrete `stake`/`redeem` move underlying and change shares. `StakedTokenV2Rev4.initialize` can rescue assets to the distributor while preserving a postcondition on its staked underlying reserve; `REWARDS_VAULT` is a real immutable getter and `claimRewards` interacts with that vault; the concrete transfer hook implements `onTransfer`. The invariant's preserved block excludes calls by the underlying token and target and excludes the rewards vault equaling the target. A state where share total supply exceeds underlying reserves is a counterexample. The report directly identifies an earlier rescue vulnerability detected by this property but marks the **fixed implementation ✔**; hence VERIFIED / FINDING is not a contradiction.

The source's `methods { }` declarations (including `onTransfer => NONDET` and `transfer => DISPATCHER(true)`) are summaries, not automatically concrete implementations. The CVL portions and selected Solidity excerpt lines are copied from the verified Project 3 catalog with only nonsemantic provenance path changes; individual source-to-assertion explanations live in `results/spec/incomplete/16/{1,2,3}.md`.

## Historical targets, scripts, and transitive dependencies

**The source snapshot is not a reproducible complete verification package.**

- Examples 1 and 2 require `DummyERC20Impl as LEND1` and `DummyERC20Impl2 as AAVE1`, absent from the supplied snapshot; example 2's `AaveTokenV2` is concretely present, but that does not replace the missing dummy tokens. The original migrator imports `solidity-utils/contracts/oz-common/interfaces/IERC20.sol`, which is not vendored here.
- Example 3 requires the absent linked `DummyERC20Impl as STAKED_TOKEN1`. In contrast, the target's `totalSupply()` and `REWARDS_VAULT()` are implemented by existing Solidity; they are not listed as missing.
- The earlier independent Project 3 investigation located the true upstream `bgd-labs/rescue-mission-phase-1` `certora/harness/ERC20Dummy.sol`, `ERC20Dummy2.sol`, `SafeMath.sol`, `certora/scripts/verifyRescueLendMigrator.sh` and `verifyRescueStkAAVE.sh`. These establish historical target/alias linking, `solidity-utils` package mapping and `--optimistic_loop` behavior. They are **not present in the PropertyGPT snapshot**, and no unrelated dummy implementation was silently substituted. See `docs/spec_catalog_project_3.md` for the upstream corroboration and source-version drift evidence.
- Governance `ProposalPayloadShort`/`ProposalPayloadLong` and their proxy upgrade/rescue paths are present as source-context, but none of the three active assertions directly proves governance authorization or all multi-transaction timing behavior. Do **not** assign S5 access-control labels merely based on the proposal names.

Consequently all three examples have the required `N.txt` missing-dependency evidence and remain **incomplete**. The original CVL era / CVL2 migration is a separate issue and by itself is NOT why they are incomplete.

## Report qualifiers and version identity

The five-page original `Rescue-Mission-Phase-1.pdf` reports an audit conducted January 6–12 (year established externally as January 2023). It states the latest reviewed commit as `4c59da8d`, yet refers to later fixes including `c905eaf`; neither statement establishes a single precise Solidity commit for every source assertion/status. The source specs match Certora Review historical copies, while the supplied Solidity matches a later upstream master snapshot. The report's explicit per-property outcome symbols govern the catalog; snapshot excerpts are evidence of mechanisms, **not claims that each exact snapshot version was proven**.

The report limits loops to finite unrolling, missing violations requiring more than one loop iteration, and assumes `onTransfer` has no state effects. The LEND precondition excludes `msg.sender` equal to either token contract; the stkAAVE preserved context has additional source exclusions. The report defines ✔* for simplified proofs but does not establish an individual star for these three entries. The undefined `reqs2` footnote in the paired property is recorded as unresolved. No Prover rerun or stronger temporal claim is made.

## Validation, provenance and integration gates

**Executed on a real isolated Git checkout** of branch head `2b54951b02ea629197d9d5c1ea756fe7da2ca1e3`, with `origin/main` and merge-base both `46670617ee77649217b9dbf64fd6955344cedcf7`. The first attempt using the device's full `/tmp` failed during checkout and its private temporary clone was removed. Repeating inside `/var/tmp` succeeded; the remote Linux device has Git 2.53.0 and Python 3.14.4. Its `python` command was provided as an isolated symlink to system `python3`, so the repository's original scripts were not altered.

| Exact command and working directory | Exit code and output |
| --- | --- |
| `cd Web3Bugs-certora && python scripts/check_specs.py .` | **0**: 478 spec examples and 483 Bug Label relationships consistent |
| `cd Web3Bugs-certora && python scripts/check_contests_csv.py .` | **0**: reports/contests consistent |
| `cd Web3Bugs-certora && python scripts/check_contracts.py .` | **0**: contracts/reports consistent |
| `git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD` from actual Git root | **0**: no errors |

This pre-documentation-update validation establishes all four official gates at the stated SHA. A subsequent documentation-only commit should be retested and cited in the PR discussion before integration. Git showed only five untracked testing log/helper files in the *isolated* checkout, no tracked modifications.

### Independent source, excerpt, CSV and PDF audit

A separate independent Python check on the checked-out Project 16 assets returned **exit 0 / 0 errors**: 3/3 catalog instances; all 9 declared CVL source ranges copied literally; all **19** declared Solidity source excerpt ranges present literally in the example snippets (4 + 8 + 7); 15/15 source snapshot files byte-identical to Project 3; Project 16 PDF byte-identical to Project 3; full previous `spec_buglabel.csv` and `contests.csv` preserved as exact byte prefixes. Both `contracts/3` and `contracts/16` resolve to the same Git tree `89ae9f4ed69bd9aab626a86d1f0a27895fba09eb`. The original PDF Git blob remains `074b15f58a63d749569d9d456155153dbc795f38` with SHA-256 `9c2d52ef16b8fae0d7168ad9fcc4e98a352c9c7f4c42eae50f3e329f660ee31b`.

**PDF raster visual review: 5/5 pages**, via PyMuPDF 1.28.2 at 1.5× page scale, compared with the report transcript and per-property files:

- Page 1: three-contract scope, reviewed commit `4c59da8d`, and first stkAAVE rescue finding.
- Page 2: the three issue entries, including the undercollateralization inequalities and later burnt-LEND issue fixed in `c905eaf`.
- Page 3: unrolled-loop limitation, no-state-change `onTransfer` assumption, and meanings of ✔ / ✔* / ❌.
- Page 4: exact named results: `LendIsBackedByAave` ❌, `LendIsBackedByAaveIncInitialize` ✔, `StkAaveIsBackedByAave` ✔; the paired initialize rule includes a `reqs2` reference.
- Page 5: only `reqs` is defined, excluding token-contract senders; `reqs2` is absent from the original and not invented.

The source/report drift and asynchronous intermediate-state distinction remain visible in all example documentation. This is a semantic and artifact-fidelity review **not** a new Certora Prover run; the original PDF is still authoritative for its mathematical layout.

### Integration caution

Only 33 paths changed in the initial PR commit: Project 16 contracts/specs, document, report, PDF, three examples, the two additive shared CSV indices, and a narrowly scoped `.gitattributes` addition. No Project 3 files or `results/bugs.csv` rows were changed. **Treat ID 16 as an alias, not a second original security audit.** The orchestrator must decide whether to retain an alias in the canonical dataset and must not merge before its review.

See `docs/spec_catalog_project_3.md` for the independently investigated upstream run-script/constructor-version differences and original source evidence.
