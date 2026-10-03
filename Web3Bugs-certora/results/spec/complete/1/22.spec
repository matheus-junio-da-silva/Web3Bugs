// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: processMessageFromRootReachability
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	processMessageFromRoot(uint256, address, bytes)
}

rule processMessageFromRootReachability()
{
	env e; calldataarg args;

	processMessageFromRoot(e, args);
	assert false;
}
