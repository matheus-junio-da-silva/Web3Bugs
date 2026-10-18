// Original: contracts/9/specs/accounts.spec:335-346 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	isStartedSignerAuthorization(address,bytes32,address) returns bool envfree
}

rule cannotStartSignerAuthorizationsForOtherAccounts(method f) filtered { f -> !f.isView } {
	address account;
	bytes32 role;
	address signer;
	require !isStartedSignerAuthorization(account, role, signer);

	env e;
	calldataarg arg;
	f(e,arg);

	assert isStartedSignerAuthorization(account, role, signer) => e.msg.sender == account;
}
