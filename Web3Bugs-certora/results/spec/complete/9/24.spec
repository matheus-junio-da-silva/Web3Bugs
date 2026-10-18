// Original: contracts/9/specs/accounts.spec:452-458 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	getAttestationSigner(address) returns address envfree
	attestationSignerToAccount(address) returns address envfree
	_getAttestationRole() returns bytes32 envfree
}

invariant accountToSignerAndInverseAttestation(address a, address s, bytes32 r)
	r == _getAttestationRole() => (s == getAttestationSigner(a) => attestationSignerToAccount(s) == a)
{
		preserved {
			require a != s;
		}
}
