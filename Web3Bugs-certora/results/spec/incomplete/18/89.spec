// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Wrapper.spec lines 192-214
// Target: ERC20Wrapper (historical underlying-token harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Wrapper.spec:6-10
methods {
    underlyingBalanceOf(address) returns(uint256) envfree
    _recover(address) returns(uint256)
}

// Original CVL declaration: erc20.spec:6-7
methods {
    totalSupply()                         returns (uint256) => DISPATCHER(true)
    balanceOf(address)                    returns (uint256) => DISPATCHER(true)
}

rule recoverSpec(env e){
    address account; uint256 amount;

    uint256 wrapperTotalBefore = totalSupply(e);
    uint256 wrapperUserBalanceBefore = balanceOf(e, account);
    uint256 wrapperSenderBalanceBefore = balanceOf(e, e.msg.sender);
    uint256 underlyingThisBalanceBefore = underlyingBalanceOf(currentContract);

    mathint value = underlyingThisBalanceBefore - wrapperTotalBefore;

    _recover(e, account);

    uint256 wrapperTotalAfter = totalSupply(e);
    uint256 wrapperUserBalanceAfter = balanceOf(e, account);
    uint256 wrapperSenderBalanceAfter = balanceOf(e, e.msg.sender);
    
    assert wrapperTotalBefore == wrapperTotalAfter - value, "wrapper total wrong update";
    assert e.msg.sender == account => wrapperUserBalanceBefore == wrapperSenderBalanceBefore
                && wrapperUserBalanceAfter == wrapperSenderBalanceAfter
                && wrapperUserBalanceBefore == wrapperUserBalanceAfter - value, "wrapper balances wrong update";
    assert e.msg.sender != account => wrapperUserBalanceBefore == wrapperUserBalanceAfter - value
                && wrapperSenderBalanceBefore == wrapperSenderBalanceAfter, "wrapper balances wrong update";
}
