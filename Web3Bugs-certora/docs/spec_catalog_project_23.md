# Project 23 — Radicle Drips Historical CVL Catalog

## Source provenance
PropertyGPT main commit `687f654c679ed45ab127b7949e2a29c8f5e491b9`. Source src tree `344f4f303849c1337ff0369da66ab840a0a9f8a8`; specs tree `d7d6012139dbcdb76ce0430e48ed4fe67208aea3`; original PDF blob `cdadcf1b83b3dc1bfa267d958d8dfde739fd5154`; PDF SHA256 `457414f284b91c6bc6b1f7307f71252f0a393f6d954bcc4662e9b65647278e6a`. Preserved byte-for-byte in contracts/23/src, contracts/23/specs and resources/23.

## Active declaration inventory
| Original spec | Active CVL declarations | Excluded |
|---|---:|---|
| DripsHub.spec | 12 | two commented invariants |
| DripsHubBackup.spec | 6 | two commented invariants |
| Reserve.spec | 5 | none |
| SlotTester.spec | 1 | none |
| Splits.spec | 17 | one commented sanity rule |
| Splits2.spec | 5 | none |

**46 original active properties**, all incomplete against snapshot dependencies, independent of original result. CVL preserved literally without CVL2 migration. Repeated front-run property names in Splits/Splits2 are distinct declarations and not deduplicated. No CVT or target harness is invented.

## Historical proof result: only Splits.sol
The original report (December 2022 to January 2023; reviewed commit 6fe9d38) expressly limits formal scope to Splits.sol, with 15 named verified rules, one violated informational-rounding rule, and one timed-out general-case rule. The remaining 29 properties (DripsHub, backup, Reserve, SlotTester, Splits2) have NOT_STATED result. The timed-out case is NOT_STATED with INCONCLUSIVE outcome, not VERIFIED. The rounding issue yields VIOLATED/FINDING (informational finding), including the team's explicit design/economics response. Three constrained split front-running variants verified in Splits.spec are not evidence for Splits2.spec.

## Assumptions & soundness
- The prover unrolled loops at most twice; behavior requiring longer loops was outside proven scope.
- Some rules assume correctly set receiver weights (sum at most 1,000,000) based on _assertSplitsValid() logic.
- Sums of balances/transfers were bounded below 2^128.
- General front-running rule timed out; specialized identity cases were checked independently.
- External contracts, dummy ERC20s, CVT-generated internal-operation wrappers, and the DripsHubHarness / UpdateReceiverStatesHarness / ReserveHarness are not in the six Solidity files; their generated verification semantics cannot be recovered from the production files alone.
- Diagnostic sanity and unrestricted-method-mutation rules are UNMAPPED; apparent successful assertions in a soundness-limited model must not be called newly proved.

## Per-rule matrix
| Example | Original spec range | Property | Label | Result | Outcome | Missing reason |
|---:|---|---|---|---|---|---|
| 1 | DripsHub.spec:343-353 | sanity | UNMAPPED | NOT_STATED | NOT_STATED | Original using DripsHubHarness as DH requires missing DripsHubHarness.so… |
| 2 | DripsHub.spec:356-361 | sanitySimple | UNMAPPED | NOT_STATED | NOT_STATED | Original using DripsHubHarness as DH requires missing DripsHubHarness.so… |
| 3 | DripsHub.spec:364-404 | asTimePassesReceivableDripsGrow | S6-4 | NOT_STATED | NOT_STATED | Original using DripsHubHarness as DH requires missing DripsHubHarness.so… |
| 4 | DripsHub.spec:407-443 | cyclesAdditivity | S6-4 | NOT_STATED | NOT_STATED | Original using DripsHubHarness as DH requires missing DripsHubHarness.so… |
| 5 | DripsHub.spec:448-496 | updateReceiverStatesEquivalency | S6-4 | NOT_STATED | NOT_STATED | Original using DripsHubHarness as DH requires missing DripsHubHarness.so… |
| 6 | DripsHub.spec:500-565 | settingSameDripsDoesntChangeReceivableDrips | S6-4 | NOT_STATED | NOT_STATED | Original using DripsHubHarness as DH requires missing DripsHubHarness.so… |
| 7 | DripsHub.spec:567-605 | whoChangedBalanceOfUserId | UNMAPPED | NOT_STATED | NOT_STATED | Original using DripsHubHarness as DH requires missing DripsHubHarness.so… |
| 8 | DripsHub.spec:608-635 | whoChangedBalanceOfToken | UNMAPPED | NOT_STATED | NOT_STATED | Original using DripsHubHarness as DH requires missing DripsHubHarness.so… |
| 9 | DripsHub.spec:637-659 | receiverCannotLoseMoney | S6-4 | NOT_STATED | NOT_STATED | Original using DripsHubHarness as DH requires missing DripsHubHarness.so… |
| 10 | DripsHub.spec:688-766 | integrityOfPast | S6-4 | NOT_STATED | NOT_STATED | Original using DripsHubHarness as DH requires missing DripsHubHarness.so… |
| 11 | DripsHub.spec:769-785 | integrityOfSplit | S6-4 | NOT_STATED | NOT_STATED | Original using DripsHubHarness as DH requires missing DripsHubHarness.so… |
| 12 | DripsHub.spec:788-806 | integrityOfCollectAll | S6-4 | NOT_STATED | NOT_STATED | Original using DripsHubHarness as DH requires missing DripsHubHarness.so… |
| 13 | DripsHubBackup.spec:312-322 | sanity | UNMAPPED | NOT_STATED | NOT_STATED | Original using UpdateReceiverStatesHarness as DH requires missing Update… |
| 14 | DripsHubBackup.spec:326-362 | whoChangedBalanceOfUserId | UNMAPPED | NOT_STATED | NOT_STATED | Original using UpdateReceiverStatesHarness as DH requires missing Update… |
| 15 | DripsHubBackup.spec:365-389 | whoChangedBalanceOfToken | S3-2 | NOT_STATED | NOT_STATED | Original using UpdateReceiverStatesHarness as DH requires missing Update… |
| 16 | DripsHubBackup.spec:392-490 | singleUserTimeUpdateNotChangingOtherUserBalance | S6-4 | NOT_STATED | NOT_STATED | Original using UpdateReceiverStatesHarness as DH requires missing Update… |
| 17 | DripsHubBackup.spec:493-510 | helperTest | UNMAPPED | NOT_STATED | NOT_STATED | Original using UpdateReceiverStatesHarness as DH requires missing Update… |
| 18 | DripsHubBackup.spec:513-562 | unrelatedUserBalanceNotChangingParametric | S6-4 | NOT_STATED | NOT_STATED | Original using UpdateReceiverStatesHarness as DH requires missing Update… |
| 19 | Reserve.spec:53-58 | sanity | UNMAPPED | NOT_STATED | NOT_STATED | ReserveHarness, DummyERC20Impl, DummyERC20A, DummyERC20B, getDeposited/g… |
| 20 | Reserve.spec:61-81 | whoChangedUserState | UNMAPPED | NOT_STATED | NOT_STATED | ReserveHarness, DummyERC20Impl, DummyERC20A, DummyERC20B, getDeposited/g… |
| 21 | Reserve.spec:84-116 | totalMoneyIsConstant | S6-4 | NOT_STATED | NOT_STATED | ReserveHarness, DummyERC20Impl, DummyERC20A, DummyERC20B, getDeposited/g… |
| 22 | Reserve.spec:120-170 | tokensNonInterference | S3-2 | NOT_STATED | NOT_STATED | ReserveHarness, DummyERC20Impl, DummyERC20A, DummyERC20B, getDeposited/g… |
| 23 | Reserve.spec:175-195 | depositedBalanceRepresentationIsCorrect | S6-4 | NOT_STATED | NOT_STATED | ReserveHarness, DummyERC20Impl, DummyERC20A, DummyERC20B, getDeposited/g… |
| 24 | SlotTester.spec:1-31 | whoChangedBalanceOfToken | UNMAPPED | NOT_STATED | NOT_STATED | The snapshot does not include SlotTester target or getters getPausedSlot… |
| 25 | Splits.spec:26-32 | correctnessOfSplitResults | S6-4 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 26 | Splits.spec:38-55 | correctnessOfSplit | S6-4 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 27 | Splits.spec:60-68 | integrityOfCollect | S6-4 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 28 | Splits.spec:72-80 | revertCharacteristicsOfCollect | L8 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 29 | Splits.spec:86-95 | correctnessOfGive | S6-4 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 30 | Splits.spec:100-111 | splittableOfNonReceiverNotAffectedByGive | S3-2 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 31 | Splits.spec:118-133 | correctnessOfHashSplits | LA | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 32 | Splits.spec:143-209 | integrityOfSplit | S6-4 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 33 | Splits.spec:216-260 | assetsDoNotInterfereEachOther | S3-2 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 34 | Splits.spec:268-303 | moneyNotLostOrCreatedDuringSplit | S6-4 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 35 | Splits.spec:311-347 | sameReturnOfSplitAndSplitResults | S6-4 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 36 | Splits.spec:368-406 | splitReceiverShouldGetMoneyUponSplit | L2 | VIOLATED | FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 37 | Splits.spec:413-456 | equalSplitWeightsResultEqualSplittableIncrease | S6-4 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 38 | Splits.spec:477-523 | cannotFrontRunSplitGeneralCase | SE-1 | NOT_STATED | INCONCLUSIVE | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 39 | Splits.spec:532-582 | cannotFrontRunSplitDifferentUsers | SE-1 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 40 | Splits.spec:586-630 | cannotFrontRunSplitTwoSameUsers | SE-1 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 41 | Splits.spec:634-676 | cannotFrontRunSplitThreeSameUsers | SE-1 | VERIFIED | NO_FINDING | The abstract Splits.sol exposes internal _split, _splitResults, _splitta… |
| 42 | Splits2.spec:7-53 | cannotFrontRunSplitGeneralCase | SE-1 | NOT_STATED | NOT_STATED | Distinct Splits2.spec uses absent generated CVT wrappers and receiver-ar… |
| 43 | Splits2.spec:62-112 | cannotFrontRunSplitDifferentUsers | SE-1 | NOT_STATED | NOT_STATED | Distinct Splits2.spec uses absent generated CVT wrappers and receiver-ar… |
| 44 | Splits2.spec:116-160 | cannotFrontRunSplitTwoSameUsers | SE-1 | NOT_STATED | NOT_STATED | Distinct Splits2.spec uses absent generated CVT wrappers and receiver-ar… |
| 45 | Splits2.spec:164-206 | cannotFrontRunSplitThreeSameUsers | SE-1 | NOT_STATED | NOT_STATED | Distinct Splits2.spec uses absent generated CVT wrappers and receiver-ar… |
| 46 | Splits2.spec:211-235 | revertCharacteristicsOfSplit | L8 | NOT_STATED | NOT_STATED | Distinct Splits2.spec uses absent generated CVT wrappers and receiver-ar… |

## Reproduction
The generator copies all six src and all six spec files, extracts active declaration blocks using comment-aware brace matching, produces .spec, .sol, .md and .txt for each incomplete example, and performs immediate literal-property/source comparisons. The independent auditor checks source-to-destination blobs, CVL lines, snippets and CSV. Then run the three repository Python validators and git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD. The catalog is documentary, not a new Certora Prover run.
