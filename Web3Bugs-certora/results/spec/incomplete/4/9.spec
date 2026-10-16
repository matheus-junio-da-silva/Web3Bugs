// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: totalSupplyDoesNotDropToZero
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:18-18; certora/specs/base.spec:42-42; certora/specs/base.spec:48-48; certora/specs/base.spec:74-80; certora/specs/allProps.spec:287-296

methods {
    totalSupply() returns (uint256) envfree
    redeem(address,uint256)
}
definition redeem_funcs(method f) returns bool =
(
    f.selector == redeem(address, uint256).selector ||
    f.selector == redeemOnBehalf(address, address, uint256).selector ||
    f.selector == claimRewardsAndRedeem(address, uint256, uint256).selector ||
    f.selector == claimRewardsAndRedeemOnBehalf(address, address, uint256, uint256).selector
);
rule totalSupplyDoesNotDropToZero(method f, calldataarg args, env e)
filtered {
    f -> !f.isView && !redeem_funcs(f)
} {
    require totalSupply() > 0;

    f(e, args);

    assert totalSupply() > 0;
}
