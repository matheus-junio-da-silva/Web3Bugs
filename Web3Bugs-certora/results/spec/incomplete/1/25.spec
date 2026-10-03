// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: afterQueueHashQueued
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getActionsSetCount() returns(uint256) envfree
	ID2actionHash(uint256, uint256) returns (bytes32) envfree
}

rule afterQueueHashQueued(bytes32 actionHash)
{
	env e;
	calldataarg args;
	uint256 actionsSetId = getActionsSetCount();

	bool queueBefore = isActionQueued(e, actionHash);
		queue2(e, args);
	bool queuedAfter = isActionQueued(e, actionHash);
		
	assert (actionHash == ID2actionHash(actionsSetId, 0) ||
			actionHash == ID2actionHash(actionsSetId, 1))
			<=> !queueBefore && queuedAfter;
}
