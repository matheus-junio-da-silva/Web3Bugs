// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/ValidBalances.spec:274-293
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using DummyERC20C as collateralToken

using MarginPool as pool

using Whitelist as whitelist

using OtokenHarnessA as shortOtoken

using OtokenHarnessB as longOtoken

using DummyERC20A as underlying

using DummyERC20B as strike

methods {
    pool.getStoredBalance(address) returns uint256 envfree
    longOtoken.collateralAsset() returns address envfree => CONSTANT
    shortOtoken.collateralAsset() returns address envfree => CONSTANT
    getVaultLongOtoken(address, uint256, uint256)  returns address envfree
    getVaultShortOtoken(address, uint256, uint256)  returns address envfree
    smallVault(address, uint256, uint256) returns bool envfree
    assetTotalSupply(address) returns uint256 envfree
    whitelist.isWhitelistedOtoken(address) returns bool envfree
    whitelist.isWhitelistedCollateral(address) returns bool envfree
    anOtokenA() returns address envfree
    anOtokenB() returns address envfree
    dummyERC20C() returns address envfree
    shortOtoken.underlyingAsset() returns address envfree
    longOtoken.underlyingAsset() returns address envfree
    shortOtoken.strikeAsset() returns address envfree
    longOtoken.strikeAsset() returns address envfree
    shortOtoken.collateralAsset() returns address envfree
    longOtoken.collateralAsset() returns address envfree
}

function links() {
    require anOtokenA() == shortOtoken;
    require anOtokenB() == longOtoken;
    require dummyERC20C() == collateralToken;
}

function callFunctionWithParameters(method f, address owner, uint256 vaultId, uint256 index) {
    env e;
    uint256 amount;
    address to;
    address from;
    address receiver;
    require to!=pool && to!=currentContract;
    require from!=pool && from!=currentContract;
    require e.msg.sender!=pool && e.msg.sender!=currentContract;
    if (f.selector == depositCollateral(address,uint256,address,uint256,uint256).selector) {
        depositCollateral(e, owner, vaultId, from, index, amount);
    }
    else if (f.selector == withdrawCollateral(address,uint256,address,uint256,uint256).selector) {
        withdrawCollateral(e, owner, vaultId, to, index, amount);
    }
    else if (f.selector == withdrawLongB(address,uint256,address,uint256,uint256).selector) {
        withdrawLongB(e, owner, vaultId, to, index, amount);
    }
    else if (f.selector == withdrawLongA(address,uint256,address,uint256,uint256).selector) {
        withdrawLongA(e, owner, vaultId, to, index, amount);
    }
    else if (f.selector == burnOtokenA(address,uint256,address,uint256,uint256).selector) {
        burnOtokenA(e, owner, vaultId, from, index, amount);
    }
    else if (f.selector == burnOtokenB(address,uint256,address,uint256,uint256).selector) {
        burnOtokenB(e, owner, vaultId, from, index, amount);
    }
    else if (f.selector == settleVault(address,uint256,address).selector) {
        settleVault(e, owner, vaultId, to);
    }
    else if (f.selector ==  depositLongA(address,uint256,address,uint256,uint256).selector) {
         depositLongA(e, owner, vaultId, from, index ,amount);
    }
    else if (f.selector ==  depositLongB(address,uint256,address,uint256,uint256).selector) {
         depositLongB(e, owner, vaultId, from, index ,amount);
    }
    else if (f.selector ==  redeemA(address,uint256).selector) {
         redeemA(e, to, amount);
    }
    else if (f.selector ==  redeemB(address,uint256).selector) {
         redeemB(e, to, amount);
    }
    else {
        calldataarg arg;
        sinvoke f(e,arg);
    }
}

rule onlyValidOtoken(address owner, uint256 vaultId, uint256 index, address otoken, method f) {
    links();
    require shortOtoken.underlyingAsset() == underlying;
    require longOtoken.underlyingAsset() == underlying;
    require shortOtoken.strikeAsset() == strike;
    require longOtoken.strikeAsset() == strike;
    require shortOtoken.collateralAsset() == collateralToken;
    require longOtoken.collateralAsset() == collateralToken;
    require smallVault(owner, vaultId, 1);
    require (otoken == shortOtoken || otoken == longOtoken );
    require ( getVaultShortOtoken(owner, vaultId, index) == otoken || getVaultLongOtoken(owner, vaultId, index) == otoken) 
            => whitelist.isWhitelistedOtoken(otoken);
    uint256 before = pool.getStoredBalance(otoken);
    uint256 totalSupplyBefore = assetTotalSupply(otoken);
    require !whitelist.isWhitelistedCollateral(otoken);
    callFunctionWithParameters(f, owner, vaultId, index);
    uint256 after = pool.getStoredBalance(otoken);
    uint256 totalSupplyAfter = assetTotalSupply(otoken);
    assert ( before != after || totalSupplyBefore != totalSupplyAfter) => whitelist.isWhitelistedOtoken(otoken);
}
