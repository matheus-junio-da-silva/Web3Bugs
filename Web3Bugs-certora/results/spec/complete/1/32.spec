// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: whoChangesActionsSetState
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getCurrentState(uint256) returns (uint8)
	delegatecall(bytes) => NONDET
}

rule whoChangesActionsSetState(method f, uint actionsSetId)
filtered {f -> !f.isView}
{
	env e;
	calldataarg args;

	uint8 state1 = getCurrentState(e, actionsSetId);
		f(e, args);
	uint8 state2 = getCurrentState(e, actionsSetId);

	assert state1 == state2, "${f} changed the state of an actions set.";
}
