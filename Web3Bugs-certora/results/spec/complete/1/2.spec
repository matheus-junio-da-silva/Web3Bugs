// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: queuedChangedCounter
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getActionsSetCount() returns(uint256) envfree
	processMessageFromRoot(uint256, address, bytes)
}

rule queuedChangedCounter()
{
	env e;
	calldataarg args;
	uint256 count1 = getActionsSetCount();
		processMessageFromRoot(e, args);
	uint256 count2 = getActionsSetCount();

	assert count1 < max_uint => count2 == count1+1;
}
