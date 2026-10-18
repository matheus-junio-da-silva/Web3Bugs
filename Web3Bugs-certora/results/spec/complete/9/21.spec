// Original: contracts/9/specs/accounts.spec:404-431 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	getAttestationSigner(address) returns address envfree
	getVoteSigner(address) returns address envfree
	getValidatorSigner(address) returns address envfree
	getDefaultSigner(address,bytes32) returns address envfree
	getLegacySigner(address,bytes32) returns address envfree
	isLegacyRole(bytes32) returns bool envfree
	_getValidatorRole() returns bytes32 envfree
	_getAttestationRole() returns bytes32 envfree
	_getVoteRole() returns bytes32 envfree
	getIndexedSigner(address,bytes32) returns address envfree
}

rule gettersInAgreement() {
	address account;
	require account != 0;
	bytes32 role;
	address indexedSigner = getIndexedSigner(account, role);
	address defaultSigner = getDefaultSigner(account, role);
	address legacySigner = getLegacySigner(account, role);
	address voteSigner = getVoteSigner(account);
	address validatorSigner = getValidatorSigner(account);
	address attestationSigner = getAttestationSigner(account);

	if (role == _getVoteRole()) {
		assert indexedSigner == legacySigner && indexedSigner == voteSigner, "indexed signer agrees with legacy signer for vote role";
	} else if (role == _getValidatorRole()) {
		assert indexedSigner == legacySigner && indexedSigner == validatorSigner, "indexed signer agrees with legacy signer for validator role";
	} else if (role == _getAttestationRole()) {
		assert indexedSigner == legacySigner && indexedSigner == attestationSigner, "indexed signer agrees with legacy signer for attestation role";
	} else {
		assert indexedSigner == defaultSigner, "for any non legacy role indexed signer is default signer";
	}

	assert indexedSigner != 0 && defaultSigner != 0 && legacySigner != 0 
		&& voteSigner != 0 && validatorSigner != 0 && attestationSigner != 0, "signer is never address 0";

	// original assertion is wrong
	//assert indexedSigner != account => defaultSigner != account, "If indexed signer is a distinct address then default signer for this role is also a distinct address";
	assert !isLegacyRole(role) && indexedSigner != account => defaultSigner != account, "If indexed signer is a distinct address then default signer for this role is also a distinct address";
}
