// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/bentoBoxCompoundStrategy.spec:97-98 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenA

using DummyWeth as wethTokenImpl

using CompoundStrategyHarness as strategyInstance

using Borrower as borrower

methods {
	totalTokenShare(address token) returns (uint128) envfree
}

ghost shareSum(uint) returns uint256 {
    init_state axiom forall address token. shareSum(token) == 0;
}

hook Sstore balanceOf[KEY uint token][KEY uint a] uint balance (uint oldBalance) STORAGE {
	havoc shareSum assuming shareSum@new(token) == shareSum@old(token) + balance - oldBalance &&
		(forall uint t. t != token => shareSum@new(t) == shareSum@old(t));
}

invariant integrityOfTotalShare(address token) 
 	totalTokenShare(token) == shareSum(token)
