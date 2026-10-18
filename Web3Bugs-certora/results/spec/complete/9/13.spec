// Original: contracts/9/specs/accounts.spec:270-271 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	_getAuthorizedBy(address) returns address envfree
	isCompletedSignerAuthorization(address,bytes32,address) returns bool envfree
}

invariant mustHaveAuthorizedByIfCompletedSignerAuthorization(address account, bytes32 role, address signer) 
	account != 0 => (isCompletedSignerAuthorization(account, role, signer) => _getAuthorizedBy(signer) == account)
