# Audited Furucombo 2021 driver, getter and import reconstruction

All sources examined as read-only text. No Perl, solc, CVL, or Prover executed.

## specs/scripts/_runHandler.sh SHA b603b618b4e85782cc63b9b97101a928c350636b
- L38: perl -0777 -i -pe 's/function _revertMsg\(string memory functionName, string memory reason\)\s*internal/function _revertMsg\(string memory functionName, string memory reason\) virtual internal/g' contracts/handlers/HandlerBase.sol
- L39: perl -0777 -i -pe 's/is HandlerBase(, [a-zA-Z0-9]+)* \{/is   HandlerBase\1 {
- L40: function getSlot\(uint s\) external view returns \(uint x\) {
- L44: function getStackLengthSlot\(\) external view returns \(uint x\) {
- L48: function getStackLength\(\) external view returns \(uint\) { return stack.length; }
- L50: function getSender\(\) public returns \(address\) { return \_getSender\(\); }
- L51: function getCubeCounter\(\) public returns \(uint256\) { return \_getCubeCounter\(\); }
- L67: perl -0777 -i -pe 's/SafeERC20.sol/ERC20.sol/g' ${handler_file}
- L68: perl -0777 -i -pe 's/safeA/a/g' ${handler_file}
- L69: perl -0777 -i -pe 's/safeT/t/g' ${handler_file}
- L70: perl -0777 -i -pe 's/address public constant /address public /g' ${handler_file}
- L71: perl -0777 -i -pe 's/address payable public constant / address payable public /g' ${handler_file}
- L72: perl -0777 -i -pe 's/dsProxyPayable.transfer\(amount\)/Nothing\(dsProxyPayable\).nop{value:amount}\(\)/g' ${handler_file}
- L75: perl -0777 -i -pe 's/address constant ETHADDRESS/address public ETHADDRESS/g' contracts/handlers/aave/FlashLoanReceiverBase.sol
- L76: perl -0777 -i -pe 's/ETHADDRESS/ETH_ADDRESS/g' contracts/handlers/aave/FlashLoanReceiverBase.sol
- L77: perl -0777 -i -pe 's/ETHADDRESS/ETH_ADDRESS/g' contracts/handlers/aave/HAaveProtocol.sol
- L78: perl -0777 -i -pe 's/ETHADDRESS/ETH_ADDRESS/g' contracts/handlers/aavev2/HAaveProtocolV2.sol
- L81: perl -0777 -i -pe 's/function repay\(/function unique_repay\(/g' contracts/handlers/aavev2/HAaveProtocolV2.sol
- L82: perl -0777 -i -pe 's/function claimComp\(/function unique_claimComp\(/g' contracts/handlers/compound/HSCompound.sol
- L83: perl -0777 -i -pe 's/function claimComp\(/function unique_claimComp\(/g' contracts/handlers/compound/HComptroller.sol
- L84: perl -0777 -i -pe 's/function swap\(/function unique_swap\(/g' contracts/handlers/oneinchV2/HOneInchExchange.sol
- L85: perl -0777 -i -pe 's/function withdraw\(/function unique_withdraw\(/g' contracts/handlers/weth/HWeth.sol
- L86: perl -0777 -i -pe 's/function deposit\(/function unique_deposit\(/g' contracts/handlers/weth/HWeth.sol
- L87: perl -0777 -i -pe 's/function swap/function unique_swap/g' contracts/handlers/kybernetwork/HKyberNetwork.sol
- L88: perl -0777 -i -pe 's/function redeemUnderlying/function unique_redeemUnderlying/g' contracts/handlers/compound/HCEther.sol
- L89: perl -0777 -i -pe 's/receiver.transfer\(amount\)/Nothing\(receiver\).nop{value:amount}\(\)/g' contracts/handlers/funds/HFunds.sol
- L92: perl -0777 -i -pe 's/pragma solidity/pragma experimental ABIEncoderV2; pragma  solidity/g' contracts/handlers/mooniswap/HMooniswap.sol
- L95: perl -0777 -i -pe 's/compound.redeem\(/compound.compoundredeem\(/g' contracts/handlers/compound/HCToken.sol
- L96: perl -0777 -i -pe 's/compound.redeem\(/compound.compoundredeem\(/g' contracts/handlers/compound/HCEther.sol
- L97: perl -0777 -i -pe 's/function redeem\(/function compoundredeem\(/g' contracts/handlers/compound/ICToken.sol
- L98: perl -0777 -i -pe 's/function redeem\(/function compoundredeem\(/g' contracts/handlers/compound/ICEther.sol
- L101: perl -0777 -i -pe 's/yVault.withdraw\(/yVault.yvault_withdraw\(/g' contracts/handlers/yearn/HYVault.sol
- L102: perl -0777 -i -pe 's/function withdraw\(/function yvault_withdraw\(/g' contracts/handlers/yearn/IYVault.sol
- L104: certoraRun ${handler_file} contracts/Registry.sol specs/harnesses/DummyERC20A.sol specs/harnesses/DummyERC20B.sol specs/harnesses/ProxyHarness.sol specs/harnesses/Summary.sol \
- L105: --verify ${handler}:${spec} \
- L106: --settings -assumeUnwindCond,-b=${B},-ciMode=true \

## specs/scripts/applyHarnesses.sh SHA b901b2f4a9550e8349ee6162db20abcfe244d1b4
- L2: perl -0777 -i -pe 's/(function _parse\(\s*bytes32\[256\] memory localStack,\s*bytes memory ret,\s*uint256 index\s*\)) internal/\1 virtual internal/g' contracts/Proxy.sol
- L3: perl -0777 -i -pe 's/(function _trim\(\s*bytes memory data,\s*bytes32 config,\s*bytes32\[256\] memory localStack,\s*uint256 index\s*\)) internal/\1 virtual internal/g' contracts/Proxy.sol
- L4: perl -0777 -i -pe 's/(function _exec\(address _to, bytes memory _data\))\s*internal/\1 virtual internal/g' contracts/Proxy.sol
- L5: perl -0777 -i -pe 's/(function _execs\(\s*address\[\] memory tos,\s*bytes32\[\] memory configs,\s*bytes\[\] memory datas\s*\)) internal/\1 virtual internal/g' contracts/Proxy.sol
- L9: perl -0777 -i -pe 's/bytes32\[256\]/bytes32\[2\]/g' contracts/Proxy.sol
- L10: perl -0777 -i -pe 's/bytes32\[256\]/bytes32\[2\]/g' specs/harnesses/ProxyHarness.sol
- L11: perl -0777 -i -pe 's/require\(newIndex <= 256\);/require\(newIndex <= 2\);/g' specs/harnesses/ProxyHarness.sol
- L14: #perl -0777 -i -pe 's/internal/public/g' contracts/Proxy.sol
- L15: #perl -0777 -i -pe 's/internal/public/g' specs/harnesses/ProxyHarness.sol

## specs/scripts/proxy.sh SHA 653607e3a26ee35581cf04eae93d33de55e81071
- L8: certoraRun specs/harnesses/ProxyHarness.sol contracts/Registry.sol specs/harnesses/DummyERC20A.sol specs/harnesses/DummyERC20B.sol specs/harnesses/Summary.sol \
- L9: --verify ProxyHarness:specs/proxy.spec \
- L10: --settings -assumeUnwindCond,-b=$B \

## specs/scripts/libParam.sh SHA 3344316e9569c8292df6d47725126dfa3173c605
- L1: certoraRun specs/harnesses/LibParamHarness.sol \
- L2: --verify LibParamHarness:specs/libParam.spec \
- L3: --settings -b=64,-smt_bitVectorTheory=true \

## specs/scripts/privRegistry.sh SHA 482b175387a6e111f3ca7062813083a369eb5b46
- L1: certoraRun contracts/Registry.sol \
- L2: --verify Registry:specs/privileged.spec \
- L3: --settings -t=300,-ignoreViewFunctions \

## specs/scripts/privProxy.sh SHA 0df5e2a0ebcf4cf369b5d32fed8303aa5c811905
- L1: certoraRun contracts/Proxy.sol \
- L2: --verify Proxy:specs/privileged.spec \
- L3: --settings -t=300,-ignoreViewFunctions \

## Unresolved implications
- Scripts _runHandler.sh and applyHarnesses.sh edit Solidity in place (the original scripts were NOT run). They inject getter functions including getSlot/getStackLength/getSender/getCubeCounter, rename overloads and reduce bounds. Post-transformation ABI and storage layout not compiler-confirmed.
- Full compilation seeds by handler: handler file, Registry, DummyERC20A/B, ProxyHarness and Summary (see target_revision_matrix.csv), with OpenZeppelin v3.3.0 Git imports recovered separately.
- CVL2 summaries default to currentContract, while historical CVL1 summaries can reach all contracts with signature. Never assert underscore wildcard or explicit receiver preservation without target-correct call resolution.
- Historical OpenZeppelin source recovery is from official tag v3.3.0, commit 6be5ffe54fc8982b7c1d0f45d4cb7bbd313107cd. It is NOT proof of exact npm tarball, compiler or Prover equivalence.
- No fabrication of function signature for raw 0x12345678 => NONDET; some method entries still need external/internal ABI determination.
- Certora official guides: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html and https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html
