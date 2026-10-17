// Historical CVL property, Project 10, contracts/10/specs/libParam.spec:21-31
// Only available dependency declarations; no historic signature edits and no CVL migration.

rule noRevert(method f) {
	env e;
	require e.msg.value == 0;
	calldataarg arg;
	if (f.selector == getParams(bytes32).selector) {
		require false;
	} else {
		f@withrevert(e, arg);
	}
	assert !lastReverted; // only fallback may revert
}
