// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: integrityOfSlashing
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:1-1; certora/specs/base.spec:4-4; certora/specs/base.spec:6-6; certora/specs/base.spec:18-18; certora/specs/base.spec:23-23; certora/specs/base.spec:24-24; certora/specs/base.spec:43-43; certora/specs/base.spec:48-48; certora/specs/base.spec:50-50; certora/specs/base.spec:52-52; certora/specs/base.spec:56-56; certora/specs/allProps.spec:134-163

using DummyERC20Impl as stake_token
methods {
    stake_token.balanceOf(address) returns (uint256) envfree
    totalSupply() returns (uint256) envfree
    inPostSlashingPeriod() returns (bool) envfree
    getMaxSlashablePercentage() returns (uint256) envfree
    slash(address,uint256) returns (uint256)
}
definition AAVE_MAX_SUPPLY() returns uint256 = 16000000 * 10^18;
definition PERCENTAGE_FACTOR() returns uint256 = 10^4;
definition MAX_PERCENTAGE() returns uint256 = 100 * PERCENTAGE_FACTOR();
rule integrityOfSlashing(address to, uint256 amount){
    env e;
    require(amount < AAVE_MAX_SUPPLY());
    require(e.msg.sender != currentContract && to != currentContract);
    require(getMaxSlashablePercentage() >= PERCENTAGE_FACTOR() &&
        getMaxSlashablePercentage() <= MAX_PERCENTAGE());

    require(totalSupply() > 0 && totalSupply() < AAVE_MAX_SUPPLY());
    uint256 total = totalSupply();

    uint256 balanceStakeTokenToBefore = stake_token.balanceOf(to);
    uint256 balanceStakeTokenVaultBefore = stake_token.balanceOf(currentContract);
    require(balanceStakeTokenToBefore < AAVE_MAX_SUPPLY());
    require(balanceStakeTokenVaultBefore < AAVE_MAX_SUPPLY());
    slash(e, to, amount);
    uint256 balanceStakeTokenToAfter = stake_token.balanceOf(to);
    uint256 balanceStakeTokenVaultAfter = stake_token.balanceOf(currentContract);
    uint256 maxSlashable = balanceStakeTokenVaultBefore * getMaxSlashablePercentage() / PERCENTAGE_FACTOR();

    uint256 amountToSlash;
    if (amount > maxSlashable) {
        amountToSlash = maxSlashable;
    } else {
        amountToSlash = amount;
    }

    assert balanceStakeTokenToAfter == balanceStakeTokenToBefore + amountToSlash;
    assert balanceStakeTokenVaultAfter == balanceStakeTokenVaultBefore - amountToSlash;
    assert inPostSlashingPeriod();
}
