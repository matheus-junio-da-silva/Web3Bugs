# Project 5 — Aave-StarkNet L1-L2 Bridge Spec Catalog

This document records the reviewed completion state of the Certora property catalog for Project 5.

## Coverage

- `specs/bridge.spec`: **13 active properties**.
- `specs/setup.spec`: **2 active invariants**.
- `specs/bridgeConstIndex.spec`: **2 active rules**.
- Total active property instances: **17**.
- Complete examples: **0**.
- Incomplete examples: **17**.
- Bug Label relationship rows: **17**.

The rule `afterCancellationStartMustSucceed` is inside a block comment and is not active.

The report's statement that community participants submitted 165 correctness properties is not the active-property count of the final selected spec snapshot. The historical verification commit contains exactly `bridge.spec`, `bridgeConstIndex.spec`, `setup.spec`, and `erc20.spec`; `erc20.spec` has no active `rule` or `invariant`. The catalog therefore counts the 17 active property declarations in the final supplied/historical spec set rather than attempting to reconstruct participant submissions that are not present in the selected project snapshot.

Top-level `use invariant` statements are not counted as new property instances. Under Certora import/use semantics, `use invariant X` selects an invariant declared in an imported spec for verification; it does not implicitly add `requireInvariant X` to every rule. This also matches the existing Project 4 convention: an invariant declaration is cataloged once, while an imported invariant is included as a dependency of another example only when the selected property's helper closure explicitly reaches it, such as `setupTokens -> requireInvariant ATokenAssetPair`.

## Independent review corrections

A second adversarial review found and corrected several material issues from the initial Project 5 extraction:

- The first extraction treated the top-level `use invariant alwaysUnSent` and `use invariant ATokenAssetPair` statements as if both invariants were dependencies of every rule in `bridge.spec`. That caused oversized extracted specs and pulled in many unrelated methods. The 17 extracted specs were rebuilt with property-specific recursive dependency closures.
- Missing `tokenBalanceOf`, `withdrawMessageStatus`, and `bridgeRewardsMessageStatus` were initially described too broadly as dependencies of the missing `erc20.spec`. Upstream evidence shows these functions are implemented by the historical `BridgeHarness.sol`. The missing `erc20.spec` instead contains generic ERC20 dispatcher declarations such as `balanceOf`, `transfer`, `transferFrom`, and `approve`. All incomplete notes were corrected.
- The initial catalog assigned the aggregate report `✔*` results to the `bridgeConstIndex.spec` instances of `depositWithdrawReversed` and `integrityOfDepositExpanded`. This was too strong. The report does not identify which same-named source instance receives the aggregate result, and its footnotes describe mixed arbitrary-index/specific-index proof scopes. Both duplicate source instances now remain `NOT_STATED`.
- Several semantic descriptions were narrowed to what the executable assertions actually prove. In particular, `integrityOfWithdraw` does not prove an exact positive payout; `initializeIntegrity` proves an equivalence/consistency condition rather than existence of registration; `dynamicToStaticInversible3` uses a one-sided subtraction rather than an absolute-error expression; and `cannotCancelDepositAndGainBothTokens` never asserts on its final `staticBalance3`.
- The supplied `Bridge.sol` was found to be a later source revision than the formal-verification package. Every `.sol` artifact now explicitly warns that it is available production-code context, not the missing historical `BridgeHarness` target.
- A later outcome review corrected `cannotCancelDepositAndGainBothTokens` from `FINDING` to `ACCEPTED_BEHAVIOR`: its formal counterexample remains `VIOLATED`, but Aave explicitly treats timely Starknet proof generation as an accepted bridge assumption. `shouldRevertInitializeTokens` remains `FINDING` because the report still presents it as a Low-severity issue; its O1 classification is kept separate as a privileged-configuration scope classification.
- A provenance audit found that reduced extracted `methods { ... }` blocks used original method declarations but did not cite the original `setup.spec` brace lines. Lines 33 (`methods {`) and 136 (`}`) were added to every affected extracted-header, `.md`, and CSV provenance range. After correction, every non-header CVL line in all 17 extracted specs is traceable to a declared original source line.

## Dependency status

All **17** examples remain incomplete under the dataset's snapshot-completeness rule.

The supplied project snapshot is missing the historical verification artifacts documented by the report and confirmed by the public verification package, including:

- `BridgeHarness.sol`;
- `BridgeL2Harness.sol`;
- `SymbolicLendingPoolL1.sol`;
- `DummyERC20UnderlyingA_L1.sol` and `DummyERC20UnderlyingB_L1.sol`;
- `ATokenWithPoolA_L1.sol` and `ATokenWithPoolB_L1.sol`;
- `StaticATokenA_L2.sol` and `StaticATokenB_L2.sol`;
- `DummyERC20RewardToken.sol`;
- the historical `IncentivesControllerMock_L1.sol` and related harness interfaces/implementations;
- `specs/erc20.spec`.

The selected snapshot contains similarly named production mocks, interfaces, and Cairo contracts, but they are not the historical verification harnesses and are not silently substituted.

A full exact-filename search across the supplied PropertyGPT tree found no copy of the project-specific historical harnesses. Other projects contain unrelated `erc20.spec` files; none is imported as a replacement for the missing Project 5 file. A historical cross-check of commit `4c010c18` confirms that the missing Project 5 `certora/specs/erc20.spec` contains a `methods {}` block but no active `rule` or `invariant`, so its absence does not hide additional property instances from the 17-property coverage count.

## Upstream historical cross-check

The public Aave Starknet Bridge repository contains the formal-verification package at commit:

`4c010c18b08703e4f367db1e0c642c76c25e551b` — Certora + Community Formal Verification.

The three supplied PropertyGPT specs are byte-identical to that package:

- `bridge.spec`: `dd9887921f3d300dde75894ae94130120920f14619dee3a5c0a328f802f6acd6`
- `bridgeConstIndex.spec`: `7b671e17cc075e028b28be6295a1b00bfa72cc7b6edb693429e9b029f3472415`
- `setup.spec`: `5c75fdca473b3a88c8aeff89b936d09eeaa3de42f3116e0d4968aa7242b7ae89`

The report PDF is also byte-identical:

- `be9aaca56abd09d2b2c30906a433e7897b5f0e24549933f841ac986b168974f5`

This cross-check is evidence only. Recovered upstream files were **not** copied into `contracts/5` or the extracted examples, because dependency completeness is defined against the supplied PropertyGPT snapshot.

The upstream verification scripts explicitly use:

- target: `BridgeHarness`;
- `--verify BridgeHarness:certora/specs/bridge.spec` or `bridgeConstIndex.spec`;
- `solc8.10`;
- `--optimistic_loop`;
- `--loop_iter 3`;
- settings `-mediumTimeout=700,-depth=12`;
- explicit links between `BridgeHarness`, `BridgeL2Harness`, the reward token, AToken mocks, symbolic lending pool, and incentives-controller mock.

The script's prose comment later says `loop_iter 2`, while the executable command uses `--loop_iter 3` and the report describes three-iteration loop coverage. The catalog follows the executable flag/report and records the comment as stale/inconsistent documentation rather than silently reconciling it.

## Source-version drift

The supplied Project 5 production `contracts/l1/Bridge.sol` is **not** byte-identical to the Bridge source in the upstream formal-verification package.

Supplied snapshot SHA-256:

`7fae97efd775387db913f84fe9c0fee143d37275a36707071a51f743664948be`

That exact source matches upstream commit `71be8e44aa7b35ae0c63fd08d3aebc338a6ac0e6` dated 2022-11-18, later than the report's August–October verification period.

Material differences from the formal-verification package include:

- deposit ceiling accounting changed from `scaledBalanceOf(address(this)) + amount` to `balanceOf(address(this)) + amount`;
- token approval changed from `approve` to `safeApprove`;
- GPv2SafeERC20 usage was replaced by the local SafeERC20 helper.

Therefore the `.sol` excerpts are useful semantic/context evidence but are not claimed to be the exact implementation bytes used by the reported proof. Formal `Result` values come only from report evidence.

## Formal results

Across the **17 active source property instances** after conservative duplicate-instance attribution:

- VERIFIED: **6**
- VIOLATED: **4**
- NOT_STATED: **7**

Audit interpretation:

- FINDING: **3**
- NO_FINDING: **6**
- ACCEPTED_BEHAVIOR: **1**
- INCONCLUSIVE: **0**
- NOT_STATED: **7**

Explicit violated properties tied to report issues:

- `dynamicToStaticInversible2` — ray-math rounding/invertibility;
- `cancelAfterDepositGivesBackExactAmount` — the same rounding issue in the cancellation flow;
- `cannotCancelDepositAndGainBothTokens` — cancellation after a successful modeled L2 deposit;
- `shouldRevertInitializeTokens` — duplicate L2 token identifier accepted during initialization.

The report's `❌` notation means violated under one of the tested versions. It is not treated as proof that the later supplied `Bridge.sol` snapshot still violates the property.

## Duplicate source properties and aggregate report entries

Two property names occur in both `bridge.spec` and `bridgeConstIndex.spec`:

- `depositWithdrawReversed`;
- `integrityOfDepositExpanded`.

The report presents one `✔*` entry for each concept, not a source-file-specific status for both instances.

For `depositWithdrawReversed`, report footnotes say:

- the underlying non-conservation comes from violated rule #2 and is bounded;
- the third assertion was proved for specific liquidity-index values;
- the other two assertions were proved for arbitrary liquidity-index values;
- `address2uint256` is modeled as a one-to-one conversion.

For `integrityOfDepositExpanded`, report footnotes say:

- the recipient is assumed not to be a contract;
- `fromUnderlyingAsset=false` was verified for specific liquidity-index values;
- the other branch used arbitrary liquidity-index values.

Those mixed scopes do not map cleanly to one whole source instance. In addition, the two `integrityOfDepositExpanded` source bodies materially differ in their `fromUnderlyingAsset=false` aToken-delta expression. For fidelity, all four duplicate source instances are `NOT_STATED`; the aggregate `✔*` evidence remains documented in their `.md` files.

## Findings related

The report contains four main issues:

1. **Token address duplicates not checked on initialize.** The detecting property is `shouldRevertInitializeTokens`. Its technical property relationship is S2-3. The final dataset finding remains O1 because the report/Aave response frames duplicate initialization as a trusted-governance configuration assumption.
2. **Front running of withdrawal.** The L2→L1 payload did not bind `toUnderlyingAsset`, allowing an unprivileged caller to choose the withdrawal token form. No cataloged source property is explicitly named for this issue. The final finding is SE-4.
3. **Dynamic/static transformation not precisely reversible.** The report attributes this to ray-math rounding and names `dynamicToStaticInversible2` plus `cancelAfterDepositGivesBackExactAmount`. The final finding is L2.
4. **Cancellation does not check successful L2 deposit completion.** The report names `cannotCancelDepositAndGainBothTokens`. Its technical property relationship is S4-1. The final finding is O6 because Aave explicitly treats timely Starknet proof generation as a bridge assumption; for the same documented reason, the property Detection Outcome is `ACCEPTED_BEHAVIOR` even though its formal Result is `VIOLATED`.

`Detection Outcome` is not mechanically derived from the final finding label. `dynamicToStaticInversible2`, `cancelAfterDepositGivesBackExactAmount`, and `shouldRevertInitializeTokens` remain `FINDING` because the report presents them as issues; `cannotCancelDepositAndGainBothTokens` is `ACCEPTED_BEHAVIOR` because Aave explicitly frames the violated behavior as an accepted Starknet-proof timing assumption. The O1/O6 finding labels remain a separate Web3Bugs classification view.

## Bug Label mapping and UNMAPPED

Property-level relationships after review:

- L2: **3** — conversion precision/rounding rules.
- S2-3: **1** — duplicate L2 token identifier.
- S3-2: **4** — state/linkage/list consistency properties.
- S4-1: **1** — cross-domain deposit/cancellation business-flow atomicity.
- S6-4: **6** — deposit/withdraw/refund balance-accounting relationships.
- UNMAPPED: **2**.

The two UNMAPPED properties are:

- `balanceOfUnderlyingAssetChanged` — a generic mutation/whitelist diagnostic probe;
- `alwaysUnSent` — a verification-model invariant over BridgeHarness message-status flags.

## Important semantic limitations by property

- `integrityOfWithdraw`: the selected payout balance is only required not to decrease; equality is allowed. It does not prove a positive or exact payout.
- `balanceOfUnderlyingAssetChanged`: diagnostic method-mutation classification, not a standalone security requirement.
- `depositWithdrawReversed`: underlying/aToken restoration conditions apply only when `fromUA == toUA`; static balance restoration is unconditional.
- `dynamicToStaticInversible3`: checks the literal one-sided expression `dynm - amount <= bound`, not an absolute error.
- `underlying2ATokenConsistency`: checks equivalence under a zero/nonzero-status guard; it is not an existence proof.
- `initializeIntegrity`: both sides of the final equivalence may be false, so it proves consistency rather than successful registration of the symbolic pair.
- `cancelAfterDepositGivesBackExactAmount`: for an underlying-origin deposit, the encoded post-state keeps underlying down by `amount` and aToken up by `amount`; this is the literal property and is not rewritten.
- `cannotCancelDepositAndGainBothTokens`: `staticBalance3` is read but never asserted. A failure proves an aToken refund after a static mint was observed; the rule alone does not prove the user still holds both token balances in the final state.
- `integrityApprovedTokensAndTokenData`: the ghost counts matching Sstore writes, not distinct registered identifiers, and the invariant filter excludes initialize.
- `shouldRevertInitializeTokens`: specifically tests duplicate L2 token identifiers in the constructed arrays; it is not generalized to every possible L1/L2 duplication case.
- `ATokenAssetPair`: a conditional consistency invariant, not a guarantee that every symbolic asset has a registered AToken.

## Assumptions and report-version qualifiers

The report explicitly states that:

- Cairo/L2 contracts were not verified directly;
- L2 behavior was replaced by simplified Solidity mocks;
- the asynchronous messaging mechanism was bypassed by immediate modeled calls;
- messaging correctness and resistance to fake-message injection were assumed;
- surrounding modeled contracts were assumed not to call back into `Bridge.sol`;
- liquidity indexes were assumed to be at least one RAY;
- underlying/aToken/static-aToken triplet relationships were preserved as modeling assumptions;
- loops were bounded/unrolled, so violations needing more iterations may be missed;
- `✔*` marks simplified proofs.

The report itself contains multiple commit references that are preserved rather than merged: the Summary names `8302ab87` as the latest reviewed commit; the Community section also references `8302ab87`; the Additional Formal Properties section references `58cbfbf7`. No source-instance result is inferred solely by choosing one of these commit references.

## Reproduction limitations

Exact historical rerun from the supplied Project 5 snapshot is not possible because the historical target/harness tree, linked mocks, run scripts, and `erc20.spec` are absent.

The supplied production Solidity also imports external `@aave/core-v3` packages not bundled in the Project 5 snapshot, and its `Bridge.sol` is a later revision than the formal package.

Upstream recovery establishes what the historical files and configuration were, but those files are deliberately not imported into the dataset snapshot. Thus every Project 5 example correctly remains `incomplete`.

CVL2 migration remains outside this cataloging step.

## Validation

The final review validates:

- 17 active source declarations and exactly 17 Project 5 examples;
- the commented `afterCancellationStartMustSucceed` remains excluded;
- every selected property body is a literal substring of its original source spec;
- every incomplete example has `.spec`, `.sol`, `.md`, and `.txt`;
- property-specific CVL closures no longer import top-level `use invariant` statements as unrelated dependencies;
- standalone invariants are not duplicated inside their own extracted specs;
- missing-helper ownership is documented against the historical BridgeHarness instead of incorrectly assigning it to `erc20.spec`;
- duplicate source instances do not inherit aggregate `✔*` report status;
- source-spec hashes still match the original PropertyGPT snapshot;
- no upstream-recovered harness source was copied into `contracts/5`.

Required structural validators were executed after the review.

The literal commands requested by the workflow with the `python` executable were attempted first, but this host does not provide a `python` alias (`python: command not found`). The equivalent commands were then executed with the available `python3` interpreter:

- `python3 scripts/check_specs.py .` — **PASS**: 132 spec examples and 136 Bug Label relationships are structurally consistent.
- `python3 scripts/check_contests_csv.py .` — **PASS**.
- `python3 scripts/check_contracts.py .` — **PASS**.
- Additional adversarial audit — **PASS**: 17/17 active Project 5 declarations accounted for; historical `erc20.spec` confirmed to contain no additional rules/invariants; 17/17 selected property bodies preserved literally; every non-header extracted CVL line is covered by declared original source ranges; all declared Solidity excerpt ranges match the copied snapshot exactly; all 17 property-specific closures contain the available recursive CVL helper dependencies; copied snapshot integrity preserved; no unrelated top-level `use invariant` leakage; duplicate aggregate results kept conservative; and `cannotCancelDepositAndGainBothTokens` outcome reviewed as `ACCEPTED_BEHAVIOR` from the explicit Aave bridge assumption.

The validators check structure and catalog consistency; they do not rerun the Certora Prover.

## Catalog locations

- Index: `results/spec/spec_buglabel.csv`
- Examples: `results/spec/incomplete/5/`
- Report transcript: `reports/5.md`
- Preserved PDF: `resources/5/Formal-Verification-Report-of-Aave-Starknet-Bridge-3.pdf`
- Copied supplied snapshot: `contracts/5/`
