// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/compoundStrategy.spec:101-113 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenInstance 

using Receiver as receiverInstance

using Owner as ownerInstance

methods {
	owner() returns (address) envfree
	exited() returns (bool) envfree
}

rule ifExitedIsTrueThenMethodsRevertExceptOwner() {
	env e;

	require exited() == true;
	method f;
	calldataarg args;

	require !f.isView && f.selector != claimOwnership().selector;
	require e.msg.sender != owner();
	f@withrevert(e, args);
	
	assert(lastReverted, "Methods didn't revert");
}
