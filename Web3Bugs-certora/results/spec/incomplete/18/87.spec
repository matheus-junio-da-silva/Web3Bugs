// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Wrapper.spec lines 139-157
// Target: ERC20Wrapper (historical underlying-token harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Wrapper.spec:4-9
methods {
    underlying() returns(address) envfree
    withdrawTo(address, uint256) returns(bool)
}

// Original CVL declaration: erc20.spec:7-7
methods {
    balanceOf(address)                    returns (uint256) => DISPATCHER(true)
}

rule withdrawToSpecWrapper(env e){
    address account; uint256 amount;

    require underlying() != currentContract;

    uint256 wrapperUserBalanceBefore = balanceOf(e, account);
    uint256 wrapperSenderBalanceBefore = balanceOf(e, e.msg.sender);

    withdrawTo(e, account, amount);

    uint256 wrapperUserBalanceAfter = balanceOf(e, account);
    uint256 wrapperSenderBalanceAfter = balanceOf(e, e.msg.sender);
    
    assert account == e.msg.sender => wrapperUserBalanceBefore == wrapperSenderBalanceBefore
                && wrapperUserBalanceAfter == wrapperSenderBalanceAfter
                && wrapperUserBalanceBefore == wrapperUserBalanceAfter + amount, "wrapper user balance wrong update";
    assert account != e.msg.sender => wrapperSenderBalanceBefore == wrapperSenderBalanceAfter + amount
                && wrapperUserBalanceBefore == wrapperUserBalanceAfter, "wrapper user balance wrong update";
}
