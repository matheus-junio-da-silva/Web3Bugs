// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/sanity.spec lines 1-6; target: OUSD

rule sanity(method f) {
	env e;
	calldataarg arg;
	sinvoke f(e, arg);
	assert false;
}
