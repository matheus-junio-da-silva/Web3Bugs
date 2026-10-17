// Historical CVL property, Project 10, contracts/10/specs/libParam.spec:6-19
// Only available dependency declarations; no historic signature edits and no CVL migration.

methods {
	isStatic(bytes32) returns (bool) envfree
	getNumOfReferences(bytes32) returns (uint256) envfree
}
}

rule noThrow(method f) {
	env e;
	require e.msg.value == 0;
	calldataarg arg;
	if (f.selector == getParams(bytes32).selector) {
		bytes32 x;
		require !isStatic(x);
		require getNumOfReferences(x) > 0;
		getParams@withrevert(e, x);
	} else {
		f@withrevert(e, arg);
	}
	assert !lastHasThrown;
}
