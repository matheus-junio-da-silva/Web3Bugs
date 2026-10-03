// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: executedValidTransition1
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getCurrentState(uint256) returns (uint8)
	delegatecall(bytes) => NONDET
}

rule executedValidTransition1(method f, uint256 actionsSetId)
filtered{f -> !f.isView}
{
	env e;
	calldataarg args;
	uint8 state1 = getCurrentState(e, actionsSetId);
		f(e, args);
	uint8 state2 = getCurrentState(e, actionsSetId);

	assert f.selector != execute(uint256).selector =>
	! (state1 == 0 && state2 == 1);
}
