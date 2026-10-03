// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: actionDuplicate
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
rule actionDuplicate()
{
	env e; 
	calldataarg args;

	queue2(e, args);
	queue2@withrevert(e, args);
	assert lastReverted;
}
