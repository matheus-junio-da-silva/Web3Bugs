// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: onlyCancelCanCancel
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getGuardian() returns(address) envfree
	getCurrentState(uint256) returns (uint8)
	delegatecall(bytes) => NONDET
}

rule onlyCancelCanCancel(method f, uint actionsSetId)
{
	env e;
	calldataarg args;
	require getGuardian() != _mock(e);
	// Replace by !=2
	require getCurrentState(e, actionsSetId) != 2;

		f(e, args);

	assert getCurrentState(e, actionsSetId) == 2
			=> f.selector == cancel(uint256).selector;
}
