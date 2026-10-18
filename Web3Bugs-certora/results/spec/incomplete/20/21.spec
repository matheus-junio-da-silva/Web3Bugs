// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/compoundStrategy.spec:136-149 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenInstance 

using Receiver as receiverInstance

using Owner as ownerInstance

methods {
	receiver() returns (address) envfree
	tokenBalanceOf(address token, address account) returns (uint256) envfree
}

definition MAX_UNSIGNED_INT() returns uint256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

rule integrityWithdraw(uint256 amount, uint256 balance) {
	require receiver() == receiverInstance;
	env e;
	uint256 balanceBefore = tokenBalanceOf(tokenInstance,receiverInstance);
		
	uint256 amountAdded = withdraw(e, amount);
	
	uint256 balanceAfter = tokenBalanceOf(tokenInstance,receiverInstance);

	mathint t = balanceBefore + amountAdded;
	require t <= MAX_UNSIGNED_INT();
	
	assert balanceAfter == balanceBefore + amountAdded, "wrong balance transfered to receiver";
}
