// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Wrapper.spec lines 68-86
// Target: ERC20Wrapper (historical underlying-token harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Wrapper.spec:4-8
methods {
    underlying() returns(address) envfree
    depositFor(address, uint256) returns(bool)
}

// Original CVL declaration: erc20.spec:7-7
methods {
    balanceOf(address)                    returns (uint256) => DISPATCHER(true)
}

rule depositForSpecWrapper(env e){
    address account; uint256 amount;

    require underlying() != currentContract;

    uint256 wrapperUserBalanceBefore = balanceOf(e, account);
    uint256 wrapperSenderBalanceBefore = balanceOf(e, e.msg.sender);

    depositFor(e, account, amount);

    uint256 wrapperUserBalanceAfter = balanceOf(e, account);
    uint256 wrapperSenderBalanceAfter = balanceOf(e, e.msg.sender);

    assert account == e.msg.sender => wrapperUserBalanceBefore == wrapperSenderBalanceBefore 
                && wrapperUserBalanceAfter == wrapperSenderBalanceAfter 
                && wrapperUserBalanceBefore == wrapperUserBalanceAfter - amount, "wrapper balances wrong update";
    assert account != e.msg.sender => wrapperUserBalanceBefore == wrapperUserBalanceAfter - amount
                && wrapperSenderBalanceBefore == wrapperSenderBalanceAfter, "wrapper balances wrong update";
}
