// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: queueCannotCancel
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getCurrentState(uint256) returns (uint8)
	processMessageFromRoot(uint256, address, bytes)
}

rule queueCannotCancel()
{
	env e;
	calldataarg args;
	uint256 actionsSetId;

	require getCurrentState(e, actionsSetId) != 2;
		processMessageFromRoot(e, args);
	assert getCurrentState(e, actionsSetId) != 2;
}
