// Project 14 — Opyn Gamma. Historical CVL, no modern migration.
// Selected active rule: settleVault, original specs/controller.spec:52-72
// Included original CVL ranges: specs/controller.spec:1-73;100;121;134;153-188
// Conservative original spec-wide methods/helper context; other properties excluded.
using DummyERC20C as collateralToken
using MarginPoolHarness as pool
using Whitelist as whitelist
using OtokenHarnessA as shortOtoken
using OtokenHarnessB as longOtoken

methods {
    //The tracked asset balance of the system
    pool.getStoredBalance(address) returns uint256 envfree
    
    // ERC20 functions
    collateralToken.totalSupply() returns uint256 envfree
    shortOtoken.totalSupply() returns uint256 envfree
    collateralToken.balanceOf(address) returns uint256 envfree
    longOtoken.balanceOf(address) returns uint256 envfree
    shortOtoken.balanceOf(address) returns uint256 envfree

    // get the cash value for an otoken afte rexpiry
    getPayout(address, uint256) returns uint256 envfree
    // get the amount of collateral that can be taken out of a vault
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

    // summarized functions
    expiryTimestamp() => CONSTANT
    burnOtoken(address, uint256) => CONSTANT
}

rule settleVault (address owner, uint256 vaultId, uint256 index, address oToken, address to, address collateral) {
    env e;
    require oToken == shortOtoken;
    require collateral == collateralToken;
    require getVaultShortOtoken(owner, vaultId, 0) == oToken;
    require getVaultCollateralAsset(owner, vaultId, 0) == collateral;
    require to != pool; 

    uint256 supplyBefore = shortOtoken.totalSupply();
    uint256 amountRemoved = getProceed(owner, vaultId);
    uint256 poolBalanceBefore = collateralToken.balanceOf(pool);

    sinvoke settleVault(e, owner, vaultId, to);

    uint256 supplyAfter = shortOtoken.totalSupply();
    uint256 poolBalanceAfter = collateralToken.balanceOf(pool);

    assert supplyAfter == supplyBefore;
    assert poolBalanceAfter != poolBalanceBefore => (poolBalanceBefore - poolBalanceAfter == amountRemoved);

}


 




// rule inverse (address owner, uint256 vaultId, address from, uint256 index, uint256 amount) { 
//     require(isValidVault(owner, vaultId));

//     storage initialStorage = lastStorage;
//     env e1; 
//     calldataarg arg1;
//     sinvoke f1(e1, arg1);
//     env e2;
//     calldataarg arg2;
//     sinvoke f2(e2, arg2);

//     function depositLongA(
//     address owner,
//     uint256 vaultId,
//     address from,
//     uint256 index,
//     uint256 amount
//   ) 
    
//     uint256 vaultCollateralAmount1 = getVaultCollateralAmount(owner, vaultId,0);

//     sinvoke f2(e2, arg2) at initialStorage;
//     sinvoke f2(e1, arg1);

//     uint256 vaultCollateralAmount2 = getVaultCollateralAmount(owner, vaultId,0);

//     assert vaultCollateralAmount1 == vaultCollateralAmount1;
//     // run first method and then second method and store the result 
//     // run the second method then first method and compare result 
// }



