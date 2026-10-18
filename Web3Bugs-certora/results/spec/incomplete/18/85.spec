// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Wrapper.spec lines 91-114
// Target: ERC20Wrapper (historical underlying-token harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Wrapper.spec:4-8
methods {
    underlying() returns(address) envfree
    underlyingBalanceOf(address) returns(uint256) envfree
    depositFor(address, uint256) returns(bool)
}

rule depositForSpecUnderlying(env e){
    address account; uint256 amount;

    require e.msg.sender != currentContract;
    require underlying() != currentContract;

    uint256 underlyingSenderBalanceBefore = underlyingBalanceOf(e.msg.sender);
    uint256 underlyingUserBalanceBefore = underlyingBalanceOf(account);

    depositFor(e, account, amount);

    uint256 underlyingSenderBalanceAfter = underlyingBalanceOf(e.msg.sender);
    uint256 underlyingUserBalanceAfter = underlyingBalanceOf(account);

    assert account == e.msg.sender => underlyingSenderBalanceBefore == underlyingUserBalanceBefore
                && underlyingSenderBalanceAfter == underlyingUserBalanceAfter
                && underlyingSenderBalanceBefore == underlyingSenderBalanceAfter + amount, "underlying balances wrong update";
    
    assert account != e.msg.sender && account == currentContract => underlyingSenderBalanceBefore == underlyingSenderBalanceAfter + amount
                && underlyingUserBalanceBefore == underlyingUserBalanceAfter - amount, "underlying balances wrong update";
    
    assert account != e.msg.sender && account != currentContract => underlyingSenderBalanceBefore == underlyingSenderBalanceAfter + amount
                && underlyingUserBalanceBefore == underlyingUserBalanceAfter, "underlying balances wrong update";
}
