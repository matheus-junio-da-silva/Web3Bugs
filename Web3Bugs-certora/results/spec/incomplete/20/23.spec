// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/compoundStrategyAdditional.spec:62-70 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenInstance 

using Receiver as receiverInstance

using Owner as ownerInstance

methods {
	receiver() returns (address) envfree
	tokenBalanceOf(address token, address account) returns (uint256) envfree
	exited() returns (bool) envfree
}

rule exitRevert(uint256 balance) {
	env e;
	require (e.msg.value == 0 && e.msg.sender == receiver() && !exited());
	require (tokenBalanceOf(tokenInstance,receiverInstance) + tokenBalanceOf(tokenInstance,currentContract) <= MAX_INT());
	exit@withrevert(e, balance);

	bool succ = !lastReverted;
	assert(succ, "exitReverted");
}
