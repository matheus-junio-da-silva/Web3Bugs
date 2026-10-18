// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/ValidBalances.spec:190-215
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using DummyERC20C as collateralToken

using MarginPool as pool

using OtokenHarnessA as shortOtoken

using OtokenHarnessB as longOtoken

methods {
    shortOtoken.totalSupply() returns uint256 envfree
    getVaultShortAmount(address, uint256, uint256)  returns uint256 envfree
    getVaultShortOtoken(address, uint256, uint256)  returns address envfree
    isVaultExpired(address, uint256) returns bool
    anOtokenA() returns address envfree
    anOtokenB() returns address envfree
    dummyERC20C() returns address envfree
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

rule validBalanceTotalShort(address owner, uint256 vaultId, uint256 index, address secondAddress, address oToken, method f, uint256 amount)
description "$f breaks the validity of stored balance of short asset"
{
    links();
    env e;
    calldataarg arg;
    require oToken == shortOtoken;
    require !isVaultExpired(e, owner, vaultId);
    require getVaultShortOtoken(owner, vaultId, index) == oToken;
    uint256 shortVaultBefore = getVaultShortAmount(owner, vaultId, index);
    uint256 supplyBefore = shortOtoken.totalSupply();
    // only test the cases before expiry
    if (f.selector == settleVault(address,uint256,address).selector) ||  (f.selector == redeemA(address,uint256).selector) {
        assert true;
    } else if (f.selector == mintOtokenA(address,uint256,address,uint256,uint256).selector) {
        // ignore the case where you can mint otokens directly to the margin pool
        require (secondAddress != pool);
        sinvoke mintOtokenA(e, owner, vaultId, secondAddress, index, amount);
	} else {
        callFunctionWithParameters(f, owner, vaultId, index);
    }
    uint256 shortVaultAfter = getVaultShortAmount(owner, vaultId, index);
    uint256 supplyAfter = shortOtoken.totalSupply();
    assert shortVaultBefore != shortVaultAfter => (supplyAfter - supplyBefore ==  shortVaultAfter - shortVaultBefore);
    assert supplyAfter != supplyBefore => ( supplyAfter - supplyBefore  ==  shortVaultAfter - shortVaultBefore);
}
