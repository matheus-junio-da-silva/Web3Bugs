// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: holdYourHorses
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getDelay() returns (uint256) envfree 
	getActionsSetCount() returns(uint256) envfree
	processMessageFromRoot(uint256, address, bytes)
	delegatecall(bytes) => NONDET
}

rule holdYourHorses()
{
	env e;
	calldataarg args;
	uint256 actionsSetId = getActionsSetCount();
	
	uint256 delay = getDelay();
	processMessageFromRoot(e, args);
	execute@withrevert(e, actionsSetId);
	assert delay > 0 => lastReverted;
}
