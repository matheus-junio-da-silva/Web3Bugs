// Original: contracts/9/specs/accounts.spec:309-330 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	isLegacyRole(bytes32) returns bool envfree
	isCompletedSignerAuthorization(address,bytes32,address) returns bool envfree
}

rule cantMakeASignerForNonLegacyRoleWithoutApprovalOfSigner(method f) filtered { f -> 
	!f.isView 
		// the authorizeSignerWithSignature allows the signer to provide a signature to the account, so we exclude this option
		&& f.selector != authorizeSignerWithSignature(address,bytes32,uint8,bytes32,bytes32).selector	
} {
	address account;
	bytes32 role;
	
	// Leagcy roles can be updated using a signature
	require !isLegacyRole(role);

	address signer;

	// not completed signer auth yet (but may have started)
	require !isCompletedSignerAuthorization(account, role, signer);

	env e;
	calldataarg arg;
	f(e, arg);

	assert isCompletedSignerAuthorization(account, role, signer) => e.msg.sender == signer;
}
