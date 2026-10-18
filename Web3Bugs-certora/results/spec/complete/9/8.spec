// Original: contracts/9/specs/accounts.spec:167-176 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

rule initializableOnlyOnce {
	env e;
	calldataarg arg;
	initialize(e, arg);

	env e2;
	calldataarg arg2;
	initialize@withrevert(e2, arg2);
	assert lastReverted;
}
