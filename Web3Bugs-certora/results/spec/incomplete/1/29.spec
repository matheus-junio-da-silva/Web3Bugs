// Extracted from: contracts/1/specs/complexity.spec
// Property: sanity
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
rule sanity(method f)
{
	env e;
	calldataarg args;
	f(e,args);
	assert false;
}
