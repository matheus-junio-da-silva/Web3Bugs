// Original: contracts/9/specs/accounts.spec:181-191 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	isAccount(address) returns bool	envfree
}

function callArbitrary(method f) {
	env e;
	calldataarg arg;
	f(e, arg);
}

rule createsAccount(method f, address a) filtered { f ->
	!f.isView
		&& f.selector != createAccount().selector
		&& f.selector != setAccount(string,bytes,address,uint8,bytes32,bytes32).selector
} {
	bool _isAccount = isAccount(a);
	callArbitrary(f);
	bool isAccount_ = isAccount(a);

	assert _isAccount == isAccount_, "checked function creates an account";
}
