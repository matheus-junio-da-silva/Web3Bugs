// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: queueDoesntModifyStateVariables
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getDelay() returns (uint256) envfree 
	getGracePeriod() returns (uint256) envfree
	getMinimumDelay() returns (uint256) envfree
	getMaximumDelay() returns (uint256) envfree
	getGuardian() returns(address) envfree
	queue(address[], uint256[], string[], bytes[], bool[])
}

rule queueDoesntModifyStateVariables()
{
	env e;
	calldataarg args;
	// State variables before
	uint256 delay1 = getDelay();
	uint256 period1 = getGracePeriod();
	uint256 minDelay1 = getMinimumDelay();
	uint256 maxDelay1 = getMaximumDelay();
	address guardian1 = getGuardian();

	// Call queue with one action in the set.
	queue2(e, args);

	// State variables after
	uint256 delay2 = getDelay();
	uint256 period2 = getGracePeriod();
	uint256 minDelay2 = getMinimumDelay();
	uint256 maxDelay2 = getMaximumDelay();
	address guardian2 = getGuardian();

	bool stateIntact =  delay1 == delay2 &&
		 period1 == period2 &&
		 minDelay1 == minDelay2 &&
		 maxDelay1 == maxDelay2 &&
		 guardian1 == guardian2;

	assert stateIntact,
		"_queue changed state variables unexpectedly";
}
