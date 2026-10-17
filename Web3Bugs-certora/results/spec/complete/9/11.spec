// Original: contracts/9/specs/accounts.spec:203-258 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	isAccount(address) returns bool	envfree
	isSigner(address,address,bytes32) returns bool envfree // account, signer, role
	_getAuthorizedBy(address) returns address envfree
	getLegacySigner(address,bytes32) returns address envfree
	isLegacyRole(bytes32) returns bool envfree
	voteSignerToAccount(address) returns address envfree
	validatorSignerToAccount(address) returns address envfree
	attestationSignerToAccount(address) returns address envfree
	signerToAccount(address) returns address envfree
	_getValidatorRole() returns bytes32 envfree
	_getAttestationRole() returns bytes32 envfree
	_getVoteRole() returns bytes32 envfree
}

invariant authorizedByIsNeverReflexive(address a)
	a != 0 => _getAuthorizedBy(a) != a



rule viewFunctionsDoNotRevert(method f) filtered { f -> 
	f.isView 
	// some functions we ignore, and the reasons:
	&& f.selector != hasAuthorizedSigner(address,string).selector // Calldatasize may not match
	&& f.selector != batchGetMetadataURL(address[]).selector // Calldatasize may not match

  // These require an account to exist
	&& f.selector != getOffchainStorageRoots(address).selector
	&& f.selector != offchainStorageRoots(address,uint256).selector
} {
	env e;
	require e.msg.value == 0; // view functions are not payable
	
	// functions that require special handling:
	if (f.selector == getLegacySigner(address,bytes32).selector) {
		// getLegacySigner requires getting a legacy role
		address a;
		bytes32 r;
		require isLegacyRole(r);
		getLegacySigner@withrevert(a, r);
	} else if (f.selector == hasLegacySigner(address,bytes32).selector) {
		// hasLegacySigner requires getting a legacy role
		address a;
		bytes32 r;
		require isLegacyRole(r);
		hasLegacySigner@withrevert(e, a, r);
	} else if (f.selector == signerToAccount(address).selector) {
		// will fail if address is not authorized by anyone, and is not an account.
		address a;
		require _getAuthorizedBy(a) != 0 || isAccount(a);
		signerToAccount@withrevert(a);
	} else if (f.selector == voteSignerToAccount(address).selector) {
		address a;
		address authBy = _getAuthorizedBy(a);
		requireInvariant authorizedByIsNeverReflexive(a);
		require (authBy != 0 && isSigner(authBy, a, _getVoteRole())) || (authBy == 0 && isAccount(a));
		voteSignerToAccount@withrevert(a);
	} else if (f.selector == validatorSignerToAccount(address).selector) {
		address a;
		address authBy = _getAuthorizedBy(a);
		requireInvariant authorizedByIsNeverReflexive(a);
		require (authBy != 0 && isSigner(authBy, a, _getValidatorRole())) || (authBy == 0 && isAccount(a));
		validatorSignerToAccount@withrevert(a);
	} else if (f.selector == attestationSignerToAccount(address).selector) {
		address a;
		address authBy = _getAuthorizedBy(a);
		requireInvariant authorizedByIsNeverReflexive(a);
		require (authBy != 0 && isSigner(authBy, a, _getAttestationRole())) || (authBy == 0 && isAccount(a));
		attestationSignerToAccount@withrevert(a);
	} else {
		calldataarg arg;
		f@withrevert(e, arg);
	}

	assert !lastReverted, "View functions should not revert";
}
