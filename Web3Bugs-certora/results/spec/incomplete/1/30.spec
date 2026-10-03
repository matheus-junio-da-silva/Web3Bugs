// Extracted from: contracts/1/specs/complexity.spec
// Property: noRevert
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
rule noRevert(method f)
description "$f has reverting paths"
{
	env e;
	calldataarg arg;
	require e.msg.value == 0; 
	f@withrevert(e, arg); 
	assert !lastReverted, "${f.selector} can revert";
}
