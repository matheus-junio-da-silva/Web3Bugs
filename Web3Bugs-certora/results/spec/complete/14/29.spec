// Project 14 — Opyn Gamma. Historical CVL, no modern migration.
// Selected active invariant: assetIsNotOtoken, original specs/ValidBalances.spec:355-356
// Included original CVL ranges: specs/ValidBalances.spec:1-71;100-110;143-150;182-189;216-241;252-260;273;294-343;354-360
// Conservative original spec-wide methods/helper context; other properties excluded.
using DummyERC20C as collateralToken
using MarginPool as pool
using Whitelist as whitelist
using OtokenHarnessA as shortOtoken
using OtokenHarnessB as longOtoken
using DummyERC20A as underlying
using DummyERC20B as strike


methods {
    //The tracked asset balance of the system
    pool.getStoredBalance(address) returns uint256 envfree
    
    // ERC20 functions
    collateralToken.totalSupply() returns uint256 envfree
    shortOtoken.totalSupply() returns uint256 envfree
    collateralToken.balanceOf(address) returns uint256 envfree
    longOtoken.balanceOf(address) returns uint256 envfree
    longOtoken.collateralAsset() returns address envfree => CONSTANT
    shortOtoken.collateralAsset() returns address envfree => CONSTANT

    // get the cash value for an otoken afte rexpiry
    getPayout(address, uint256) returns uint256 envfree
    
    getProceed(address, uint256) returns uint256 envfree

    //the amount of collateral in an index in a vault of an owner. i.e.,  vaults[owner][index].collateralAmounts[i]
    getVaultCollateralAmount(address, uint256, uint256)  returns uint256 envfree
    //the collateral asset of an index in a vault of an owner. i.e., vaults[owner][index].collateralAssets(i)
    getVaultCollateralAsset(address, uint256, uint256)  returns address envfree
    //the amount of long in an index in a vault of an owner. i.e.,  vaults[owner][index].longAmounts[i]
    getVaultLongAmount(address, uint256, uint256)  returns uint256 envfree
    //the long oToken in an index in a vault of an owner. i.e.,  vaults[owner][index].longOtoken[i]
    getVaultLongOtoken(address, uint256, uint256)  returns address envfree
    //the amount of long in an index in a vault of an owner. i.e.,  vaults[owner][index].shortAmounts[i]
    getVaultShortAmount(address, uint256, uint256)  returns uint256 envfree
    //the long oToken in an index in a vault of an owner. i.e.,  vaults[owner][index].shortOtoken[i]
    getVaultShortOtoken(address, uint256, uint256)  returns address envfree
	// checks if the vault is expired (true when there is an otoken which we can check expiry for)
    isVaultExpired(address, uint256) returns bool
    // checks if vault is "small" all lengths shorter than a constant
    smallVault(address, uint256, uint256) returns bool envfree
    // checks that a vault is valid
    isValidVault(address, uint256) returns bool envfree

    // The total supply of an asset. i.e., asset.totalSupply()
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
    
    // summarized functions
    getOtokenDetails() => CONSTANT
    burnOtoken(address, uint256) => CONSTANT
}

function links() {
    require anOtokenA() == shortOtoken;
    require anOtokenB() == longOtoken;
    require dummyERC20C() == collateralToken;
}



/**
@title Valid balance with respect to total collateral before expiry
@notice The sum of a collateral asset across vaults matches the assetBalance stored in the margin pool
        Vasset = { (v,i) v ∈ Vaults.  v.collateralAssets(i) = asset }
        getStoredBalance(asset) = ∑(v,i) ∈ Vasset. v.collateralAmounts[i]

This is proven by showing that change to a single vault is coherent with the change to the stored balance

*/


/**
@title Valid balance of long oTokens
@notice The sum of a long asset across vaults matches the assetBalance stored in the margin pool
        Vasset = { (v,i) v ∈ Vaults.  v.longOtokens(i) = oToken}
        getStoredBalance(oToken) = ∑(v,i) ∈ Vasset. v.longAmounts[i]
*/


/**
@title Valid supply of short oToken before expiry
@notice The sum of a short asset across vaults matches the supply of that short oToken
        Vasset = { (v,i) v ∈ Vaults.  v.shortOtokens(i) = oToken}
        oToken.totalSupply() = ∑(v,i) ∈ Vasset. v.shortAmounts[i]
*/

// rule validBalanceTotalCollateralPostExpiry(address owner, uint256 vaultId, uint256 index, address oToken, address to, address collateral) {
    // env e;
    // require oToken == shortOtoken;
    // require collateral == collateralToken;
    // require isValidVault(owner, vaultId); 
    // require getVaultShortOtoken(owner, vaultId, index) == oToken;
    // require getVaultCollateralAsset(owner, vaultId, index) == collateral;
    // uint256 collateralVaultBefore = getProceed(owner, vaultId);
    // uint256 supplyBefore = shortOtoken.totalSupply();
    // // uint256 collateralBalanceBefore = collateralToken.balanceOf(pool);

    // sinvoke settleVault(e, owner, vaultId, to);

    // uint256 shortVaultAfter = getVaultShortAmount(owner, vaultId, index);
    // uint256 supplyAfter = shortOtoken.totalSupply();
    // // uint256 collateralBalanceAfter = collateralToken.balanceOf(pool);
    // assert shortVaultAfter == 0;
    // assert supplyAfter == supplyBefore;
    // // assert collateralBalanceBefore - collateralBalanceAfter == collateralVaultBefore;
    
    // 1. in a single tx only 1 vault can be modified 
    // 

// }



/**
@title Valid balance of the system
@notice The balance of the system at an external asset is correlated with the tracked  asset balance
        getStoredBalance(asset) ≤ asset.balanceOf(MarginPool)
*/
// XX Instantiated for collateral token
/*isValidAsset(asset) => */



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


invariant assetIsNotOtoken(address a)
    !(whitelist.isWhitelistedOtoken(a) && whitelist.isWhitelistedCollateral(a))
   



