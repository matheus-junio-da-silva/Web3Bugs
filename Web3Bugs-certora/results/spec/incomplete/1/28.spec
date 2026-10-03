// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: queue2Reachability
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
rule queue2Reachability()
{
	env e; calldataarg args;

	queue2(e, args);
	assert false;
}
