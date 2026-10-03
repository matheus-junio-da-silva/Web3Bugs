// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: executeCannotCancel
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getGuardian() returns(address) envfree
	getCurrentState(uint256) returns (uint8)
	delegatecall(bytes) => NONDET
}

rule executeCannotCancel()
{
	env e;
	calldataarg args;
	uint256 calledSet;
	uint256 canceledSet;

	require getCurrentState(e, canceledSet) != 2;
	require getGuardian() != _mock(e);
	
	execute(e, calledSet);

	assert getCurrentState(e, canceledSet) != 2;
}
