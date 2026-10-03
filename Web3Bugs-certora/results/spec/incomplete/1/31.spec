// Extracted from: contracts/1/specs/complexity.spec
// Property: alwaysRevert
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
rule alwaysRevert(method f)
description "$f has reverting paths"
{
	env e;
	calldataarg arg;
	f@withrevert(e, arg); 
	assert lastReverted, "${f.selector} succeeds";
}
