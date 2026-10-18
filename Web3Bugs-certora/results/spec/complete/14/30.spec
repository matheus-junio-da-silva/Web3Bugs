// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/controller.spec:52-72
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using DummyERC20C as collateralToken

using MarginPoolHarness as pool

using OtokenHarnessA as shortOtoken

methods {
    shortOtoken.totalSupply() returns uint256 envfree
    collateralToken.balanceOf(address) returns uint256 envfree
    getProceed(address, uint256) returns uint256 envfree
    getVaultCollateralAsset(address, uint256, uint256)  returns address envfree
    getVaultShortOtoken(address, uint256, uint256)  returns address envfree
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
