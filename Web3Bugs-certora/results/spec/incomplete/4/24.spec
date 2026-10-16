// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: cooldownAmountNotGreaterThanBalance
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:15-15; certora/specs/base.spec:16-16; certora/specs/base.spec:17-17; certora/specs/base.spec:18-18; certora/specs/base.spec:42-42; certora/specs/base.spec:48-48; certora/specs/invariants.spec:35-44; certora/specs/invariants.spec:78-109; certora/specs/invariants.spec:51-71

methods {
    balanceOf(address) returns (uint256) envfree
    cooldownAmount(address) returns (uint216) envfree
    cooldownTimestamp(address) returns (uint40) envfree
    totalSupply() returns (uint256) envfree
    redeem(address,uint256)
}
invariant cooldownDataCorrectness(address user, env e)
    cooldownAmount(user) > 0 => cooldownTimestamp(user) > 0
    {
        preserved with (env e2)
        {
            require e2.block.timestamp == e.block.timestamp;
            require e.block.timestamp > 0;
            require e.block.timestamp < 2^32;
        }
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
invariant cooldownAmountNotGreaterThanBalance(address user)
    balanceOf(user) >= cooldownAmount(user)
    {
        preserved with (env e1)
        {
            requireInvariant cooldownDataCorrectness(user, e1);
            requireInvariant totalSupplyGreaterThanUserBalance(user);
        }
        preserved transferFrom(address from, address to, uint256 amount) with (env e2)
        {
            require balanceOf(from) + balanceOf(to) <= totalSupply();
            requireInvariant cooldownDataCorrectness(user, e2);
            requireInvariant totalSupplyGreaterThanUserBalance(user);
        }
        preserved transfer(address to, uint256 amount) with (env e3)
        {
            require balanceOf(e3.msg.sender) + balanceOf(to) <= totalSupply();
            requireInvariant cooldownDataCorrectness(user, e3);
            requireInvariant totalSupplyGreaterThanUserBalance(user);
        }
    }
