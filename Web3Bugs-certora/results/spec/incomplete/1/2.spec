// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: actionNotCanceledAndExecuted
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getActionsSetExecuted(uint256) returns (bool) envfree
	getActionsSetCanceled(uint256) returns (bool) envfree
}

invariant actionNotCanceledAndExecuted(uint256 setID)
	! (getActionsSetCanceled(setID) && getActionsSetExecuted(setID))
