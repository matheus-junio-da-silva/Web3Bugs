# Project 19 — Origin OUSD — ATLAS Catalog

## Scope and provenance

- PropertyGPT upstream project: certora_projects/ousd; upstream commit 687f654c679ed45ab127b7949e2a29c8f5e491b9.
- Source snapshot: `contracts/19/` (all non-PDF original files preserved byte-identically; PDF in resources/19).
- Historical report: `resources/19/OriginFeb2021.pdf`, nine pages; work January 10–15, 2021; report-reviewed commit 5c702edbefb451287805918c3275535c11654074.
- The original Web3Bugs dataset also has unrelated Connext at repository-root contracts/19 and reports/19.md. Only `Web3Bugs-certora/` paths are modified.
- 36 active CVL declarations in nine spec files; 37 target-specific examples because sanity.spec has distinct OUSD and VaultCore runs. Duplicate math rule names count as two active textual declarations, not silently collapsed.
- Commented-out preserveSumOfRebasingCredits and preserveNonRebasingSupply in ousd.spec are excluded.

## Counts

- Examples: 37; 2 complete, 35 incomplete.
- Results: NOT_STATED=29, VIOLATED=4, VERIFIED=4.
- Detection Outcomes: NOT_STATED=29, FINDING=2, NO_FINDING=4, ACCEPTED_BEHAVIOR=2.
- Additional CSV mapping rows: 37 (one defensible label relationship per material example).

## Snapshot-dependent closure

All real OUSD/Vault/VaultAdmin Solidity compilation graphs rely on unvendored @openzeppelin packages. The source includes npm package manifests but not installed package content; this is source missing-dependency evidence, not simply a missing solc binary. It prevents an unqualified complete classification for those examples. The two pure arithmetic math.spec rules depend only on present CVL definitions and Dummy.sol; compile/Prover readiness and duplicate rule identifiers are separate concerns.

The OUSDHarness source references a private MAX_SUPPLY and changes it via applyHarnesses.sh; that script also comments-out the ERC20 initializer and injects a ratio condition. OUSDHarnessSimplified returns a hard-coded creditsPerToken ratio; it is not synonymous with production OUSD. The runOUSDSpec scripts select OUSDHarness plus VaultCore, while privileged scripts select OUSD/VaultCore/VaultAdmin separately.

The generic Privileged.spec has no corresponding run script/target. VaultAdmin compares three callers, and the other privileged variants compare two: neither identifies specific allowed addresses. The report does not establish independent outcomes for these rules.

## PDF finding reconciliation

| Historical report | PDF pages | Proper interpretation |
| --- | --- | --- |
| Stablecoin valuation can exceed $1 backing; vault solvency | 2, 9 | Vault/strategy dependency; solvency is writing-mark/not specified; do not attribute to arbitrary token rule |
| Governor can withdraw assets backing OUSD | 2 | Fixed historically by limiting to unsupported assets; no direct CVL rule in this catalog reproduces it |
| Max supply may be exceeded via rounded changeSupply | 2, 7 | PDF property 1 crossed; fix added require; not a fresh run |
| Nonadditive burn and mint due to credit rounding | 2, 9 | PDF properties 11–12 crossed; accepted small deviation/intended tradeoff, respectively |
| Zero-amount burn changes credits | 3, 9 | PDF property 13 crossed; fix recorded historically |
| Fee splits, mint threshold, stablecoin depeg, dust redemption | 3 | Historical findings not misattributed to absent CVL assertions |
| Mint/burn return mismatches | 4 | Historical low-severity fix, not separately tested by a cataloged property |

The PDF states property 6 (total-supply **equality**) was violated, but active totalSupplyIntegrity uses **>=**; therefore its individual Result is NOT_STATED rather than importing a violation of a different predicate. PDF property 8 (balance-update effects), property 9 solvency and property 10 rebasing monotonicity are not verified, and must not be projected onto related test harnesses.

## Property-by-property audit

| # | Original spec | Original lines | Property | Historical target | Status | Result | Detection Outcome | Label | Missing deps |
|---:|---|---|---|---|---|---|---|---|---:|
| 1 | math.spec | 24-35 | mathOfChangeSupply | Dummy | complete | NOT_STATED | NOT_STATED | L2 | 0 |
| 2 | math.spec | 38-49 | mathOfChangeSupply | Dummy | complete | NOT_STATED | NOT_STATED | L2 | 0 |
| 3 | ousd.spec | 29-30 | totalSupplyIsBelowMaxSupply | OUSDHarness | incomplete | VIOLATED | FINDING | S6-4 | 5 |
| 4 | ousd.spec | 33-39 | neverRevert_BalanceOf | OUSDHarness | incomplete | VERIFIED | NO_FINDING | SC | 5 |
| 5 | ousd.spec | 49-50 | rebasingCreditsPerTokenMustBeGreaterThan0 | OUSDHarness | incomplete | VERIFIED | NO_FINDING | S6-4 | 5 |
| 6 | ousd.spec | 54-62 | totalSupplyIntegrity | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 7 | ousd.spec | 66-77 | senderCannotDecreaseOthersBalance | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S5-1 | 5 |
| 8 | ousd.spec | 79-90 | changesRebaseState | OUSDHarness | incomplete | VERIFIED | NO_FINDING | S3-2 | 5 |
| 9 | ousd.spec | 96-119 | reverseOptInThenOut | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 10 | ousd.spec | 125-141 | additiveMint | OUSDHarness | incomplete | VIOLATED | ACCEPTED_BEHAVIOR | L2 | 5 |
| 11 | ousd.spec | 143-152 | mintDoesNotDecreaseBalance | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 12 | ousd.spec | 154-163 | zeroMintDoesNotIncreaseBalance | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | L2 | 5 |
| 13 | ousd.spec | 169-186 | additiveBurn | OUSDHarness | incomplete | VIOLATED | ACCEPTED_BEHAVIOR | L2 | 5 |
| 14 | ousd.spec | 188-197 | burnDoesNotIncreaseBalance | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 15 | ousd.spec | 199-208 | zeroBurnDoesNotDecreaseBalance | OUSDHarness | incomplete | VIOLATED | FINDING | L2 | 5 |
| 16 | ousd.spec | 214-227 | transferCheckPreconditions | OUSDHarness | incomplete | VERIFIED | NO_FINDING | SC | 5 |
| 17 | ousd.spec | 271-275 | nonRebasingToNonRebasingTransferCheckEqualRatiosSpecific | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 18 | ousd.spec | 278-281 | nonRebasingToNonRebasingTransferCheckEqualRatiosGeneral | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 19 | ousd.spec | 293-297 | rebasingToRebasingTransferSimplified | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 20 | ousd.spec | 299-302 | rebasingToRebasingTransferGeneral | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 21 | ousd.spec | 304-308 | transferIntegrityCheck | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 22 | ousd.spec | 310-317 | rebasingToRebasingTransfer | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 23 | ousd.spec | 344-346 | optingInAndOutSyncdWithNonRebasingState | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S3-2 | 5 |
| 24 | ousd.spec | 348-366 | isRebasingPredicateSynchronized | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S3-2 | 6 |
| 25 | ousd.spec | 368-377 | onceRebaseStateWasSelectedCannotUnsetIt | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S3-2 | 5 |
| 26 | ousdExtras.spec | 26-27 | rebasingCreditsPerTokenMustBeGreaterThan0 | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 27 | ousdExtras.spec | 29-65 | additiveBurnRanges | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | L2 | 5 |
| 28 | ousdSum.spec | 7-33 | changesOne | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 29 | ousdSum.spec | 35-65 | changesTwo | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 30 | ousdSum.spec | 67-86 | sum1Test | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | UNMAPPED | 5 |
| 31 | ousdSum.spec | 88-117 | sum2Test | OUSDHarness | incomplete | NOT_STATED | NOT_STATED | S6-4 | 5 |
| 32 | Privileged.spec | 12-31 | privilegedOperation | UNSPECIFIED | incomplete | NOT_STATED | NOT_STATED | UNMAPPED | 1 |
| 33 | PrivilegedOUSD.spec | 11-30 | privilegedOperation | OUSD | incomplete | NOT_STATED | NOT_STATED | UNMAPPED | 4 |
| 34 | PrivilegedVault.spec | 11-30 | privilegedOperation | VaultCore | incomplete | NOT_STATED | NOT_STATED | UNMAPPED | 5 |
| 35 | PrivilegedVaultAdmin.spec | 1-26 | privilegedOperation | VaultAdmin | incomplete | NOT_STATED | NOT_STATED | S5-1 | 5 |
| 36 | sanity.spec | 1-6 | sanity | OUSD | incomplete | NOT_STATED | NOT_STATED | UNMAPPED | 4 |
| 37 | sanity.spec | 1-6 | sanity | VaultCore | incomplete | NOT_STATED | NOT_STATED | UNMAPPED | 5 |

## Validation

- Validation commands and real exit codes are recorded separately after generating the final commit; the source was cataloged without executing historical Certora Prover.
- Original source fidelity is checked separately from generated documentation and from the CSV structural checks.
