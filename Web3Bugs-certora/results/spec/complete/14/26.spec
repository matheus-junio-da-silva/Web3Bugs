// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/ValidBalances.spec:261-272
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using DummyERC20C as collateralToken

using MarginPool as pool

using OtokenHarnessA as shortOtoken

using OtokenHarnessB as longOtoken

using DummyERC20A as underlying

using DummyERC20B as strike

methods {
    pool.getStoredBalance(address) returns uint256 envfree
    collateralToken.balanceOf(address) returns uint256 envfree
    longOtoken.collateralAsset() returns address envfree => CONSTANT
    shortOtoken.collateralAsset() returns address envfree => CONSTANT
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

rule validBalanceOfTheSystem(address owner, uint256 vaultId, uint256 index, method f) {
    links();
    require shortOtoken.underlyingAsset() == underlying;
    require longOtoken.underlyingAsset() == underlying;
    require shortOtoken.strikeAsset() == strike;
    require longOtoken.strikeAsset() == strike;
    require shortOtoken.collateralAsset() == collateralToken;
    require longOtoken.collateralAsset() == collateralToken;
    require pool.getStoredBalance(collateralToken) == sinvoke collateralToken.balanceOf(pool);
    callFunctionWithParameters(f, owner, vaultId, index);
    assert pool.getStoredBalance(collateralToken) == sinvoke collateralToken.balanceOf(pool);
}
