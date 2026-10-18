// Original: contracts/9/specs/accounts.spec:460-466 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	signerToAccount(address) returns address envfree
	getIndexedSigner(address,bytes32) returns address envfree
}

invariant accountToSignerAndInverseNewRoles(address a, address s, bytes32 r)	
	getIndexedSigner(a, r) == s => signerToAccount(s) == a 
{
		preserved {
			require a != s;
		}
}
