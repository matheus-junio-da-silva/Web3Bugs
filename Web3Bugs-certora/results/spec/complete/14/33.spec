// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/controller.spec:122-133
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using DummyERC20C as collateralToken

using MarginPoolHarness as pool

methods {
    collateralToken.balanceOf(address) returns uint256 envfree
}

rule collateralWithdrawsRestricted(address owner, uint256 vaultId, uint256 index, method f) {
    env e;
    uint256 collateralBalanceBefore = collateralToken.balanceOf(pool);
    calldataarg arg;
    sinvoke f(e, arg);
    uint256 collateralBalanceAfter = collateralToken.balanceOf(pool);

    assert collateralBalanceAfter < collateralBalanceBefore => (f.selector == settleVault(address,uint256,address).selector) 
                                                            || (f.selector == redeemB(address,uint256).selector)
                                                            || (f.selector == redeemA(address,uint256).selector)
                                                            || (f.selector == withdrawCollateral(address,uint256,address,uint256,uint256).selector);
}
