// Original: contracts/9/specs/accounts.spec:276-285 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	isCompletedSignerAuthorization(address,bytes32,address) returns bool envfree
}

invariant mustHaveAuthorizedByIfCompletedSignerAuthorization(address account, bytes32 role, address signer) 
	account != 0 => (isCompletedSignerAuthorization(account, role, signer) => _getAuthorizedBy(signer) == account)

invariant mustHaveAuthorizedByIfCompletedSignerAuthorization(address account, bytes32 role, address signer) 
	account != 0 => (isCompletedSignerAuthorization(account, role, signer) => _getAuthorizedBy(signer) == account)

invariant noMultipleAccountsPerSignerInARole(address account, address account2, bytes32 role, bytes32 role2, address signer)
	account != 0 && account2 != 0
		=> (isCompletedSignerAuthorization(account, role, signer) && isCompletedSignerAuthorization(account2, role2, signer) 
			=> account == account2) {
	
	preserved {
		requireInvariant mustHaveAuthorizedByIfCompletedSignerAuthorization(account, role, signer);
		requireInvariant mustHaveAuthorizedByIfCompletedSignerAuthorization(account2, role2, signer);
	}
}
