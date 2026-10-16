// Project 6 - Aave Static aToken
// Extracted active property: sumAllBalance_eq_totalSupply
// Status: incomplete; property and available CVL dependencies are copied literally below.
// CVL1/CVL2 migration is intentionally not performed.

// Original source: StaticATokenLM.spec:1-1
import "erc20.spec"

// Original source: StaticATokenLM.spec:12-13
methods
{

// Original source: StaticATokenLM.spec:15-16
    totalSupply() returns uint256 envfree
	balanceOf(address) returns (uint256) envfree

// Original source: StaticATokenLM.spec:94-94
 }

// Original source: StaticATokenLM.spec:113-124
/// @title Sum of balances of StaticATokenLM 
ghost sumAllBalance() returns mathint {
    init_state axiom sumAllBalance() == 0;
}

hook Sstore balanceOf[KEY address a] uint256 balance (uint256 old_balance) STORAGE {
  havoc sumAllBalance assuming sumAllBalance@new() == sumAllBalance@old() + balance - old_balance;
}

hook Sload uint256 balance balanceOf[KEY address a] STORAGE {
    require balance <= sumAllBalance();
} 

// Original source: StaticATokenLM.spec:215-217
/// @title Sum of balances=totalSupply()
invariant sumAllBalance_eq_totalSupply()
	sumAllBalance() == totalSupply()
