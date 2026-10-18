// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/compoundStrategy.spec:66-83 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenInstance 

using Receiver as receiverInstance

using Owner as ownerInstance

methods {
	tokenBalanceOf(address token, address account) returns (uint256) envfree
}

rule allTokensAreInvested(uint256 amount, address to, bytes data) {
	env e;

	method f;
	calldataarg args;

	if (f.selector == skim(uint256).selector) {
		require amount == tokenBalanceOf(tokenInstance, currentContract);

		skim(e, amount);
	} else {
		require tokenBalanceOf(tokenInstance, currentContract) == 0;

		f(e, args);
	}

	assert(tokenBalanceOf(tokenInstance, currentContract) == 0, "all not invested");
}
