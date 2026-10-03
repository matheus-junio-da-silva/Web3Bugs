// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: expiredForever
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getGracePeriod() returns (uint256) envfree
	getCurrentState(uint256) returns (uint8)
	delegatecall(bytes) => NONDET
}

rule expiredForever(method f, uint256 actionsSetId)
{
	env e; env e2;
	calldataarg args;
	require getCurrentState(e, actionsSetId) == 3;
	require e.block.timestamp <= e2.block.timestamp;
	 
	if (f.selector == updateGracePeriod(uint256).selector) {
		uint256 oldPeriod = getGracePeriod();
		updateGracePeriod(e, args);
		uint256 newPeriod = getGracePeriod();
		assert newPeriod <= oldPeriod =>
		getCurrentState(e2, actionsSetId) == 3;
	}
	else {
		f(e, args);
		assert getCurrentState(e2, actionsSetId) == 3;
	}	
}
