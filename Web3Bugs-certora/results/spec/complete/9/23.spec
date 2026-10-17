// Original: contracts/9/specs/accounts.spec:444-450 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	getValidatorSigner(address) returns address envfree
	validatorSignerToAccount(address) returns address envfree
	_getValidatorRole() returns bytes32 envfree
}

invariant accountToSignerAndInverseValidator(address a, address s, bytes32 r)	
	r == _getValidatorRole() => (s == getValidatorSigner(a) => validatorSignerToAccount(s) == a)
{
		preserved {
			require a != s;
		}
}
