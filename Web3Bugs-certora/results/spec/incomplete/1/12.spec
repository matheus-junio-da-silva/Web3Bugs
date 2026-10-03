// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: notCanceledNotExecuted
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getActionsSetCount() returns(uint256) envfree
	getActionsSetExecuted(uint256) returns (bool) envfree
	getActionsSetCanceled(uint256) returns (bool) envfree
}

invariant notCanceledNotExecuted(uint256 id)
	( !getActionsSetCanceled(id) && !getActionsSetExecuted(id) )
	{
		preserved{
			require id == getActionsSetCount();
		}
	}
