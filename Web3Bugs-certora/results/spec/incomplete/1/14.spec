// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: queueCannotCancel
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getCurrentState(uint256) returns (uint8)
}

rule queueCannotCancel()
{
	env e;
	calldataarg args;
	uint256 actionsSetId;

	require getCurrentState(e, actionsSetId) != 2;
		queue2(e, args);
	assert getCurrentState(e, actionsSetId) != 2;
}
