// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/ValidBalances.spec:344-353
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using DummyERC20C as collateralToken

using MarginPool as pool

using Whitelist as whitelist

using OtokenHarnessA as shortOtoken

using OtokenHarnessB as longOtoken

methods {
    getVaultLongOtoken(address, uint256, uint256)  returns address envfree
    getVaultShortOtoken(address, uint256, uint256)  returns address envfree
    whitelist.isWhitelistedOtoken(address) returns bool envfree
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

rule OtokenInVaultIsWhitelisted(address owner, uint256 vaultId, uint256 index, address otoken, method f)
{
    links();
    require (otoken == shortOtoken || otoken == longOtoken );
    require ( getVaultShortOtoken(owner, vaultId, index) == otoken || getVaultLongOtoken(owner, vaultId, index) == otoken) 
                => whitelist.isWhitelistedOtoken(otoken);
    callFunctionWithParameters(f, owner, vaultId, index);
    assert ( getVaultShortOtoken(owner, vaultId, index) == otoken || getVaultLongOtoken(owner, vaultId, index) == otoken) 
                => whitelist.isWhitelistedOtoken(otoken);
}
