// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/ValidBalances.spec:72-99
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using DummyERC20C as collateralToken

using MarginPool as pool

using OtokenHarnessA as shortOtoken

using OtokenHarnessB as longOtoken

methods {
    pool.getStoredBalance(address) returns uint256 envfree
    getVaultCollateralAmount(address, uint256, uint256)  returns uint256 envfree
    getVaultCollateralAsset(address, uint256, uint256)  returns address envfree
    getVaultLongAmount(address, uint256, uint256)  returns uint256 envfree
    getVaultLongOtoken(address, uint256, uint256)  returns address envfree
    getVaultShortAmount(address, uint256, uint256)  returns uint256 envfree
    getVaultShortOtoken(address, uint256, uint256)  returns address envfree
    smallVault(address, uint256, uint256) returns bool envfree
    assetTotalSupply(address) returns uint256 envfree
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

rule validState(address owner, uint256 vaultId, uint256 index,  method f) 
{
    links();
    /* TODO: Redeem */
    require f.selector != redeemA(address,uint256).selector && f.selector != redeemB(address,uint256).selector;
    /* TODO: depositLongB */
    require f.selector != depositLongB(address,uint256,address,uint256,uint256).selector;
    
    require smallVault(owner, vaultId, 1);
    require shortOtoken == getVaultShortOtoken(owner, vaultId, index) &&
            longOtoken == getVaultLongOtoken(owner, vaultId, index) &&
            collateralToken == getVaultCollateralAsset(owner, vaultId, index) 
    ;
    
    require assetTotalSupply(shortOtoken) >= (pool.getStoredBalance(shortOtoken) + getVaultShortAmount(owner, vaultId, index)) &&
            assetTotalSupply(longOtoken) >= pool.getStoredBalance(longOtoken) &&
            pool.getStoredBalance(longOtoken) >= getVaultLongAmount(owner, vaultId, index) &&
            pool.getStoredBalance(collateralToken) >= getVaultCollateralAmount(owner, vaultId, index) 
    ;
    
    callFunctionWithParameters(f, owner, vaultId, index);
    
    assert  assetTotalSupply(shortOtoken) >= (pool.getStoredBalance(shortOtoken) + getVaultShortAmount(owner, vaultId, index)) &&
            assetTotalSupply(longOtoken) >= pool.getStoredBalance(longOtoken) &&
            pool.getStoredBalance(longOtoken) >= getVaultLongAmount(owner, vaultId, index) &&
            pool.getStoredBalance(collateralToken) >= getVaultCollateralAmount(owner, vaultId, index) 
    ;
}
