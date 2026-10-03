// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: sameExecutionTimesReverts
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getDelay() returns (uint256) envfree 
	queue(address[], uint256[], string[], bytes[], bool[])
}

rule sameExecutionTimesReverts()
{
	env e1; env e2;
	calldataarg args;
	uint256 delay;
	uint256 t1 = e1.block.timestamp;
	uint256 t2 = e2.block.timestamp;

	// Assume different blocks (block2 later than block1)
	require t1 < t2;

	// queue first set.
	queue2(e1, args);
	// Change the delay period.
	uint256 delay1 = getDelay();
		updateDelay(e1, delay);
	uint256 delay2 = getDelay();
	// Try to queue second set, with same arguments.
	queue2@withrevert(e2, args);

	assert t1 + delay1 == t2 + delay2 => lastReverted;
}
