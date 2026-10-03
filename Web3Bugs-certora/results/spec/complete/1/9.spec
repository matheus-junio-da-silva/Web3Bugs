// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: noIncarnations2
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getCurrentState(uint256) returns (uint8)
	delegatecall(bytes) => NONDET
}

rule noIncarnations2(uint256 actionsSetId)
{
	env e;
	execute(e, actionsSetId);
	assert getCurrentState(e, actionsSetId) != 0;
}
