// Extracted from Project 5 — Aave-StarkNet L1-L2 Bridge
// Property: initializeIntegrity
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: specs/setup.spec:4;13-14;16;33;39;50;88;91;122-124;136;296-305 | specs/bridge.spec:191-206

import "./erc20.spec"
    using ATokenWithPoolA_L1 as ATOKEN_A
    using ATokenWithPoolB_L1 as ATOKEN_B
    using SymbolicLendingPoolL1 as LENDINGPOOL_L1
methods {
    initialize(uint256, address, address, address[], uint256[], uint256[])
    getATokenOfUnderlyingAsset(address, address) returns (address) envfree
    ATOKEN_A.UNDERLYING_ASSET_ADDRESS() returns (address) envfree
    ATOKEN_B.UNDERLYING_ASSET_ADDRESS() returns (address) envfree  
    POOL() returns (address) => DISPATCHER(true)
    getIncentivesController() => DISPATCHER(true)
    UNDERLYING_ASSET_ADDRESS() returns (address) => DISPATCHER(true)
}
function getUnderlyingAssetHelper(address AToken) returns address {
    if (AToken == ATOKEN_A) {
        return ATOKEN_A.UNDERLYING_ASSET_ADDRESS();
    }
    else if (AToken == ATOKEN_B) {
        return ATOKEN_B.UNDERLYING_ASSET_ADDRESS();
    }
    // Warning: default value is 0!
    return 0;
}
rule initializeIntegrity(address AToken, address asset)
{
    env e;
    calldataarg args;

    // Post-constructor conditions
    require getUnderlyingAssetHelper(AToken) == 0;
    require getATokenOfUnderlyingAsset(LENDINGPOOL_L1, asset) == 0;
    
    initialize(e, args);

    assert (asset !=0 && AToken !=0) => (
        getUnderlyingAssetHelper(AToken) == asset 
        <=>
        getATokenOfUnderlyingAsset(LENDINGPOOL_L1, asset) == AToken);
}
