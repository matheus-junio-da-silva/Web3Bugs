// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: noIncarnations1
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getActionsSetCount() returns(uint256) envfree
	getCurrentState(uint256) returns (uint8)
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

rule noIncarnations1()
{
	env e;
	calldataarg args;
	uint256 actionsSetId = getActionsSetCount();
	require actionsSetId < max_uint;
	requireInvariant notCanceledNotExecuted(actionsSetId);
	queue2(e, args);
	assert getCurrentState(e, actionsSetId) == 0
	&& actionsSetId < getActionsSetCount();
}
