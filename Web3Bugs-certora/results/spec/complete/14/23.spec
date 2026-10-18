// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/ValidBalances.spec:151-181
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using DummyERC20C as collateralToken

using MarginPool as pool

using OtokenHarnessA as shortOtoken

using OtokenHarnessB as longOtoken

methods {
    longOtoken.balanceOf(address) returns uint256 envfree
    longOtoken.collateralAsset() returns address envfree => CONSTANT
    getVaultLongAmount(address, uint256, uint256)  returns uint256 envfree
    getVaultLongOtoken(address, uint256, uint256)  returns address envfree
    smallVault(address, uint256, uint256) returns bool envfree
    anOtokenA() returns address envfree
    anOtokenB() returns address envfree
    dummyERC20C() returns address envfree
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

rule validBalanceTotalLong(address owner, uint256 vaultId, uint256 index, method f, address secondAddress, uint256 amount, address asset)
description "$f breaks the validity of stored balance of long asset"
{
    links();
    env e;
    require asset == longOtoken;
    require getVaultLongOtoken(owner, vaultId, index) == asset;
    uint256 longVaultBefore = getVaultLongAmount(owner, vaultId, index);
    uint256 poolBalanceBefore = longOtoken.balanceOf(pool);
    // the margin pool can neither be the owner nor the msg sender since it is a contract. 
    require (owner != pool);
    require (e.msg.sender != pool);

    if (f.selector == depositLongB(address,uint256,address,uint256,uint256).selector) {
        sinvoke depositLongB(e, owner, vaultId, secondAddress, index, amount);
	} else if (f.selector == mintOtokenB(address,uint256,address,uint256,uint256).selector) {
        // ignore the case where you can mint otokens directly to the margin pool
        require (secondAddress != pool);
        sinvoke mintOtokenB(e, owner, vaultId, secondAddress, index, amount);
	} else {
        require smallVault(owner, vaultId, 1);
        require longOtoken.collateralAsset() == collateralToken;
        callFunctionWithParameters(f, owner, vaultId, index);
    }
    
    uint256 longVaultAfter = getVaultLongAmount(owner, vaultId, index);
    uint256 poolBalanceAfter = longOtoken.balanceOf(pool);

    assert longVaultBefore != longVaultAfter => ( poolBalanceAfter - poolBalanceBefore ==  longVaultAfter - longVaultBefore);
    assert poolBalanceAfter != poolBalanceBefore => ( poolBalanceAfter - poolBalanceBefore ==  longVaultAfter - longVaultBefore);
}
