// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: cancelPriviliged
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
rule cancelPriviliged()
{
	env e1;
	env e2;
	calldataarg args1;
	calldataarg args2;
	cancel(e1, args1);
	cancel@withrevert(e2, args2);
	assert e1.msg.sender != e2.msg.sender => lastReverted;
}
