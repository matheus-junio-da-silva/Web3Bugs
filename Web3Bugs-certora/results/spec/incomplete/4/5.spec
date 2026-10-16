// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: integrityOfReturnFunds
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:1-1; certora/specs/base.spec:4-4; certora/specs/base.spec:6-6; certora/specs/base.spec:44-44; certora/specs/base.spec:48-48; certora/specs/base.spec:50-50; certora/specs/allProps.spec:184-200

using DummyERC20Impl as stake_token
methods {
    stake_token.balanceOf(address) returns (uint256) envfree
    returnFunds(uint256)
}
definition AAVE_MAX_SUPPLY() returns uint256 = 16000000 * 10^18;
rule integrityOfReturnFunds(uint256 amount){
    env e;
    require(amount < AAVE_MAX_SUPPLY());
    require(e.msg.sender != currentContract);

    uint256 balanceStakeTokenSenderBefore = stake_token.balanceOf(e.msg.sender);
    uint256 balanceStakeTokenVaultBefore = stake_token.balanceOf(currentContract);
    require(balanceStakeTokenSenderBefore < AAVE_MAX_SUPPLY());
    require(balanceStakeTokenVaultBefore < AAVE_MAX_SUPPLY());
    returnFunds(e, amount);
    uint256 balanceStakeTokenSenderAfter = stake_token.balanceOf(e.msg.sender);
    uint256 balanceStakeTokenVaultAfter = stake_token.balanceOf(currentContract);
    require(balanceStakeTokenVaultAfter > 0);

    assert balanceStakeTokenSenderAfter == balanceStakeTokenSenderBefore - amount;
    assert balanceStakeTokenVaultAfter == balanceStakeTokenVaultBefore + amount;
}
