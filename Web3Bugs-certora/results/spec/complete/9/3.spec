// Original: contracts/9/specs/accounts.spec:54-57 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	isAccount(address) returns bool	envfree
	_getAuthorizedBy(address) returns address envfree
	_getAttestationSigner(address) returns address envfree
	_getVoteSigner(address) returns address envfree
	_getValidatorSigner(address) returns address envfree
}

invariant address_signer_if_authorizedby_legacy(address x, address d) 
  (x != d && x != 0 && d != 0 &&
  	(_getAttestationSigner(x) == d || _getVoteSigner(x) == d || _getValidatorSigner(x) == d))
    	=> (isAccount(x) && _getAuthorizedBy(d) == x)
