// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/compoundStrategy.spec:152-164 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenInstance 

using Receiver as receiverInstance

using Owner as ownerInstance

methods {
	receiver() returns (address) envfree
	tokenBalanceOf(address token, address account) returns (uint256) envfree
	checkAplusBeqC(uint256 a, int256 b, uint256 c) returns (bool) envfree
}

definition MAX_UNSIGNED_INT() returns uint256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

rule integrityExit(uint256 balance) {
	require receiver() == receiverInstance;
	env e;
	uint256 balanceBefore = tokenBalanceOf(tokenInstance,receiverInstance);
		
	int256 amountAdded = exit(e, balance);
	
	uint256 balanceAfter = tokenBalanceOf(tokenInstance,receiverInstance);

	mathint t = balanceBefore + balance;
	require t <= MAX_UNSIGNED_INT();
	uint256 expectedBalance = balanceBefore + balance;
	assert checkAplusBeqC(expectedBalance, amountAdded, balanceAfter), "wrong balance transfered to receiver";
}
