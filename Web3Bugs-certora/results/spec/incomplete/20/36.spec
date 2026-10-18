// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/strategy.spec:69-86 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenInstance 

using Receiver as receiverInstance

methods {
	receiver() returns (address) envfree
	tokenInstance.balanceOf(address account) returns (uint256) envfree
}

definition MAX_UNSIGNED_INT() returns uint256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

rule integrityWithdraw(uint256 amount, uint256 balance) {
	require receiver() == receiverInstance;
	
	uint256 strategyBalanceBefore = tokenInstance.balanceOf(currentContract);
	uint256 balanceBefore = tokenInstance.balanceOf(receiverInstance);
	
	env e;
	uint256 amountAdded = withdraw(e, amount);
	
	uint256 strategyBalanceAfter = tokenInstance.balanceOf(currentContract);
	uint256 balanceAfter = tokenInstance.balanceOf(receiverInstance);

	mathint t = balanceBefore + amountAdded;
	require t <= MAX_UNSIGNED_INT();
	
	assert strategyBalanceAfter == strategyBalanceBefore - amountAdded, "strategy balance is not correct";
	assert balanceAfter == balanceBefore + amountAdded, "wrong balance transfered to receiver";
}
