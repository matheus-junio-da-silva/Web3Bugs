// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: minDelayLtMaxDelay
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getMinimumDelay() returns (uint256) envfree
	getMaximumDelay() returns (uint256) envfree
}

invariant minDelayLtMaxDelay()
	getMinimumDelay() <= getMaximumDelay()
