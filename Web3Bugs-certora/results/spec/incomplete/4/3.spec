// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: noSlashingMoreThanMax
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:1-1; certora/specs/base.spec:4-4; certora/specs/base.spec:6-6; certora/specs/base.spec:24-24; certora/specs/base.spec:43-43; certora/specs/base.spec:48-48; certora/specs/base.spec:50-50; certora/specs/base.spec:52-52; certora/specs/base.spec:56-56; certora/specs/allProps.spec:98-112

using DummyERC20Impl as stake_token
methods {
    stake_token.balanceOf(address) returns (uint256) envfree
    getMaxSlashablePercentage() returns (uint256) envfree
    slash(address,uint256) returns (uint256)
}
definition AAVE_MAX_SUPPLY() returns uint256 = 16000000 * 10^18;
definition PERCENTAGE_FACTOR() returns uint256 = 10^4;
definition MAX_PERCENTAGE() returns uint256 = 100 * PERCENTAGE_FACTOR();
rule noSlashingMoreThanMax(uint256 amount, address recipient){
    env e;
    uint vaultBalanceBefore = stake_token.balanceOf(currentContract);
    require(vaultBalanceBefore < AAVE_MAX_SUPPLY());
    require(getMaxSlashablePercentage() >= PERCENTAGE_FACTOR() &&
        getMaxSlashablePercentage() <= MAX_PERCENTAGE());
    uint256 maxSlashable = vaultBalanceBefore * getMaxSlashablePercentage() / PERCENTAGE_FACTOR();

    require (amount > maxSlashable);
    require (recipient != currentContract);
    slash(e, recipient, amount);
    uint vaultBalanceAfter = stake_token.balanceOf(currentContract);

    assert vaultBalanceBefore - vaultBalanceAfter == maxSlashable;
}
