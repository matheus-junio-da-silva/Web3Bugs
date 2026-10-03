// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: onlyQueuedAreExecuted
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getGuardian() returns(address) envfree
	ID2actionHash(uint256, uint256) returns (bytes32) envfree
	delegatecall(bytes) => NONDET
}

rule onlyQueuedAreExecuted(bytes32 actionHash, uint256 actionsSetId)
{
	env e2; env e;
	calldataarg args;

	require isActionQueued(e, actionHash);
	// This is true in general, guardian is not a contract (is EOA).
	require getGuardian() != _mock(e);
		execute(e2, actionsSetId);
	bool queuedAfter = isActionQueued(e2, actionHash);
	
	assert (actionHash == ID2actionHash(actionsSetId, 0) ||
			actionHash == ID2actionHash(actionsSetId, 1)) 
			<=> !queuedAfter;
}
