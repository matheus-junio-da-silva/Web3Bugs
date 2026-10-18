// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/strategy.spec:46-67 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenInstance 

using Receiver as receiverInstance

methods {
	receiver() returns (address) envfree
	tokenInstance.balanceOf(address account) returns (uint256) envfree
	compareGTzero(int256 x) returns (bool) envfree
	checkAplusBeqC(uint256 a, int256 b, uint256 c) returns (bool) envfree
}

definition MIN_INT() returns int256 = 0x8000000000000000000000000000000000000000000000000000000000000000;

rule integrityHarvest(uint256 balance, uint256 strategyBalanceBefore) {
	require receiver() == receiverInstance;
	
	require strategyBalanceBefore == tokenInstance.balanceOf(currentContract);
	uint256 balanceBefore = tokenInstance.balanceOf(receiverInstance);
	
	env e;
	int256 amountAdded = harvest(e, balance,_);

	require amountAdded < MIN_INT();
	uint256 strategyBalanceAfter = tokenInstance.balanceOf(currentContract);
	uint256 balanceAfter = tokenInstance.balanceOf(receiverInstance);
	
	if (compareGTzero(amountAdded)) {
		// strategy made profit 
		assert checkAplusBeqC(balanceBefore, amountAdded, balanceAfter), "wrong balance transfered to receiver";
	} else {
		// strategy made loss
		assert balanceBefore == balanceAfter, "balance should not change if profit is negative";
	}
	
}
