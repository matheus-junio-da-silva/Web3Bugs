// Original: contracts/9/specs/accounts.spec:35-40 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	isAccount(address) returns bool	envfree
	getWalletAddress(address) returns address envfree
	_getAttestationSigner(address) returns address envfree
	_getVoteSigner(address) returns address envfree
	_getValidatorSigner(address) returns address envfree
}

invariant account_empty_if_not_exist(env e, address x) 
  !isAccount(x) => 
    getWalletAddress(x) == 0 &&
    _getAttestationSigner(x) == 0 &&
    _getVoteSigner(x) == 0 &&
    _getValidatorSigner(x) == 0
