// Historical CVL property, Project 10, contracts/10/specs/sanity.spec:1-6
// Only available dependency declarations; no historic signature edits and no CVL migration.

rule sanity(method f) {
	env e;
	calldataarg arg;
	sinvoke f(e, arg);
	assert false;
}
