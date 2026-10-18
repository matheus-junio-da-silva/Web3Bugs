// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/bentoBoxCompoundStrategy.spec:151-163 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenA

using DummyWeth as wethTokenImpl

using CompoundStrategyHarness as strategyInstance

using Borrower as borrower

methods {
	totalTokenAmount(address token) returns (uint128) envfree
	tokenBalanceOf(address token) returns (uint256) envfree
	tokenBalanceOfUser(address token, address user) returns (uint256) envfree // external balanceOf
	harnessBorrower() returns (address) envfree
	harnessToken() returns (address) envfree
}

rule totalAssetsAfterFlashLoan(address token) {
	//link the strategy to the current token
	require harnessBorrower() == borrower;
	require harnessToken() == token;
	//assume solvency safe assumption as we know that solvency is kept before and after flash loan
	require tokenBalanceOf(token) == totalTokenAmount(token);
	uint256 _systemBalance = tokenBalanceOfUser(token, currentContract);
	env e;
	calldataarg args;
	flashLoan(e, args);
	uint256 systemBalance_ = tokenBalanceOfUser(token, currentContract);
	assert  systemBalance_ >= _systemBalance, "system lost assets due to flahs loan";
}
