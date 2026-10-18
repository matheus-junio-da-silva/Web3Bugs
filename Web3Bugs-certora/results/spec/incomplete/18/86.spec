// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Wrapper.spec lines 119-134
// Target: ERC20Wrapper (historical underlying-token harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Wrapper.spec:4-9
methods {
    underlying() returns(address) envfree
    underlyingTotalSupply() returns(uint256) envfree
    withdrawTo(address, uint256) returns(bool)
}

// Original CVL declaration: erc20.spec:6-6
methods {
    totalSupply()                         returns (uint256) => DISPATCHER(true)
}

rule withdrawToSpecBasic(env e){
    address account; uint256 amount;

    require underlying() != currentContract;

    uint256 wrapperTotalBefore = totalSupply(e);
    uint256 underlyingTotalBefore = underlyingTotalSupply();

    withdrawTo(e, account, amount);

    uint256 wrapperTotalAfter = totalSupply(e);
    uint256 underlyingTotalAfter = underlyingTotalSupply();

    assert wrapperTotalBefore == wrapperTotalAfter + amount, "wrapper total wrong update";
    assert underlyingTotalBefore == underlyingTotalAfter, "underlying total was updated";
}
