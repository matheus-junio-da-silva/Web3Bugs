// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Wrapper.spec lines 162-187
// Target: ERC20Wrapper (historical underlying-token harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Wrapper.spec:4-9
methods {
    underlying() returns(address) envfree
    underlyingBalanceOf(address) returns(uint256) envfree
    withdrawTo(address, uint256) returns(bool)
}

rule withdrawToSpecUnderlying(env e){
    address account; uint256 amount;

    require e.msg.sender != currentContract;
    require underlying() != currentContract;

    uint256 underlyingSenderBalanceBefore = underlyingBalanceOf(e.msg.sender);
    uint256 underlyingUserBalanceBefore = underlyingBalanceOf(account);
    uint256 underlyingThisBalanceBefore = underlyingBalanceOf(currentContract);

    withdrawTo(e, account, amount);

    uint256 underlyingSenderBalanceAfter = underlyingBalanceOf(e.msg.sender);
    uint256 underlyingUserBalanceAfter = underlyingBalanceOf(account);
    uint256 underlyingThisBalanceAfter = underlyingBalanceOf(currentContract);

    assert account == e.msg.sender => underlyingSenderBalanceBefore == underlyingUserBalanceBefore 
                && underlyingSenderBalanceAfter == underlyingUserBalanceAfter 
                && underlyingUserBalanceBefore == underlyingUserBalanceAfter - amount, "underlying balances wrong update (acc == sender)";
    
    assert account != e.msg.sender && account == currentContract => underlyingUserBalanceBefore == underlyingUserBalanceAfter
                && underlyingSenderBalanceBefore == underlyingSenderBalanceAfter, "underlying balances wrong update (acc == contract)"; 
    assert account != e.msg.sender && account != currentContract => underlyingUserBalanceBefore == underlyingUserBalanceAfter - amount
                && underlyingSenderBalanceBefore == underlyingSenderBalanceAfter
                && underlyingThisBalanceBefore == underlyingThisBalanceAfter + amount, "underlying balances wrong update (acc != contract)";   
}
