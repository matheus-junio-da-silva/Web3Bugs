// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: queuedStateConsistency
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getActionsSetCount() returns(uint256) envfree
	getCurrentState(uint256) returns (uint8)
	getActionsSetExecuted(uint256) returns (bool) envfree
	getActionsSetCanceled(uint256) returns (bool) envfree
	processMessageFromRoot(uint256, address, bytes)
}

invariant notCanceledNotExecuted(uint256 id)
	( !getActionsSetCanceled(id) && !getActionsSetExecuted(id) )
	{
		preserved{
			require id == getActionsSetCount();
		}
	}

rule queuedStateConsistency()
{
	env e;
	calldataarg args;
	uint256 id = getActionsSetCount();
	requireInvariant notCanceledNotExecuted(id);
	processMessageFromRoot(e, args);
	assert getCurrentState(e, id) == 0;
}
