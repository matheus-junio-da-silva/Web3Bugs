// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: integrityOfStaking
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:1-1; certora/specs/base.spec:4-4; certora/specs/base.spec:6-6; certora/specs/base.spec:15-15; certora/specs/base.spec:20-20; certora/specs/base.spec:22-22; certora/specs/base.spec:41-41; certora/specs/base.spec:48-48; certora/specs/base.spec:50-50; certora/specs/base.spec:51-51; certora/specs/allProps.spec:32-59

using DummyERC20Impl as stake_token
methods {
    stake_token.balanceOf(address) returns (uint256) envfree
    balanceOf(address) returns (uint256) envfree
    stakersCooldowns(address) returns (uint40, uint216) envfree
    getExchangeRate() returns (uint216) envfree
    stake(address,uint256)
}
definition AAVE_MAX_SUPPLY() returns uint256 = 16000000 * 10^18;
definition EXCHANGE_RATE_FACTOR() returns uint256 = 10^18;
rule integrityOfStaking(address onBehalfOf, uint256 amount) {
    env e;
    require(amount < AAVE_MAX_SUPPLY());
    require(e.msg.sender != currentContract);

    uint256 balanceStakeTokenDepositorBefore = stake_token.balanceOf(e.msg.sender);
    uint256 balanceStakeTokenVaultBefore = stake_token.balanceOf(currentContract);
    uint256 balanceBefore = balanceOf(onBehalfOf);
    require(balanceStakeTokenDepositorBefore < AAVE_MAX_SUPPLY());
    require(balanceStakeTokenVaultBefore < AAVE_MAX_SUPPLY());
    require(balanceBefore < AAVE_MAX_SUPPLY());
    uint72 cooldownBefore;
    cooldownBefore, _ = stakersCooldowns(onBehalfOf);
    require(cooldownBefore == 0);
    stake(e, onBehalfOf, amount);
    uint256 balanceAfter = balanceOf(onBehalfOf);
    uint72 cooldownAfter;
    cooldownAfter, _ = stakersCooldowns(onBehalfOf);
    uint256 balanceStakeTokenDepositorAfter = stake_token.balanceOf(e.msg.sender);
    uint256 balanceStakeTokenVaultAfter = stake_token.balanceOf(currentContract);

    uint216 currentExchangeRate = getExchangeRate();

    assert balanceAfter == balanceBefore +
        amount * currentExchangeRate / EXCHANGE_RATE_FACTOR();
    assert balanceStakeTokenDepositorAfter == balanceStakeTokenDepositorBefore - amount;
    assert balanceStakeTokenVaultAfter == balanceStakeTokenVaultBefore + amount;
}
