// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: rewardsGetterEquivalentClaim
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:2-2; certora/specs/base.spec:4-4; certora/specs/base.spec:9-9; certora/specs/base.spec:48-48; certora/specs/allProps.spec:352-363

using DummyERC20Impl as reward_token
methods {
    REWARDS_VAULT() returns (address) envfree
}
rule rewardsGetterEquivalentClaim(method f, env e, address to, address from) {
    require to != REWARDS_VAULT();
    uint256 deservedRewards = getTotalRewardsBalance(e, from);
    uint256 _receiverBalance = reward_token.balanceOf(to);

    uint256 claimedAmount = claimRewardsOnBehalf(e, from, to, max_uint256);

    uint256 receiverBalance_ = reward_token.balanceOf(to);

    assert(deservedRewards == claimedAmount);
    assert(receiverBalance_ == _receiverBalance + claimedAmount);
}
