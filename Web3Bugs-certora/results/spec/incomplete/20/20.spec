// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/compoundStrategy.spec:116-133 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenInstance 

using Receiver as receiverInstance

using Owner as ownerInstance

methods {
	receiver() returns (address) envfree
	tokenBalanceOf(address token, address account) returns (uint256) envfree
	compareGTzero(int256 x) returns (bool) envfree
	checkAplusBeqC(uint256 a, int256 b, uint256 c) returns (bool) envfree
}

definition MIN_INT() returns int256 = 0x8000000000000000000000000000000000000000000000000000000000000000;

rule integrityHarvest(uint256 balance, uint256 strategyBalanceBefore) {
	require receiver() == receiverInstance;
	env e;
	uint256 balanceBefore = tokenBalanceOf(tokenInstance, receiverInstance);
		
	int256 amountAdded = harvest(e, balance,_);

	require amountAdded < MIN_INT();
	uint256 balanceAfter = tokenBalanceOf(tokenInstance, receiverInstance);
	
	if (compareGTzero(amountAdded)) {
		// strategy made profit 
		assert checkAplusBeqC(balanceBefore, amountAdded, balanceAfter), "wrong balance transfered to receiver";
	} else {
		// strategy made loss
		assert balanceBefore == balanceAfter, "balance should not change if profit is negative";
	}
}
