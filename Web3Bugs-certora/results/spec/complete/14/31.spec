// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/controller.spec:74-99
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using DummyERC20C as collateralToken

using MarginPoolHarness as pool

using OtokenHarnessA as shortOtoken

methods {
    shortOtoken.totalSupply() returns uint256 envfree
    collateralToken.balanceOf(address) returns uint256 envfree
    getPayout(address, uint256) returns uint256 envfree
}

rule redeem (address oToken, address to, address collateral, uint256 amount) {
    env e;
    require oToken == shortOtoken;
    require collateral == collateralToken;

    require to != pool; 

    uint256 supplyBefore = shortOtoken.totalSupply();
    uint256 amountRemoved = getPayout(oToken, amount);
    uint256 amount1 = getPayout(oToken, 1);
    uint256 poolBalanceBefore = collateralToken.balanceOf(pool);
    uint256 toBalanceBefore =  collateralToken.balanceOf(to);

    sinvoke redeemA(e, to, amount);

    uint256 supplyAfter = shortOtoken.totalSupply();
    uint256 poolBalanceAfter = collateralToken.balanceOf(pool);
    uint256 toBalanceAfter =  collateralToken.balanceOf(to);

    //assert supplyAfter != supplyBefore => ((supplyBefore - supplyAfter) * amount1 == amountRemoved);
    //assert poolBalanceAfter != poolBalanceBefore => (poolBalanceBefore - poolBalanceAfter == amountRemoved);
    assert supplyBefore - supplyAfter == amount;
    assert poolBalanceBefore - poolBalanceAfter == amountRemoved;
    assert toBalanceAfter - toBalanceBefore == amountRemoved;

}
