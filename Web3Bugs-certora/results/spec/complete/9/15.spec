// Original: contracts/9/specs/accounts.spec:290-303 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	isLegacyRole(bytes32) returns bool envfree
	isCompletedSignerAuthorization(address,bytes32,address) returns bool envfree
	isStartedSignerAuthorization(address,bytes32,address) returns bool envfree
}

function callArbitrary(method f) {
	env e;
	calldataarg arg;
	f(e, arg);
}

rule cantGoFromNoAuthorizationToCompletedInOneStepUnlessRoleIsLegacy(method f) filtered { f -> 
	!f.isView 
		// the authorizeSignerWithSignature allows the signer to provide a signature to the account, so we exclude this option
		&& f.selector != authorizeSignerWithSignature(address,bytes32,uint8,bytes32,bytes32).selector
} {
	address account;
	bytes32 role;
	address signer;
	require !isStartedSignerAuthorization(account, role, signer) && !isCompletedSignerAuthorization(account, role, signer);

	callArbitrary(f);

	assert isCompletedSignerAuthorization(account, role, signer) => isLegacyRole(role);
}
