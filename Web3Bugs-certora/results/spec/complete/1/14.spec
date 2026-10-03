// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: cancelExclusive
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getCurrentState(uint256) returns (uint8)
}

rule cancelExclusive(uint actionsSetId1, uint actionsSetId2)
{
	env e;
	uint8 stateBefore = getCurrentState(e, actionsSetId2);
		cancel(e, actionsSetId1);
	uint8 stateAfter = getCurrentState(e, actionsSetId2);

	assert actionsSetId1 != actionsSetId2 => stateBefore == stateAfter;
}
