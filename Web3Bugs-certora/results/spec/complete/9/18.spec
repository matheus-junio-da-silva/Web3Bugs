// Original: contracts/9/specs/accounts.spec:351-368 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	_getAuthorizedBy(address) returns address envfree
}

rule cannotSetAuthorizedByWithoutSignatures(method f) filtered { f -> 
	!f.isView 
		&& f.selector != authorizeSignerWithSignature(address,bytes32,uint8,bytes32,bytes32).selector
		&& f.selector != authorizeAttestationSigner(address,uint8,bytes32,bytes32).selector
		&& f.selector != authorizeValidatorSigner(address,uint8,bytes32,bytes32).selector
		&& f.selector != authorizeValidatorSignerWithKeys(address,uint8,bytes32,bytes32,bytes,bytes,bytes).selector
		&& f.selector != authorizeValidatorSignerWithPublicKey(address,uint8,bytes32,bytes32,bytes).selector
		&& f.selector != authorizeVoteSigner(address,uint8,bytes32,bytes32).selector
} {
	address d;
	require _getAuthorizedBy(d) == 0;

	env e;
	calldataarg arg;
	f(e, arg);

	assert _getAuthorizedBy(d) == 0 || e.msg.sender == d;
} 
