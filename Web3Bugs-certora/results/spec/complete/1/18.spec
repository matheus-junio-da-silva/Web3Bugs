// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: executedValidTransition2
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getCurrentState(uint256) returns (uint8)
	delegatecall(bytes) => NONDET
}

rule executedValidTransition2(uint256 actionsSetId)
{
	env e;
	uint actionsSetId2;
	uint8 state1 = getCurrentState(e, actionsSetId);
		execute(e, actionsSetId2);
	uint8 state2 = getCurrentState(e, actionsSetId);

	assert actionsSetId2 == actionsSetId <=> state1 == 0 && state2 == 1;
}
