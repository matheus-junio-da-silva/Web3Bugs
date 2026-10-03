// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: properDelay
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getDelay() returns (uint256) envfree 
	getMinimumDelay() returns (uint256) envfree
	getMaximumDelay() returns (uint256) envfree
}

invariant properDelay()
	getMinimumDelay() <= getDelay() && getDelay() <= getMaximumDelay()
