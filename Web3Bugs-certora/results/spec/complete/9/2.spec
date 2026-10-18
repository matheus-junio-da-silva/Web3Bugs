// Original: contracts/9/specs/accounts.spec:46-48 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	isAccount(address) returns bool	envfree
	_getAuthorizedBy(address) returns address envfree
}

invariant address_cant_be_both_account_and_signer(address x, address d) 
  (x != 0 && d != 0 && x != d && _getAuthorizedBy(d) == x) => 
    (isAccount(x) && !isAccount(d))
