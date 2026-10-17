// Original: contracts/9/specs/accounts.spec:154-162 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	_getAuthorizedBy(address) returns address envfree
}

function callArbitrary(method f) {
	env e;
	calldataarg arg;
	f(e, arg);
}

rule authorizedBy_can_not_be_removed(method f, address signer) filtered { f -> !f.isView } {
	address _account = _getAuthorizedBy(signer); 
	callArbitrary(f);
	address account_ = _getAuthorizedBy(signer); 
	// Whatever transacation occurs, if `_account` was authorized before, it remains authorized.
  	// If `_account` was null, then we could authorize a new account `account_`.
	assert _account == account_ || _account == 0, 
		"Account delegating to $signer cannot change from one non-zero value to another non-zero value";
}
