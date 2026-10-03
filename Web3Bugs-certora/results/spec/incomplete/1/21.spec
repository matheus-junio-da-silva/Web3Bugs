// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: holdYourHorses
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getDelay() returns (uint256) envfree 
	getActionsSetCount() returns(uint256) envfree
	delegatecall(bytes) => NONDET
}

rule holdYourHorses()
{
	env e;
	calldataarg args;
	uint256 actionsSetId = getActionsSetCount();
	
	uint256 delay = getDelay();
	queue2(e, args);
	execute@withrevert(e, actionsSetId);
	assert delay > 0 => lastReverted;
}
