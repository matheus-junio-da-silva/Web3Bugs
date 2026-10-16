// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: rewardsIncreaseForNonClaimFunctions
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:1-1; certora/specs/base.spec:4-4; certora/specs/base.spec:6-6; certora/specs/base.spec:12-12; certora/specs/base.spec:15-15; certora/specs/base.spec:18-18; certora/specs/base.spec:22-22; certora/specs/base.spec:28-28; certora/specs/base.spec:40-40; certora/specs/base.spec:41-41; certora/specs/base.spec:42-42; certora/specs/base.spec:44-44; certora/specs/base.spec:48-48; certora/specs/base.spec:64-72; certora/specs/base.spec:57-57; certora/specs/invariants.spec:78-109; certora/specs/propertiesWithSummarizations.spec:9-30; certora/specs/allProps.spec:405-420

using DummyERC20Impl as stake_token
methods {
    stake_token.balanceOf(address) returns (uint256) envfree
    INITIAL_EXCHANGE_RATE() returns (uint216) envfree
    balanceOf(address) returns (uint256) envfree
    totalSupply() returns (uint256) envfree
    getExchangeRate() returns (uint216) envfree
    previewRedeem(uint256) returns (uint256) envfree
    initialize(address,address,address,uint256,uint256)
    stake(address,uint256)
    redeem(address,uint256)
    returnFunds(uint256)
}
definition claimRewards_funcs(method f) returns bool =
(
    f.selector == claimRewards(address, uint256).selector ||
    f.selector == claimRewardsOnBehalf(address, address, uint256).selector ||
    f.selector == claimRewardsAndStake(address, uint256).selector ||
    f.selector == claimRewardsAndStakeOnBehalf(address, address, uint256).selector ||
    f.selector == claimRewardsAndRedeem(address, uint256, uint256).selector ||
    f.selector == claimRewardsAndRedeemOnBehalf(address, address, uint256, uint256).selector
);
definition INITIAL_EXCHANGE_RATE() returns uint256 = 10^18;
invariant totalSupplyGreaterThanUserBalance(address user)
    totalSupply() >= balanceOf(user)
    {
        preserved transferFrom(address from, address to, uint256 amount) with (env e2)
        {
            require balanceOf(from) + balanceOf(to) <= totalSupply();
        }
        preserved transfer(address to, uint256 amount) with (env e3)
        {
            require balanceOf(e3.msg.sender) + balanceOf(to) <= totalSupply();
        }
        preserved redeem(address to, uint256 amount) with (env e4)
        {
            require to == user;
            require balanceOf(e4.msg.sender) + balanceOf(to) <= totalSupply();
        }
        preserved redeemOnBehalf(address from, address to, uint256 amount) with (env e5)
        {
            require to == user;
            require balanceOf(from) + balanceOf(to) <= totalSupply();
        }
        preserved claimRewardsAndRedeem(address to, uint256 claimAmount, uint256 redeemAmount) with (env e6)
        {
            require to == user;
            require balanceOf(e6.msg.sender) + balanceOf(to) <= totalSupply();
        }
        preserved claimRewardsAndRedeemOnBehalf(address from, address to, uint256 claimAmount, uint256 redeemAmount) with (env e7)
        {
            require to == user;
            require balanceOf(from) + balanceOf(to) <= totalSupply();
        }
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
rule rewardsIncreaseForNonClaimFunctions(method f, address user, env e)
filtered {
    f -> !f.isView && !claimRewards_funcs(f)
} {
    uint256 _deservedRewards = getTotalRewardsBalance(e, user);

    requireInvariant totalSupplyGreaterThanUserBalance(user);
    requireInvariant allSharesAreBacked();

    calldataarg args;
    f(e, args);

    uint256 deservedRewards_ = getTotalRewardsBalance(e, user);

    assert(deservedRewards_ >= _deservedRewards);
}
