// Original: contracts/9/specs/accounts.spec:196-197 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	_getDefaultSigner(address,bytes32) returns address envfree
	isLegacyRole(bytes32) returns bool envfree
}

invariant legacyRolesAreNotUsedInNewRoles(address account, bytes32 role) 
	isLegacyRole(role) => _getDefaultSigner(account, role) == 0
