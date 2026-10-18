// Original: contracts/9/specs/accounts.spec:393-399 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

rule check_no_fallback {
	env e;
	calldataarg arg;
	invoke_fallback(e, arg);

	assert lastReverted;
}
