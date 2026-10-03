// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: noIncarnations3
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getActionsSetCount() returns(uint256) envfree
	getCurrentState(uint256) returns (uint8)
}

rule noIncarnations3(uint256 actionsSetId)
{
	env e;
	calldataarg args;
	require actionsSetId <= getActionsSetCount();
	require getCurrentState(e, actionsSetId) != 0;
	queue2(e, args);
	assert getCurrentState(e, actionsSetId) != 0;
}
