// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: rewardsMonotonicallyIncrease
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/allProps.spec:372-380

rule rewardsMonotonicallyIncrease(address user, env e, env e2) {
    uint256 _deservedRewards = getTotalRewardsBalance(e, user);

    require e2.block.timestamp >= e.block.timestamp;

    uint256 deservedRewards_ = getTotalRewardsBalance(e2, user);

    assert(deservedRewards_ >= _deservedRewards);
}
