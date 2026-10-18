// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/compoundStrategy.spec:87-98 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenInstance 

using Receiver as receiverInstance

using Owner as ownerInstance

methods {
	exited() returns (bool) envfree
}

rule onceExitedIsTrueThenItIsNeverFalse() {
	env e;

	require exited() == true;

	method f;
	calldataarg args;

	f(e, args);

	assert(exited() == true, "exited became false");
}
