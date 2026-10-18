// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC20Wrapper.spec lines 16-26
// Target: ERC20Wrapper (historical underlying-token harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC20Wrapper.spec:5-8
methods {
    underlyingTotalSupply() returns(uint256) envfree
    underlyingBalanceOf(address) returns(uint256) envfree
    depositFor(address, uint256) returns(bool)
}

// Original CVL declaration: erc20.spec:6-6
methods {
    totalSupply()                         returns (uint256) => DISPATCHER(true)
}

invariant whatAboutTotal(env e)
    totalSupply(e) <= underlyingTotalSupply()
    filtered { f -> f.selector != certorafallback_0().selector && !f.isView}
    {
        preserved {
            require underlyingBalanceOf(currentContract) <= underlyingTotalSupply();
        }
        preserved depositFor(address account, uint256 amount) with (env e2){
            require totalSupply(e) + amount <= underlyingTotalSupply();
        }
    }
