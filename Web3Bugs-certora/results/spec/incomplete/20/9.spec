// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/bentoBoxCompoundStrategy.spec:94-95 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenA

using DummyWeth as wethTokenImpl

using CompoundStrategyHarness as strategyInstance

using Borrower as borrower

methods {
	strategy(address) returns (address) envfree
	getStrategyTokenBalance(address token) returns (uint256) envfree
}

invariant zeroStrategy(address token)
	strategy(token) == 0 => getStrategyTokenBalance(token) == 0
