// Original: contracts/9/specs/accounts.spec:62-65 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	isAccount(address) returns bool	envfree
	_getAuthorizedBy(address) returns address envfree
	_getDefaultSigner(address,bytes32) returns address envfree
}

invariant address_signer_if_authroizedby_new(address x, address d, bytes32 role)
	(x != d && x != 0 && d != 0 &&
		_getDefaultSigner(x,role) == d)
			=> (isAccount(x) && _getAuthorizedBy(d) == x)
