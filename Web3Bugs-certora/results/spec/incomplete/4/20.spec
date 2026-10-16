// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: previewStakeEquivalentStake
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:15-15; certora/specs/base.spec:18-18; certora/specs/base.spec:27-27; certora/specs/base.spec:41-41; certora/specs/base.spec:42-42; certora/specs/base.spec:48-48; certora/specs/invariants.spec:78-109; certora/specs/allProps.spec:628-638

methods {
    balanceOf(address) returns (uint256) envfree
    totalSupply() returns (uint256) envfree
    previewStake(uint256) returns (uint256) envfree
    stake(address,uint256)
    redeem(address,uint256)
}
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
rule previewStakeEquivalentStake(method f, env e, address to, uint256 amount){
    requireInvariant totalSupplyGreaterThanUserBalance(to);
    uint256 amountOfShares = previewStake(amount);
    uint256 _receiverBalance = balanceOf(to);

    stake(e, to, amount);

    uint256 receiverBalance_ = balanceOf(to);

    assert(amountOfShares == receiverBalance_ - _receiverBalance);
}
