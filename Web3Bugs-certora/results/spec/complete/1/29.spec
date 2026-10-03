// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: canceledForever
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getCurrentState(uint256) returns (uint8)
	delegatecall(bytes) => NONDET
}

rule canceledForever(method f, uint256 actionsSetId)
{
	env e; env e2;
	calldataarg args;
	require getCurrentState(e, actionsSetId) == 2;
		f(e, args);
	assert getCurrentState(e2, actionsSetId) == 2;
}
