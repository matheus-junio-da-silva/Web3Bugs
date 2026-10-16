// Extracted from Project 5 — Aave-StarkNet L1-L2 Bridge
// Property: cannotCancelDepositAndGainBothTokens
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: specs/setup.spec:4;11-17;22-24;27;33;39-41;43;50-51;58;115-116;123-124;136;156-158;167-170;210-216;232-244;248-251;254-261;278-287;289-293;296-305;319-332 | specs/bridge.spec:252-287

import "./erc20.spec"
    using DummyERC20UnderlyingA_L1 as UNDERLYING_ASSET_A 
    using DummyERC20UnderlyingB_L1 as UNDERLYING_ASSET_B
    using ATokenWithPoolA_L1 as ATOKEN_A
    using ATokenWithPoolB_L1 as ATOKEN_B
    using DummyERC20RewardToken as REWARD_TOKEN
    using SymbolicLendingPoolL1 as LENDINGPOOL_L1
    using IncentivesControllerMock_L1 as incentivesController
    using BridgeL2Harness as BRIDGE_L2
    using StaticATokenA_L2 as STATIC_ATOKEN_A
    using StaticATokenB_L2 as STATIC_ATOKEN_B
    using BridgeHarness as Bridge
methods {
    initialize(uint256, address, address, address[], uint256[], uint256[])
    deposit(address, uint256, uint256, uint16, bool) returns (uint256) 
    withdraw(address, uint256, address, uint256, uint256, bool)
    receiveRewards(uint256, address, uint256)
    getATokenOfUnderlyingAsset(address, address) returns (address) envfree
    getLendingPoolOfAToken(address) returns (address) envfree //(ILendingPool)
    getUnderlyingAssetOfAToken(address) returns (address) envfree
    BRIDGE_L2.getStaticATokenAddress(address) returns (address) envfree
    BRIDGE_L2.address2uint256(address) returns (uint256) envfree
    ATOKEN_A.UNDERLYING_ASSET_ADDRESS() returns (address) envfree
    ATOKEN_B.UNDERLYING_ASSET_ADDRESS() returns (address) envfree  
}
definition excludeInitialize(method f) returns bool =
    f.selector != 
    initialize(uint256, address, address, address[], uint256[], uint256[]).selector; 
definition messageSentFilter(method f) returns bool = 
    f.selector != receiveRewards(uint256, address, uint256).selector
    &&
    f.selector != withdraw(address, uint256, address, uint256, uint256, bool).selector;
invariant ATokenAssetPair(address asset, address AToken)
    (asset !=0 <=> AToken !=0) 
    =>
    (getUnderlyingAssetHelper(AToken) == asset 
    <=>
    getATokenOfUnderlyingAsset(LENDINGPOOL_L1, asset) == AToken)
    filtered{f -> excludeInitialize(f)  && messageSentFilter(f)}
function setupTokens(
    address asset, 
    address AToken, 
    address static){
    // Selects a dummy contract implementation for the tokens trio.
    // Note that if it used twice, for two different trios, it is possible
    // they will share the same addresses.
    tokenSelector(asset, AToken, static);
    // Links tokens to each other throught the bridges and pool stored data.
    setLinkage(asset, AToken, static);
    // Links asset and AToken. (Might be redundant after calling 'setLinkage').
    requireInvariant ATokenAssetPair(asset, AToken);
}
function setupUser(address user){
    // Exclude contracts addresses from possible values of [user].
    requireValidUser(user);
}
function tokenSelector(
    address asset, 
    address AToken, 
    address static){
    require asset == UNDERLYING_ASSET_A || asset == UNDERLYING_ASSET_B;
    require AToken == ATOKEN_A || AToken == ATOKEN_B;
    require static == STATIC_ATOKEN_A || static == STATIC_ATOKEN_B;
}
function setLinkage(
    address asset, 
    address AToken, 
    address static){
    // Setting the underlying token of the given AToken as either UNDERLYING_ASSET_A or UNDERLYING_ASSET_B
    require getUnderlyingAssetOfAToken(AToken) == asset;
    require getLendingPoolOfAToken(AToken) == LENDINGPOOL_L1;
    require BRIDGE_L2.getStaticATokenAddress(AToken) == static;
    setUnderlyingAToken(AToken, asset);
}
function setUnderlyingAToken(address AToken, address asset) {
    // Note that if AToken is neither ATOKEN_A nor ATOKEN_B,
    // this function will force asset == 0.
    require getUnderlyingAssetHelper(AToken) == asset;
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
function requireValidUser(address user){
    require 
        user != Bridge &&
        user != BRIDGE_L2 &&
        user != UNDERLYING_ASSET_A &&
        user != UNDERLYING_ASSET_B &&
        user != ATOKEN_A &&
        user != ATOKEN_B &&
        user != STATIC_ATOKEN_A &&
        user != STATIC_ATOKEN_B &&
        user != REWARD_TOKEN &&
        user != LENDINGPOOL_L1 &&
        user != incentivesController;
}
rule cannotCancelDepositAndGainBothTokens(address user, uint256 amount) {
    env e1; env e2; env e3;
    calldataarg args1;
    address asset;
    address aToken;
    address static;
    uint256 recipient = BRIDGE_L2.address2uint256(user);
    uint16 code;
    bool fromUA;
    uint256 rewardsIndex;
    uint256 blockNumber;
    uint256 nonce;

    setupTokens(asset, aToken, static);
    setupUser(user);
    require user == e1.msg.sender;
    require user == e2.msg.sender;
    require user == e3.msg.sender;
    
    uint256 ATokenBalance1 = tokenBalanceOf(e1, aToken, user);
    uint256 staticBalance1 = tokenBalanceOf(e1, static, user);

    uint256 staticAmount = deposit(e1, aToken, recipient, amount, code, fromUA);
    
    uint256 ATokenBalance2 = tokenBalanceOf(e1, aToken, user);
    uint256 staticBalance2 = tokenBalanceOf(e1, static, user);

    startDepositCancellation(e2, aToken, staticAmount, recipient, rewardsIndex, blockNumber, nonce);
    cancelDeposit(e3, aToken, staticAmount, recipient, rewardsIndex, blockNumber, nonce);
    
    uint256 ATokenBalance3 = tokenBalanceOf(e3, aToken, user);
    uint256 staticBalance3 = tokenBalanceOf(e3, static, user);

    // If static tokens were minted, no deposit cancellation should succeed.
    assert staticBalance2 > staticBalance1 => ATokenBalance3 == ATokenBalance2;
}
