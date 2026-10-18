// Original: contracts/9/specs/accounts.spec:96-120 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	isAccount(address) returns bool	envfree
	_getAuthorizedBy(address) returns address envfree
}

rule address_can_authorize_two_addresses_legacy(address x, address d1, address d2)
{ 
	require x != 0 && d1 != 0 && d2 != 0 && x != d1 && x != d2 && d1 != d2 && isAccount(x); 
	env e;
	require e.msg.sender == x;
  	
	storage init = lastStorage;
	// first, authorizing d2 as a validation signer should succeed
	uint8 v2;
	bytes32 r2;
	bytes32 s2;
	authorizeValidatorSigner(e, d2, v2, r2, s2);  

	// Authorize d1 as a Vote signer (alternative execution path - start from the state where validator authorization started)
	uint8 v1;
	bytes32 r1;
	bytes32 s1;
	authorizeVoteSigner(e, d1, v1, r1, s1) at init;
	
	// Even after authorizing d1, the authorization of d2 as a Validation signer should succeed
	authorizeValidatorSigner(e, d2, v2, r2, s2);  
		
	// AuthorizedBy(d1) and AuthorizedBy(d2) should still be x
	assert _getAuthorizedBy(d1) == x && _getAuthorizedBy(d2) == x, "Authorizedby should both be x";
}
