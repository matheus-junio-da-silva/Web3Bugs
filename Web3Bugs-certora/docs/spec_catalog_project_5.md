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

## Per-example consolidated semantic audit (Boreal review — 2026-10-16)

This section consolidates the five explicit semantic checks already documented in the 17 example files. For each source instance, the counterexample is conditional on the property's actual CVL preconditions and model. The Bug Label is the *technical assertion category*, not necessarily the Web3Bugs finding label. Report results and audit outcomes are recorded separately. No additional source instance, report claim, or historical harness is invented here.

### 1. `integrityOfWithdraw` — `bridge.spec`

**Indexed interpretation:** S6-4; Result = VERIFIED; Detection Outcome = NO_FINDING; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? If toUnderlyingAsset is true, the recipient's underlying balance decreases or its aToken balance changes; if false, the aToken balance decreases or the underlying balance changes; or the reward balance decreases.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Additional property #4 — ✔. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 2. `balanceOfUnderlyingAssetChanged` — `bridge.spec`

**Indexed interpretation:** UNMAPPED; Result = NOT_STATED; Detection Outcome = NOT_STATED; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? After arbitrary method f, either observed balance changes while f is not one of the three whitelisted selectors.
2. Does that counterexample match the selected Bug Label? No label is forced because this is diagnostic.
3. Is this normative or diagnostic? Diagnostic.
4. Report attribution check: No exact report entry. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 3. `depositWithdrawReversed` — `bridge.spec`

**Indexed interpretation:** S6-4; Result = NOT_STATED; Detection Outcome = NOT_STATED; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? balanceS3 differs from balanceS1, or—when the deposit/withdraw token-choice flags match—the underlying delta exceeds (indexL1/RAY()+1)/2 or the aToken balance differs from its initial value.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Aggregate Additional property #5 — ✔*; no source-instance-specific result. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 4. `dynamicToStaticInversible1` — `bridge.spec`

**Indexed interpretation:** L2; Result = VERIFIED; Detection Outcome = NO_FINDING; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? _dynamicToStaticAmount_Wrapper(_staticToDynamicAmount_Wrapper(amount)) does not equal amount.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Additional property #1 — ✔. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 5. `dynamicToStaticInversible2` — `bridge.spec`

**Indexed interpretation:** L2; Result = VIOLATED; Detection Outcome = FINDING; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? _staticToDynamicAmount_Wrapper(_dynamicToStaticAmount_Wrapper(amount)) differs from amount.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Additional property #2 — ❌; named in the rounding Main Issue. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 6. `dynamicToStaticInversible3` — `bridge.spec`

**Indexed interpretation:** L2; Result = VERIFIED; Detection Outcome = NO_FINDING; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? dynm - amount is greater than (indexL1/RAY()+1)/2 under the rule's uint256 arithmetic.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Additional property #3 — ✔. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 7. `underlying2ATokenConsistency` — `bridge.spec`

**Indexed interpretation:** S3-2; Result = NOT_STATED; Detection Outcome = NOT_STATED; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? When (asset != 0 <=> AToken != 0) holds, exactly one of getUnderlyingAssetHelper(AToken)==asset and getUnderlyingAssetOfAToken(AToken)==asset is true.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: No exact report entry. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 8. `initializeIntegrity` — `bridge.spec`

**Indexed interpretation:** S3-2; Result = VERIFIED; Detection Outcome = NO_FINDING; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? After initialize, for nonzero asset and AToken, one side of the equivalence is true and the other false.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Additional property #6 — ✔. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 9. `cancelAfterDepositGivesBackExactAmount` — `bridge.spec`

**Indexed interpretation:** S6-4; Result = VIOLATED; Detection Outcome = FINDING; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? For fromUA=true, assetBalance1 != assetBalance2 + amount or ATokenBalance2 != ATokenBalance1 + amount; for fromUA=false, either observed balance changes.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Additional property #8 — ❌; named in the rounding Main Issue. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 10. `cannotCancelDepositAndGainBothTokens` — `bridge.spec`

**Indexed interpretation:** S4-1; Result = VIOLATED; Detection Outcome = ACCEPTED_BEHAVIOR; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? staticBalance2 > staticBalance1 but ATokenBalance3 != ATokenBalance2 after the cancellation sequence.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Additional property #9 — ❌; named in the cancellation Main Issue. The counterexample is formally violated, but Aave explicitly treats timely Starknet proof generation as an accepted bridge assumption, so Detection Outcome is ACCEPTED_BEHAVIOR. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 11. `integrityApprovedTokensAndTokenData` — `bridge.spec`

**Indexed interpretation:** S3-2; Result = VERIFIED; Detection Outcome = NO_FINDING; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? totalApprovedTokens differs from getApprovedL1TokensLength() for a checked state/method.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Community property #1 — ✔. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 12. `shouldRevertInitializeTokens` — `bridge.spec`

**Indexed interpretation:** S2-3; Result = VIOLATED; Detection Outcome = FINDING; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? initialize@withrevert does not revert when [l1TokenA,l1TokenB] is paired with [l2Token,l2Token] under the rule's preconditions.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Community property #2 — ❌; named in the duplicate-token Main Issue. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 13. `integrityOfDepositExpanded` — `bridge.spec`

**Indexed interpretation:** S6-4; Result = NOT_STATED; Detection Outcome = NOT_STATED; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? Any branch-specific balance assertion in integrityOfDepositExpanded fails after deposit.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Aggregate Community property #3 — ✔*; no source-instance-specific result. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 14. `alwaysUnSent` — `setup.spec`

**Indexed interpretation:** UNMAPPED; Result = NOT_STATED; Detection Outcome = NOT_STATED; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? For a method admitted by messageSentFilter, withdrawMessageStatus or bridgeRewardsMessageStatus is true in the invariant state.
2. Does that counterexample match the selected Bug Label? No label is forced because this is modeling/diagnostic.
3. Is this normative or diagnostic? Modeling/diagnostic.
4. Report attribution check: No standalone report result. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 15. `ATokenAssetPair` — `setup.spec`

**Indexed interpretation:** S3-2; Result = VERIFIED; Detection Outcome = NO_FINDING; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? Under the implication guard, exactly one of the two linkage relations holds.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Additional property #7 — ✔. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 16. `depositWithdrawReversed` — `bridgeConstIndex.spec`

**Indexed interpretation:** S6-4; Result = NOT_STATED; Detection Outcome = NOT_STATED; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? Under the summarized model, static balance is not restored, or—when fromUA == toUA—the underlying bound or exact aToken restoration fails.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Aggregate Additional property #5 — ✔*; no source-instance-specific result. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### 17. `integrityOfDepositExpanded` — `bridgeConstIndex.spec`

**Indexed interpretation:** S6-4; Result = NOT_STATED; Detection Outcome = NOT_STATED; Target Contract = BridgeHarness. The dependency status is `incomplete`.

1. What exactly makes the assertion fail? Under the summarized model, any branch-specific sender/recipient/reward balance assertion fails.
2. Does that counterexample match the selected Bug Label? Yes, within the partial-proof limitations stated above; the mapping follows the executable assertion rather than only its name/comment.
3. Is this normative or diagnostic? Normative.
4. Report attribution check: Aggregate Community property #3 — ✔*; no source-instance-specific result. No aggregate status is silently propagated across duplicate source instances.
5. Target check: upstream verification scripts confirm BridgeHarness as the target for both bridge.spec and bridgeConstIndex.spec; supplied Bridge.sol excerpts are later production evidence, not the missing historical target implementation.

### Integrity checks and execution boundary for this review

- Read-only GitHub blob comparison found **51/51** supplied Solidity/Cairo/spec files byte-identical between `PropertyGPT/certora_projects/aave_starknet_bridge/{contracts,specs}` and `Web3Bugs-certora/contracts/5/{contracts,specs}`. No extra file was found inside the Project 5 copied snapshot. The preserved report PDF has the same Git blob SHA as the source PDF.
- An independent comment-aware declaration scan identified **13** active properties in `bridge.spec`, **2** in `bridgeConstIndex.spec`, and **2** in `setup.spec`, excluding the block-commented `afterCancellationStartMustSucceed`. All **17** original active property blocks were compared as literal strings with the corresponding extracted `N.spec` files and matched. There are **17** Project 5 CSV relationships and **17** complete sets of four incomplete artifacts (`.spec`, `.sol`, `.md`, `.txt`).
- A source-range review compared **31/31** literal Solidity excerpt segments across the 17 `.sol` files with their exact original line ranges in `contracts/5/contracts/l1/Bridge.sol`; all matched. A read-only structural audit of the complete branch tree and CSV content, implementing the key checks of the three validators independently in JavaScript, found no mismatched paths, orphaned spec artifacts, invalid labels/results/outcomes, or inconsistent contest/contract pairs (**164** examples, **169** label relationships overall). This is **not** an execution of the Python scripts.
- The GitHub-connected environment used for this focused documentation follow-up could inspect blobs and repository metadata but **could not execute** the three Python validators or `git diff --check` on a local checkout: the local container cannot resolve `github.com` and the authorized remote Desktop Commander is offline. The historical PASS statements in the preceding Validation section document an earlier catalog review, **not** execution of those scripts in this follow-up. CI/independent reviewers must execute those commands before accepting this change. The read-only integrity audit does not replace CVL semantic analysis or formal prover reproduction.

## Adversarial follow-up: transitive CVL summaries and literal-assertion limits

This independent review on 2026-10-16 found additional interpretive limitations after inspecting the preserved source bodies and per-example documentation. These are **not** new formal-verification results or new security findings.

### Available CVL methods summaries are not proven transitively preserved

The reduced extracted N.spec files preserve direct CVL call-site declarations and lexically reached helpers. However, a direct CVL helper closure is not necessarily the **full historical methods summarization environment** for a Solidity execution path. The original setup.spec contains potentially relevant external-call summaries that are not reproduced in reduced examples:

- setup.spec lines **75–77**: lending-pool deposit, withdraw, and getReserveNormalizedIncome dispatcher summaries;
- setup.spec lines **84–104**: AToken and incentives-controller dispatcher/constant summaries;
- setup.spec line **117**: l1ToL2MessageNonce() => NONDET;
- setup.spec lines **122–126**: token/address/reward dispatcher summaries.

These are **CVL declarations available in the snapshot**, not missing Solidity implementations. This PR has now **restored selected original declarations verbatim** in the reduced N.spec files for examples **1, 3–6, 8–10, 12–13 and 16–17**. Their CVL line provenance is reflected in each N.spec header, the N.md source-range field, and the Project 5 CSV row. The restored settings are selectively relevant to observed production-code paths, **not** an exhaustive independent proof of the historical effective method environment. Their relevance is not established solely by textual CVL rule references: Bridge.sol lines **173–176** call the lending pool or aToken during withdrawal; lines **95–120** call token/pool/index/messaging interfaces during deposit; lines **277–287** call AToken getters during initialization. Consequently, external-call settings can affect a verification even where a selected CVL rule never directly names a dispatcher.

Previous claims of a *property-specific recursive CVL helper closure* must be interpreted as a **lexical/direct-CVL extraction audit**. The newly included original method declarations close identified **source-available** indirect-call gaps, but are **not proof** that all transitive Solidity calls retain historical effective summaries. With BridgeHarness, linked mocks, original erc20.spec and the exact run environment absent, it is not possible to validate the full call graph or independently establish the minimal transitive summaries per example. The reduced files should **not** be treated as stand-alone, historically equivalent prover configurations; they remain **incomplete**. A subsequent reproduction pass should identify which original available methods declarations materially affect each rule, cite their original lines, and preserve the relevant declarations rather than guessing or borrowing files from another project.

### Additional per-rule limits identified by the second review

| Source example(s) | Literal observation | Interpretation |
| --- | --- | --- |
| 3 and 16: depositWithdrawReversed | Both specs require RAY() <= indexL1 <= 2*RAY() and compare balanceU3 - balanceU1 <= (indexL1/RAY()+1)/2. | This is a **one-sided subtraction**, not an absolute-error bound. The ✔* report footnotes do not remove the explicit source precondition. |
| 10: cannotCancelDepositAndGainBothTokens | staticBalance3 is never asserted. Unlike the other cancellation rule, no explicit require imposes timestamp ordering on e1/e2/e3. | The rule demands equality of aToken balances after observed static minting, without asserting whether any differing balance is an increase or decrease. Interpreting a change as a refund requires the modeled cancellation implementation; historical harness timing/message restrictions remain unknown. |
| 12: shouldRevertInitializeTokens | The rule does not require l1TokenA != l1TokenB or directly require a valid nonzero l2Token. | Some symbolic cases can revert for other reasons and satisfy lastReverted; the report's violated instance still supports the duplicate-L2 finding, not universal input-array uniqueness. |
| 13 and 17: integrityOfDepositExpanded | The fromUnderlyingAsset=false aToken assertions use different one-sided subtraction directions. | They are not interchangeable formulas or absolute-error bounds; no report-wide ✔* attribution to either whole instance. |
| setup.spec:309–316 | requireValidTokens is declared but never invoked by an active Project 5 property. | setupTokens constrains token membership/linkage through other helpers, not through this pairwise-address-inequality helper. |

The source property texts remain untouched, and examples 3, 10, 12, 13, 16 and 17 have had their explanatory .md files narrowed. The *Detection Intent* prose in the Project 5 CSV row for example 10 was also corrected from categorical 'refund' to the literal condition 'balance change', without altering any other CSV row or its CRLF line endings. The Bug Label, Result, Detection Outcome and Target Contract remain unchanged.

### Follow-up provenance checks and execution boundary

The independent second review re-enumerated the 17 active declarations; verified each property body appears unchanged in its extracted N.spec; and checked **every nonempty, non-header line** of the 17 extracted CVL files against the cited original source-line ranges. **No unmatched extracted lines** were found. This is a positive source-provenance check, not a test for omitted transitive global summaries.

The three required Python validators and git diff --check were **not rerun** in this environment because no local GitHub checkout can be accessed. No new validator PASS is claimed.

## Final Boreal follow-up — source-available method-summary corrections (2026-10-16)

The originally extracted CVL files included direct rule/helper declarations but omitted some original methods summaries that can influence Solidity calls reached indirectly. Rather than declaring those declarations missing, this follow-up restored verbatim selected settings from the original setup.spec in 12 examples:

| Example(s) | Restored original setup.spec methods line(s) | Path-dependent relevance |
| --- | --- | --- |
| 1 | 76, 77, 100, 104 | withdrawal lending-pool call and index/reward reads |
| 3, 16 | 75–77, 100, 104, 117 | deposit, withdrawal, conversion, rewards and message nonce |
| 4, 5, 6 | 77 | normalized-income getter potentially reached by conversion wrappers |
| 8, 12 | 88, 91, 122 | initialize token/pool/controller checks |
| 9, 10, 13, 17 | 75, 77, 100, 104, 117 | deposit/cancellation or deposit balance flow with index/reward/nonce calls |

The inserted lines are **literal original declarations**, not invented implementations; the historical rules/invariants themselves were not changed. Exact CVL provenance fields were updated consistently in their N.spec headers, individual N.md references, and the corresponding rows in spec_buglabel.csv; pre-existing file paths, property names, formal results, outcomes and labels were retained. The shared CSV retains its original CRLF style.

For examples **2, 7, 11, 14, 15**, the parametric or invariant preservation domain can reach a broad set of calls. Without the historical harness and erc20.spec, it is not defensible to claim that a hand-picked short summary set reproduces the original full methods environment, so no transitive closure is claimed. All 17 individual N.md files now have a dedicated section explaining what is restored or unresolved.

### Historical model reproduction procedure (not performed)

1. Obtain the original formal-verification project corresponding to the report, keeping BridgeHarness, BridgeL2Harness, symbolic lending-pool and token mocks, the historical erc20.spec import and the original verification scripts together, rather than mixing them with newer production Solidity.
2. Evaluate each spec in its original context, with its full setup.spec methods block (including dispatchers, NONDET, constants and any summaries selected by the source spec). The constant-index spec activates rayMul/rayDiv CVL summaries at bridgeConstIndex.spec:13–14; the ordinary bridge.spec does not activate those commented-out setup summaries.
3. Match the historical config, solver settings, compiler and contract links before interpreting a verified/violated claim. The previously recovered public verification metadata refers to BridgeHarness, solc8.10, --optimistic_loop, --loop_iter 3, and -mediumTimeout=700,-depth=12, but the local PropertyGPT snapshot lacks the historical linked implementations. The exact report-era run for every property has **not** been reproduced.
4. Compare model traces under the full original spec/harness with extracted CVL examples only after linking all historical targets and resolving imports. Their present status is incomplete; a matching structural CSV check does not establish prover equivalence.

**Validation limitation:** In this connected session, a checkout of the GitHub branch is not available to the local Python runtime because github.com cannot be resolved; the authorized remote computer is offline and GitHub Actions has no workflow runs for this PR. Therefore, the three exact Python validators and literal git diff --check **have not been executed on the commit**. GitHub-only structural/provenance checks may be documented separately, but must not be represented as authoritative PASS logs. The independent orchestrator must run these commands before approving/merging the PR. This is an explicit unresolved review gate, not a completed CI check.

### Actual checkout attempt and validation log — 2026-10-17 02:21:55 UTC

The following is the literal stderr/stdout and exit code of a command **executed in this session's Linux environment** before attempting to run the required scripts. It documents why the exact validator commands could not be run on the PR commit; it is not a PASS log.

```text
DATE UTC: 2026-10-17T02:21:55Z
COMMAND: git clone --depth=1 --branch catalog/p05-boreal-aave-starknet-bridge https://github.com/matheus-junio-da-silva/Web3Bugs.git /mnt/data/boreal_p5_validation/Web3Bugs
Cloning into '/mnt/data/boreal_p5_validation/Web3Bugs'...
fatal: unable to access 'https://github.com/matheus-junio-da-silva/Web3Bugs.git/': Could not resolve host: github.com
CLONE_EXIT_CODE: 128
Validator execution and git diff --check on the requested branch: BLOCKED (checkout did not exist).
```

The required commands, `python3 scripts/check_specs.py .`, `python3 scripts/check_contests_csv.py .`, `python3 scripts/check_contracts.py .`, and `git diff --check`, consequently have **no successful or failed script-run logs** for this commit (they were not executed against a checkout). The absence of checkout is the blocker, not evidence of a validator failure or success. GitHub Actions reports zero workflow runs in this repository. The independent reviewer must execute all four commands from the internal project root when an authorized checkout is available.

An independent **GitHub tree/CSV structural check** on PR head `7e30c10a6375d02ec3f71cf2c82ff3e695c2eb5e` found 164 spec examples, 169 label rows, 17 Project 5 entries, zero schema/path/orphan/relationship errors, and no trailing spaces in added patch lines. This check is not the actual Python validators and GitHub patch scanning is not `git diff --check`; neither is presented as a substitute.
