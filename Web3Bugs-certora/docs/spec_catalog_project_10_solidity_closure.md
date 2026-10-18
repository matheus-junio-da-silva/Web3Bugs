# Project 10 — transitive Solidity dependency closure, independent re-audit

Source baseline: PR #8 HEAD `471ac775c37ed243ca7145762417cbdd6bc2e197`; merged main `46670617ee77649217b9dbf64fd6955344cedcf7`. Audit date: 2026-10-18.

This is a static recursive import/target-identity audit, **not** a Certora replay, an ABI equivalence proof, or a guarantee that historical code compiles. Each source Solidity `import` in the reachable target closure must resolve from the **preserved** snapshot. CVL `methods` declarations and Summary do not bypass Solidity compiler imports. Do not install modern replacements to relabel an example complete.

**Decision on all 89 previously complete:** 87 changed to incomplete; only IDs 33 and 34 remain dependency-complete for `LibParamHarness` (two local source files and zero unresolved Solidity imports). Previous 39 incomplete remain incomplete. Final: 2 complete, 126 incomplete, 128 total. Standalone diagnostic #35 is incomplete because its target and execution script are unknown.

## Direct and transitive import closure by target

Columns: target, concrete compilation seeds used to audit the intended run, number of reachable local files, unresolved imports and their physical import sites, affected previously complete IDs.

### HAaveProtocolV2 — previously complete IDs 45, 46, 47, 48

Local roots: contracts/10/contracts/handlers/aavev2/HAaveProtocolV2.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 24.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/aavev2/HAaveProtocolV2.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HBProtocol — previously complete IDs 36, 61, 62, 63, 64

Local roots: contracts/10/contracts/handlers/bprotocol/HBProtocol.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 22.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/maker/HMaker.sol:9.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HCEther — previously complete IDs 69, 70, 71, 72

Local roots: contracts/10/contracts/handlers/compound/HCEther.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 20.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/compound/HCEther.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HCToken — previously complete IDs 73, 74, 75, 76

Local roots: contracts/10/contracts/handlers/compound/HCToken.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 20.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/compound/HCToken.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HComptroller — previously complete IDs 77, 78, 79, 80

Local roots: contracts/10/contracts/handlers/compound/HComptroller.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 20.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/compound/HComptroller.sol:7.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HCurve — previously complete IDs 81, 82, 83, 84

Local roots: contracts/10/contracts/handlers/curve/HCurve.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 20.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/curve/HCurve.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HCurveDao — previously complete IDs 85, 86, 87, 88

Local roots: contracts/10/contracts/handlers/curve/HCurveDao.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 21.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/curve/HCurveDao.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HFunds — previously complete IDs 53, 54, 55, 56

Local roots: contracts/10/contracts/handlers/funds/HFunds.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 19.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/funds/HFunds.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HFurucomboStaking — previously complete IDs 89, 90, 91, 92

Local roots: contracts/10/contracts/handlers/furucombo/HFurucomboStaking.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 21.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/furucombo/HFurucomboStaking.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HMaker — previously complete IDs 31, 37, 38, 39, 40

Local roots: contracts/10/contracts/handlers/maker/HMaker.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 21.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/maker/HMaker.sol:9.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HSCompound — previously complete IDs 32, 49, 50, 51, 52

Local roots: contracts/10/contracts/handlers/compound/HSCompound.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 22.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/compound/HSCompound.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HStakingRewardsAdapter — previously complete IDs 105, 106, 107, 108

Local roots: contracts/10/contracts/handlers/staking/HStakingRewardsAdapter.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 21.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/IERC20.sol` imported at contracts/10/contracts/staking/IStakingRewardsAdapter.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/staking/HStakingRewardsAdapter.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HSushiSwap — previously complete IDs 109, 110, 111, 112

Local roots: contracts/10/contracts/handlers/sushiswap/HSushiSwap.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 22.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/sushiswap/HSushiSwap.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HUniswapV2 — previously complete IDs 117, 118, 119, 120

Local roots: contracts/10/contracts/handlers/uniswapv2/HUniswapV2.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 22.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/uniswapv2/HUniswapV2.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### HYVault — previously complete IDs 125, 126, 127, 128

Local roots: contracts/10/contracts/handlers/yearn/HYVault.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 20.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5, contracts/10/contracts/handlers/HandlerBase.sol:5, contracts/10/contracts/handlers/yearn/HYVault.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- The actual script `specs/scripts/_runHandler.sh` compiles this handler with `Registry.sol`, `ProxyHarness.sol`, `DummyERC20A/B.sol` and `Summary.sol`; it rewrites `SafeERC20.sol` to `ERC20.sol` *in the handler*, yet neither OpenZeppelin path is present. Getters `getStackLength`, `getSender`, `getCubeCounter` and `getStackLengthSlot` are injected textually; `stack_slot` and `_getCubeCounter` remain unresolved in the later snapshot. Historical ABI identity is unproven.

### LibParamHarness — previously complete IDs 33, 34

Local roots: contracts/10/specs/harnesses/LibParamHarness.sol; reachable local Solidity sources: 2.
- No unresolved Solidity imports found among identified local roots; this is **not** confirmation that a modern Prover replay succeeds.
- `libParam.sh` compiles local `LibParamHarness.sol` and its local `LibParam.sol` import; property methods `getParams`, `getNumOfReferences` and `isStatic` are defined in the harness. Compiler/Prover was not run.

### Proxy — previously complete IDs 12

Local roots: contracts/10/contracts/Proxy.sol; reachable local Solidity sources: 10.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- `privProxy.sh` invokes `certoraRun contracts/Proxy.sol`; the imported missing library dependencies cannot be abstracted by `--ignoreViewFunctions`.

### ProxyHarness — previously complete IDs 13, 14, 17, 18, 21, 22, 24, 25, 26, 27, 28

Local roots: contracts/10/specs/harnesses/ProxyHarness.sol, contracts/10/contracts/Registry.sol, contracts/10/specs/harnesses/DummyERC20A.sol, contracts/10/specs/harnesses/DummyERC20B.sol, contracts/10/specs/harnesses/Summary.sol; reachable local Solidity sources: 16.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- **MISSING** `@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol` imported at contracts/10/contracts/Proxy.sol:5.
- **MISSING** `@openzeppelin/contracts/utils/Address.sol` imported at contracts/10/contracts/Proxy.sol:6.
- **MISSING** `@openzeppelin/contracts/utils/Strings.sol` imported at contracts/10/contracts/Proxy.sol:7.
- `proxy.sh` compiles `ProxyHarness`, `Registry`, `DummyERC20A/B`, and `Summary` and runs `applyHarnesses.sh`; the harness/Proxy signatures do not match the original transformations.

### Registry — previously complete IDs 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11

Local roots: contracts/10/contracts/Registry.sol; reachable local Solidity sources: 2.
- **MISSING** `@openzeppelin/contracts/access/Ownable.sol` imported at contracts/10/contracts/Registry.sol:5.
- `registry.sh` invokes `certoraRun contracts/Registry.sol`: inheriting `Ownable` requires the missing imported Solidity source, regardless of CVL method summaries.

### UNSPECIFIED — previously complete IDs 35

Local roots: not identified; reachable local Solidity sources: 0.
- No unresolved Solidity imports found among identified local roots; this is **not** confirmation that a modern Prover replay succeeds.
- `sanity.spec` standalone probe has no independently attributable script or target; the adjacent Proxy excerpt is **not** a target proof.

## Per-example disposition of all 89 previously complete records

| Example | Rule | Target | New status | Blocking dependency |
| ---: | --- | --- | --- | --- |
| 1 | `changesHandler` | `Registry` | incomplete | @openzeppelin/contracts/access/Ownable.sol |
| 2 | `deprecatesHandler` | `Registry` | incomplete | @openzeppelin/contracts/access/Ownable.sol |
| 3 | `changesCaller` | `Registry` | incomplete | @openzeppelin/contracts/access/Ownable.sol |
| 4 | `deprecatesCaller` | `Registry` | incomplete | @openzeppelin/contracts/access/Ownable.sol |
| 5 | `unregisterHandlerIsPermanent` | `Registry` | incomplete | @openzeppelin/contracts/access/Ownable.sol |
| 6 | `unregisterCallerIsPermanent` | `Registry` | incomplete | @openzeppelin/contracts/access/Ownable.sol |
| 7 | `unregisterHandlerIsPermanent2` | `Registry` | incomplete | @openzeppelin/contracts/access/Ownable.sol |
| 8 | `unregisterCallerIsPermanent2` | `Registry` | incomplete | @openzeppelin/contracts/access/Ownable.sol |
| 9 | `banningIsReversible` | `Registry` | incomplete | @openzeppelin/contracts/access/Ownable.sol |
| 10 | `haltingIsReversible` | `Registry` | incomplete | @openzeppelin/contracts/access/Ownable.sol |
| 11 | `privilegedOperation` | `Registry` | incomplete | @openzeppelin/contracts/access/Ownable.sol |
| 12 | `privilegedOperation` | `Proxy` | incomplete | @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 13 | `notTouchingCache` | `ProxyHarness` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 14 | `sanity` | `ProxyHarness` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 17 | `stackLengthIncreaseIsBounded` | `ProxyHarness` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 18 | `senderIsAlwaysCleanedUp` | `ProxyHarness` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 21 | `nonExecutableWhenProxyIsBanned` | `ProxyHarness` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 22 | `nonExecutableWhenHalted` | `ProxyHarness` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 24 | `nonExecutableWithInitializedSender` | `ProxyHarness` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 25 | `transferredTokensMeanThatStackIsUpdated` | `ProxyHarness` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 26 | `approvedTokensAreTemporary` | `ProxyHarness` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 27 | `tokenMovementCorrectness` | `ProxyHarness` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 28 | `noOtherPartyModified` | `ProxyHarness` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 31 | `executeDelegatesOnlyToAllowedAddresses` | `HMaker` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 32 | `executeDelegatesOnlyToAllowedAddresses` | `HSCompound` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 33 | `noThrow` | `LibParamHarness` | complete | all local imports resolved |
| 34 | `noRevert` | `LibParamHarness` | complete | all local imports resolved |
| 35 | `sanity` | `UNSPECIFIED` | incomplete | target/script unspecified |
| 36 | `executeDelegatesOnlyToAllowedAddresses` | `HBProtocol` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 37 | `transferredTokensMeanThatStackIsUpdated` | `HMaker` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 38 | `approvedTokensAreTemporary` | `HMaker` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 39 | `tokenMovementCorrectness` | `HMaker` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 40 | `noOtherPartyModified` | `HMaker` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 45 | `transferredTokensMeanThatStackIsUpdated` | `HAaveProtocolV2` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 46 | `approvedTokensAreTemporary` | `HAaveProtocolV2` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 47 | `tokenMovementCorrectness` | `HAaveProtocolV2` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 48 | `noOtherPartyModified` | `HAaveProtocolV2` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 49 | `transferredTokensMeanThatStackIsUpdated` | `HSCompound` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 50 | `approvedTokensAreTemporary` | `HSCompound` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 51 | `tokenMovementCorrectness` | `HSCompound` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 52 | `noOtherPartyModified` | `HSCompound` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 53 | `transferredTokensMeanThatStackIsUpdated` | `HFunds` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 54 | `approvedTokensAreTemporary` | `HFunds` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 55 | `tokenMovementCorrectness` | `HFunds` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 56 | `noOtherPartyModified` | `HFunds` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 61 | `transferredTokensMeanThatStackIsUpdated` | `HBProtocol` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 62 | `approvedTokensAreTemporary` | `HBProtocol` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 63 | `tokenMovementCorrectness` | `HBProtocol` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 64 | `noOtherPartyModified` | `HBProtocol` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 69 | `transferredTokensMeanThatStackIsUpdated` | `HCEther` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 70 | `approvedTokensAreTemporary` | `HCEther` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 71 | `tokenMovementCorrectness` | `HCEther` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 72 | `noOtherPartyModified` | `HCEther` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 73 | `transferredTokensMeanThatStackIsUpdated` | `HCToken` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 74 | `approvedTokensAreTemporary` | `HCToken` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 75 | `tokenMovementCorrectness` | `HCToken` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 76 | `noOtherPartyModified` | `HCToken` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 77 | `transferredTokensMeanThatStackIsUpdated` | `HComptroller` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 78 | `approvedTokensAreTemporary` | `HComptroller` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 79 | `tokenMovementCorrectness` | `HComptroller` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 80 | `noOtherPartyModified` | `HComptroller` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 81 | `transferredTokensMeanThatStackIsUpdated` | `HCurve` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 82 | `approvedTokensAreTemporary` | `HCurve` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 83 | `tokenMovementCorrectness` | `HCurve` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 84 | `noOtherPartyModified` | `HCurve` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 85 | `transferredTokensMeanThatStackIsUpdated` | `HCurveDao` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 86 | `approvedTokensAreTemporary` | `HCurveDao` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 87 | `tokenMovementCorrectness` | `HCurveDao` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 88 | `noOtherPartyModified` | `HCurveDao` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 89 | `transferredTokensMeanThatStackIsUpdated` | `HFurucomboStaking` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 90 | `approvedTokensAreTemporary` | `HFurucomboStaking` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 91 | `tokenMovementCorrectness` | `HFurucomboStaking` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 92 | `noOtherPartyModified` | `HFurucomboStaking` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 105 | `transferredTokensMeanThatStackIsUpdated` | `HStakingRewardsAdapter` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/IERC20.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 106 | `approvedTokensAreTemporary` | `HStakingRewardsAdapter` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/IERC20.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 107 | `tokenMovementCorrectness` | `HStakingRewardsAdapter` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/IERC20.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 108 | `noOtherPartyModified` | `HStakingRewardsAdapter` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/IERC20.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 109 | `transferredTokensMeanThatStackIsUpdated` | `HSushiSwap` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 110 | `approvedTokensAreTemporary` | `HSushiSwap` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 111 | `tokenMovementCorrectness` | `HSushiSwap` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 112 | `noOtherPartyModified` | `HSushiSwap` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 117 | `transferredTokensMeanThatStackIsUpdated` | `HUniswapV2` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 118 | `approvedTokensAreTemporary` | `HUniswapV2` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 119 | `tokenMovementCorrectness` | `HUniswapV2` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 120 | `noOtherPartyModified` | `HUniswapV2` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 125 | `transferredTokensMeanThatStackIsUpdated` | `HYVault` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 126 | `approvedTokensAreTemporary` | `HYVault` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 127 | `tokenMovementCorrectness` | `HYVault` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |
| 128 | `noOtherPartyModified` | `HYVault` | incomplete | @openzeppelin/contracts/access/Ownable.sol, @openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol, @openzeppelin/contracts/utils/Address.sol, @openzeppelin/contracts/utils/Strings.sol |

## Assertion/replay boundaries

- #26 `noOtherPartyModified` (proxy.spec:534–550) asserts that a nonzero address distinct from `currentContract` and `summaryInstance` retains **both** modeled token balances across a selected `f` call. A hypothetical falsifier changes at least one of these balances under all requires. The report discusses this property on physical PDF **page 25**, including target-dependent `None`, expected and `N/A` cells. No recorded per-target Prover trace is inferred.
- `tokenMovementCorrectness` retains the source omission of `at initialStorage` on one generated-token pre-balance; it may compare post-state with itself and cannot be called a conservation proof.
- The 2021 `noOverwrite` source assertion about flat storage does not recreate the High local-memory-overwrite finding described in the PDF.
- Source 2021 revision, Solidity textual transforms, `ProxyHarness` ABI signatures, modelled external DeFi logic, bounded unrolling and `-assumeUnwindCond` prevent sound replay claims even if import closure were restored.

## Checks applied in this reclassification

- All 128 `.spec` and `.sol` bodies keep the same SHA-256 as before relocation; no original `contracts/10` or `resources/10` content was edited.
- All 87 newly incomplete entries have a dedicated `N.txt` documenting the missing dependency, scripts and non-reproducibility; complete IDs 33 and 34 do not have `.txt`.
- CSV `Result`, `Detection Outcome` and `Bug Label` values remain unchanged; no Prover result is mechanically derived from static import closure.
- The 13 malformed `FurucomboMay2021.pdf pp.` references for report property #26 were replaced with grounded **p. 25** citations. A scan found zero remaining `Counterexample: undefined` and zero unnumbered `pp.` markers.
