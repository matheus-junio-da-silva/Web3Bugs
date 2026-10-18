// Original: contracts/9/specs/accounts.spec:373-388 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	isCompletedSignerAuthorization(address,bytes32,address) returns bool envfree
	isStartedSignerAuthorization(address,bytes32,address) returns bool envfree
}

rule signerAuthorizationChangePrivileges(address a, bytes32 r, address s, method f) filtered { f ->
	!f.isView 
} {
	bool _started = isStartedSignerAuthorization(a, r, s);
	bool _completed = isCompletedSignerAuthorization(a, r, s);

	env e;
	calldataarg arg;
	f(e, arg);

	bool started_ = isStartedSignerAuthorization(a, r, s);
	bool completed_ = isCompletedSignerAuthorization(a, r, s);
	assert _started != started_ => e.msg.sender == a, "Only account can start a signer authorization";
	assert _completed && !completed_ => e.msg.sender == a, "Only account can remove a signer authorization";
	assert !_completed && completed_ => e.msg.sender == a || e.msg.sender == s, "Only signer or account can complete a signer authorization";
} 
