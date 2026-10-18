// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Wrapper.spec lines 44-63
// Target: ERC20Wrapper (historical underlying-token harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Wrapper.spec:4-8
methods {
    underlying() returns(address) envfree
    underlyingTotalSupply() returns(uint256) envfree
    underlyingBalanceOf(address) returns(uint256) envfree
    depositFor(address, uint256) returns(bool)
}

// Original CVL declaration: erc20.spec:6-6
methods {
    totalSupply()                         returns (uint256) => DISPATCHER(true)
}

rule depositForSpecBasic(env e){
    address account; uint256 amount;

    require e.msg.sender != currentContract;
    require underlying() != currentContract;

    uint256 wrapperTotalBefore = totalSupply(e);
    uint256 underlyingTotalBefore = underlyingTotalSupply();
    uint256 underlyingThisBalanceBefore = underlyingBalanceOf(currentContract);

    depositFor(e, account, amount);

    uint256 wrapperTotalAfter = totalSupply(e);
    uint256 underlyingTotalAfter = underlyingTotalSupply();
    uint256 underlyingThisBalanceAfter = underlyingBalanceOf(currentContract);

    assert wrapperTotalBefore == wrapperTotalAfter - amount, "wrapper total wrong update";
    assert underlyingTotalBefore == underlyingTotalAfter, "underlying total was updated";
    assert underlyingThisBalanceBefore == underlyingThisBalanceAfter - amount, "underlying this balance wrong update";
}
