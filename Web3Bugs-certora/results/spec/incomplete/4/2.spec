// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: noStakingPostSlashingPeriod
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:23-23; certora/specs/base.spec:41-41; certora/specs/base.spec:48-48; certora/specs/allProps.spec:74-79

methods {
    inPostSlashingPeriod() returns (bool) envfree
    stake(address,uint256)
}
rule noStakingPostSlashingPeriod(address onBehalfOf, uint256 amount) {
    env e;
    require(inPostSlashingPeriod());
    stake@withrevert(e, onBehalfOf, amount);
    assert lastReverted, "should not be able to stake in post slashing period";
}
