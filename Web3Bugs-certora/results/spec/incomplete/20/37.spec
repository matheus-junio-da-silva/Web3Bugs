// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/strategy.spec:88-104 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenInstance 

using Receiver as receiverInstance

methods {
	receiver() returns (address) envfree
	tokenInstance.balanceOf(address account) returns (uint256) envfree
	compareLTzero(int256 x) returns (bool) envfree
	checkAplusBeqC(uint256 a, int256 b, uint256 c) returns (bool) envfree
}

definition MAX_UNSIGNED_INT() returns uint256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

rule integrityExit(uint256 balance) {
	require receiver() == receiverInstance;

	uint256 strategyBalanceBefore = tokenInstance.balanceOf(currentContract);
	uint256 balanceBefore = tokenInstance.balanceOf(receiverInstance);
	
	env e;
	int256 amountAdded = exit(e, balance);
	
	uint256 strategyBalanceBAfter = tokenInstance.balanceOf(currentContract);
	uint256 balanceAfter = tokenInstance.balanceOf(receiverInstance);

	mathint t = balanceBefore + balance;
	require t <= MAX_UNSIGNED_INT();
	uint256 expectedBalance = balanceBefore + balance;
	assert checkAplusBeqC(expectedBalance, amountAdded, balanceAfter), "wrong balance transfered to receiver";
	assert compareLTzero(amountAdded) => strategyBalanceBefore < balance , "did not send all availaible tokens";
}
