// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: allSharesAreBacked
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:1-1; certora/specs/base.spec:4-4; certora/specs/base.spec:6-6; certora/specs/base.spec:12-12; certora/specs/base.spec:18-18; certora/specs/base.spec:22-22; certora/specs/base.spec:28-28; certora/specs/base.spec:40-40; certora/specs/base.spec:41-41; certora/specs/base.spec:44-44; certora/specs/base.spec:48-48; certora/specs/base.spec:57-57; certora/specs/summarizations.spec:3-6; certora/specs/propertiesWithSummarizations.spec:9-30

using DummyERC20Impl as stake_token
methods {
    stake_token.balanceOf(address) returns (uint256) envfree
    INITIAL_EXCHANGE_RATE() returns (uint216) envfree
    totalSupply() returns (uint256) envfree
    getExchangeRate() returns (uint216) envfree
    previewRedeem(uint256) returns (uint256) envfree
    initialize(address,address,address,uint256,uint256)
    stake(address,uint256)
    returnFunds(uint256)
}
definition INITIAL_EXCHANGE_RATE() returns uint256 = 10^18;
methods {
    _getRewards(uint256, uint256, uint256) => NONDET
    _getAssetIndex(uint256, uint256, uint128, uint256) => NONDET
}
invariant allSharesAreBacked()
    previewRedeem(totalSupply()) <= stake_token.balanceOf(currentContract)
    {
        preserved stake(address to, uint256 amount) with (env e2)
        {
            require e2.msg.sender != currentContract;
        }
        preserved stakeWithPermit(address from, uint256 amount, uint256 deadline,
            uint8 v, bytes32 r, bytes32 s) with (env e3)
        {
            require from != currentContract;
        }
        preserved returnFunds(uint256 amount) with (env e4)
        {
            require e4.msg.sender != currentContract;
        }
        preserved initialize(address slashingAdmin, address cooldownPauseAdmin, address claimHelper,
                            uint256 maxSlashablePercentage, uint256 cooldownSeconds) with (env e5)
        {
            require getExchangeRate() == INITIAL_EXCHANGE_RATE();
        }
    }
