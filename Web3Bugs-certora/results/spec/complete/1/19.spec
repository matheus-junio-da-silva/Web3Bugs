// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: executeFailsIfExpired
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getCurrentState(uint256) returns (uint8)
	delegatecall(bytes) => NONDET
}

rule executeFailsIfExpired(uint256 actionsSetId)
{
	env e;
	uint8 stateBefore = getCurrentState(e, actionsSetId);
	execute@withrevert(e, actionsSetId);
	bool executeReverted = lastReverted;
	assert stateBefore == 3 => executeReverted;
}
