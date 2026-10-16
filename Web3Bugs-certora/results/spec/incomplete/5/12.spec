// Extracted from Project 5 — Aave-StarkNet L1-L2 Bridge
// Property: shouldRevertInitializeTokens
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: specs/setup.spec:4;13-14;16;33;39;50;61;123-124;136;296-305 | specs/bridge.spec:346-370

import "./erc20.spec"
    using ATokenWithPoolA_L1 as ATOKEN_A
    using ATokenWithPoolB_L1 as ATOKEN_B
    using SymbolicLendingPoolL1 as LENDINGPOOL_L1
methods {
    initialize(uint256, address, address, address[], uint256[], uint256[])
    getATokenOfUnderlyingAsset(address, address) returns (address) envfree
    getL2TokenOfAToken(address) returns (uint256) envfree
    ATOKEN_A.UNDERLYING_ASSET_ADDRESS() returns (address) envfree
    ATOKEN_B.UNDERLYING_ASSET_ADDRESS() returns (address) envfree  
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
rule shouldRevertInitializeTokens(address AToken, address asset){
    env e;
    uint256 l2Bridge;
    address msg;
    address controller;
    address l1TokenA;
    address l1TokenB;
    uint256 l2Token;
    // Addition by Certora, to match new interface.
    uint256 ceil1;
    uint256 ceil2;

    // Post-constructor conditions
    require getUnderlyingAssetHelper(AToken) == 0;
    require getATokenOfUnderlyingAsset(LENDINGPOOL_L1, asset) == 0;
    require getL2TokenOfAToken(l1TokenA) == 0 
        && getL2TokenOfAToken(l1TokenB) == 0;

    // In this case, both l1Tokens point to same l2Token :
    // L1TokenA => L2Token
    // L1TokenB => L2Token
    initialize@withrevert(e, l2Bridge, msg, controller,
     [l1TokenA, l1TokenB], [l2Token,l2Token], [ceil1, ceil2]);
    assert lastReverted;
}
