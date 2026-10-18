# Project 20 — Sushi BentoBox: Boreal historical Certora catalog

## Provenance and completeness

- Source: PropertyGPT/certora_projects/sushi_benttobox/ (original double-t spelling retained).
- Source commit: 687f654c679ed45ab127b7949e2a29c8f5e491b9.
- Base destination main: 46670617ee77649217b9dbf64fd6955344cedcf7.
- Report: SushiBentoboxFeb2021.pdf, 11 pages, project verification January 25–February 9, 2021; report latest reviewed contract commit 0c68f2aa38cd600b5959197416fe090baa6a2a3f.
- Original blobs: 66 files, sha256 per original in docs/spec_catalog_project_20_source_hashes.json; PDF retained byte-for-byte under resources/20, original non-PDF source under contracts/20.
- Source declarations: 34, from six named specs: {'bentobox.spec': 8, 'bentoBoxCompoundStrategy.spec': 8, 'compoundStrategy.spec': 6, 'compoundStrategyAdditional.spec': 1, 'rebase.spec': 8, 'strategy.spec': 3}.
- Extracted instances: 37, including a separate three-rule instance for SymbolicStrategy and SushiStrategyHarness using shared strategy.spec.
- Dependency status: 0 complete, 37 incomplete. This is historical dependency completeness, not source correctness or proof outcome.
- Original imports missing: node_modules/@boringcrypto/boring-solidity, referenced by BentoBox, MasterContractManager, RebaseWrapper, strategy harnesses and strategies. Flat sources are present but do not prove exact imported historical module identity.
- An independent CVL omission affects compoundStrategyAdditional.spec: MAX_INT() invoked without a local definition or import.
- Report extraction: reports/20.md is text-layer layout transcript, authoritative source remains PDF.

## Formal outcomes and labeling

- Report marks the eight high-level BentoBox properties ✔ on its latest checked version (pp8–9). Seven exact/aligned source cases are assigned VERIFIED only to bentobox.spec with symbolic linked strategy; additivity remains NOT_STATED because the source performs deposits while PDF p9 describes withdrawals.
- The source bentoBoxCompoundStrategy.spec is a separate Compound strategy context with an April 18 message in its historical script, not proven by the February report; all eight instances retain NOT_STATED.
- Rebase report (p6) explicitly ✔ monotonicity's named toBaseIsMonotone and toElasticIsMonotone. Identity ✔ refers to the wildcard group toElasticAndToBaseAreInverse*, not to individual proof status for each source variant; those six retain NOT_STATED.
- Strategy report (pp10–11) says SushiStrategy and SymbolicStrategy were verified under the listed three high-level integrity obligations. Their shared three source rules are catalogued independently for both targets; per-source caveats apply.
- CompoundStrategy standalone and additional rules are not individually reported; Result and Detection Outcome remain NOT_STATED.
- Three named BentoBox rules (preserveTotalAssetsOfUser, noChangeToOthersBalances, solvency) have earlier issue attribution on PDF pp2–3, but the final PDF says ✔. This yields Result VERIFIED, Detection Outcome FINDING for the source context only: an earlier detected problem subsequently fixed, **not** a claim the final code violates the rule.
- Flashloan denial-of-service is explicitly marked Rules Broken N/A. Do not attribute it to totalAssetsAfterFlashLoan, which checks a different asset-nondecrease postcondition.
- The report's locked-assets finding names inverse of deposit and withdraw, a rule absent from six available specs; it is not retroactively mapped to rebase conversion inverse rules.
- The historical noChangeToOthersBalances source asserts preShares <= postShares, not strict equality and not equality of amount-denominated value. The PDF high-level phrasing is stronger than this CVL.
- The additivity source **deposits** split/summed shares while PDF p9 describes additivity of **withdrawals**; we preserve the actual assertion without claiming equivalent economic behavior.
- The historic harvest rules contain amountAdded < MIN_INT(), potentially unsatisfiable depending on CVL typing. No non-vacuity demonstration was performed.
- StrategyHarness.compareLEmaxUint255 uses Solidity ^ (bitwise XOR), not mathematical exponentiation; do not interpret that helper as a standard 2^255 bound without reviewing use.
- All historical run scripts, source versions, Solidity literal excerpts, and CVL helpers are preserved. applyHarnesses.sh has not been executed on the snapshot; it changes contract semantics and can affect proof soundness.

## Accounting mapping

BentoBox's balanceOf[token][user] is a **share count**, totals[token].base is aggregate shares, and totals[token].elastic is recorded total asset amount. RebaseWrapper.rebase.base/elastic controls conversions and rounding, not an ERC20 transfer. External IERC20.balanceOf(user or BentoBox) is a token amount. strategyData[token].balance tracks BentoBox's believed strategy amount; it is not a direct getter of actual underlying-token balances inside Compound or Sushi. A proof of book accounting alone must not be described as proof of on-chain full collateral coverage.

## Property-to-target ledger

| # | Source spec | Concrete target (linked context) | Property | Label | Result | Detection Outcome |
|---:|---|---|---|---|---|---|
| 1 | bentobox.spec | BentoBoxHarness (SymbolicStrategy) | zeroStrategy | S3-2 | VERIFIED | NO_FINDING |
| 2 | bentobox.spec | BentoBoxHarness (SymbolicStrategy) | integrityOfTotalShare | S6-4 | VERIFIED | NO_FINDING |
| 3 | bentobox.spec | BentoBoxHarness (SymbolicStrategy) | solvency | S6-4 | VERIFIED | FINDING |
| 4 | bentobox.spec | BentoBoxHarness (SymbolicStrategy) | totalAssetsAfterFlashLoan | S6-4 | VERIFIED | NO_FINDING |
| 5 | bentobox.spec | BentoBoxHarness (SymbolicStrategy) | additivity | S6-4 | NOT_STATED | NOT_STATED |
| 6 | bentobox.spec | BentoBoxHarness (SymbolicStrategy) | validDecreaseToBalanceOf | S3-2 | VERIFIED | NO_FINDING |
| 7 | bentobox.spec | BentoBoxHarness (SymbolicStrategy) | noChangeToOthersBalances | S3-2 | VERIFIED | FINDING |
| 8 | bentobox.spec | BentoBoxHarness (SymbolicStrategy) | preserveTotalAssetsOfUser | S6-4 | VERIFIED | FINDING |
| 9 | bentoBoxCompoundStrategy.spec | BentoBoxHarness (CompoundStrategyHarness) | zeroStrategy | S3-2 | NOT_STATED | NOT_STATED |
| 10 | bentoBoxCompoundStrategy.spec | BentoBoxHarness (CompoundStrategyHarness) | integrityOfTotalShare | S6-4 | NOT_STATED | NOT_STATED |
| 11 | bentoBoxCompoundStrategy.spec | BentoBoxHarness (CompoundStrategyHarness) | solvency | S6-4 | NOT_STATED | NOT_STATED |
| 12 | bentoBoxCompoundStrategy.spec | BentoBoxHarness (CompoundStrategyHarness) | totalAssetsAfterFlashLoan | S6-4 | NOT_STATED | NOT_STATED |
| 13 | bentoBoxCompoundStrategy.spec | BentoBoxHarness (CompoundStrategyHarness) | additivity | S6-4 | NOT_STATED | NOT_STATED |
| 14 | bentoBoxCompoundStrategy.spec | BentoBoxHarness (CompoundStrategyHarness) | validDecreaseToBalanceOf | S3-2 | NOT_STATED | NOT_STATED |
| 15 | bentoBoxCompoundStrategy.spec | BentoBoxHarness (CompoundStrategyHarness) | noChangeToOthersBalances | S3-2 | NOT_STATED | NOT_STATED |
| 16 | bentoBoxCompoundStrategy.spec | BentoBoxHarness (CompoundStrategyHarness) | preserveTotalAssetsOfUser | S6-4 | NOT_STATED | NOT_STATED |
| 17 | compoundStrategy.spec | CompoundStrategyHarness (CompoundStrategy) | allTokensAreInvested | S6-4 | NOT_STATED | NOT_STATED |
| 18 | compoundStrategy.spec | CompoundStrategyHarness (CompoundStrategy) | onceExitedIsTrueThenItIsNeverFalse | S3-2 | NOT_STATED | NOT_STATED |
| 19 | compoundStrategy.spec | CompoundStrategyHarness (CompoundStrategy) | ifExitedIsTrueThenMethodsRevertExceptOwner | S5-2 | NOT_STATED | NOT_STATED |
| 20 | compoundStrategy.spec | CompoundStrategyHarness (CompoundStrategy) | integrityHarvest | S6-4 | NOT_STATED | NOT_STATED |
| 21 | compoundStrategy.spec | CompoundStrategyHarness (CompoundStrategy) | integrityWithdraw | S6-4 | NOT_STATED | NOT_STATED |
| 22 | compoundStrategy.spec | CompoundStrategyHarness (CompoundStrategy) | integrityExit | S6-4 | NOT_STATED | NOT_STATED |
| 23 | compoundStrategyAdditional.spec | CompoundStrategyHarness (CompoundStrategy) | exitRevert | UNMAPPED | NOT_STATED | NOT_STATED |
| 24 | rebase.spec | RebaseWrapper (RebaseLibrary) | toBaseIsMonotone | S6-2 | VERIFIED | NO_FINDING |
| 25 | rebase.spec | RebaseWrapper (RebaseLibrary) | toElasticIsMonotone | S6-2 | VERIFIED | NO_FINDING |
| 26 | rebase.spec | RebaseWrapper (RebaseLibrary) | toElasticAndToBaseAreInverse1down | S6-2 | NOT_STATED | NOT_STATED |
| 27 | rebase.spec | RebaseWrapper (RebaseLibrary) | toElasticAndToBaseAreInverse1up | S6-2 | NOT_STATED | NOT_STATED |
| 28 | rebase.spec | RebaseWrapper (RebaseLibrary) | toElasticAndToBaseAreInverse2down | S6-2 | NOT_STATED | NOT_STATED |
| 29 | rebase.spec | RebaseWrapper (RebaseLibrary) | toElasticAndToBaseAreInverse2up | S6-2 | NOT_STATED | NOT_STATED |
| 30 | rebase.spec | RebaseWrapper (RebaseLibrary) | toElasticAndToBaseAreInverse0ElasticEdgeCase | S6-2 | NOT_STATED | NOT_STATED |
| 31 | rebase.spec | RebaseWrapper (RebaseLibrary) | toElasticAndToBaseAreInverse0BaseEdgeCase | S6-2 | NOT_STATED | NOT_STATED |
| 32 | strategy.spec | SymbolicStrategy (SymbolicStrategy) | integrityHarvest | S6-4 | VERIFIED | NO_FINDING |
| 33 | strategy.spec | SymbolicStrategy (SymbolicStrategy) | integrityWithdraw | S6-4 | VERIFIED | NO_FINDING |
| 34 | strategy.spec | SymbolicStrategy (SymbolicStrategy) | integrityExit | S6-4 | VERIFIED | NO_FINDING |
| 35 | strategy.spec | SushiStrategyHarness (SushiStrategy) | integrityHarvest | S6-4 | VERIFIED | NO_FINDING |
| 36 | strategy.spec | SushiStrategyHarness (SushiStrategy) | integrityWithdraw | S6-4 | VERIFIED | NO_FINDING |
| 37 | strategy.spec | SushiStrategyHarness (SushiStrategy) | integrityExit | S6-4 | VERIFIED | NO_FINDING |

## Source integrity and validation

- Original property declaration body is copied literally into each N.spec; the only additions are provenance and required CVL closure (methods/using/definitions, ghost/hook, and dispatcher helper as needed).
- Historical Solidity lines are copied unchanged, with original paths and line ranges annotated inside N.sol and metadata.
- No CVL2 migration, synthetic historical commits, Prover reproduction, or edits to original source files.
- Result, Detection Outcome and Bug Label are separate judgments; especially UNMAPPED for the constrained non-reversion probe.
- Each incomplete example has an N.txt referencing the historical unresolved import closure.
- Official validation logs and git SHA/diff checks are recorded in docs/spec_catalog_project_20_validation.log.

## Formal-result distribution

{"('VERIFIED', 'NO_FINDING')": 12, "('VERIFIED', 'FINDING')": 3, "('NOT_STATED', 'NOT_STATED')": 22}
