// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Wrapper.spec lines 31-39
// Target: ERC20Wrapper (historical underlying-token harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Wrapper.spec:4-6
methods {
    underlying() returns(address) envfree
    underlyingBalanceOf(address) returns(uint256) envfree
}

// Original CVL declaration: erc20.spec:6-6
methods {
    totalSupply()                         returns (uint256) => DISPATCHER(true)
}

invariant underTotalAndContractBalanceOfCorrelation(env e)
    totalSupply(e) <= underlyingBalanceOf(currentContract)
    {
        preserved with (env e2) {
            require underlying() != currentContract;
            require e.msg.sender != currentContract;
            require e.msg.sender == e2.msg.sender;
        }
    }
