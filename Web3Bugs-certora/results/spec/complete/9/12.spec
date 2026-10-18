// Original: contracts/9/specs/accounts.spec:263-264 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	_getAuthorizedBy(address) returns address envfree
}

invariant authorizedByIsNeverReflexive(address a)
	a != 0 => _getAuthorizedBy(a) != a
