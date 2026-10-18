// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousd.spec lines 348-366; target: OUSDHarness

using OUSDHarness as ousd
using VaultCore as vault

methods {
	// envfree methods
	totalSupply() returns uint256 envfree
	balanceOf(address) returns uint256 envfree
	allowance(address,address) returns uint256 envfree

	rebasingCreditsPerToken() returns uint256 envfree
	nonRebasingCreditsPerToken(address) returns uint256 envfree
	nonRebasingSupply() returns uint256 envfree
	rebasingCredits() returns uint256 envfree

	rebaseState(address) returns uint8 envfree

	// certora harnesses methods
	Certora_maxSupply() returns uint256 envfree
	Certora_isNonRebasingAccount(address) returns bool envfree
}

definition OPT_IN() returns uint8 = 2 ;

definition OPT_OUT() returns uint8 = 1 ;

invariant rebasingCreditsPerTokenMustBeGreaterThan0() 
	rebasingCreditsPerToken() > 0

invariant optingInAndOutSyncdWithNonRebasingState(address a) 
	(rebaseState(a) == OPT_IN() => nonRebasingCreditsPerToken(a) == 0) &&
	(rebaseState(a) == OPT_OUT() => nonRebasingCreditsPerToken(a) > 0) // otherwise - no need to check

rule isRebasingPredicateSynchronized(address a) {
	requireInvariant optingInAndOutSyncdWithNonRebasingState;
	requireInvariant rebasingCreditsPerTokenMustBeGreaterThan0();
	
	uint256 _previousNonRebasingCreditsPerToken = nonRebasingCreditsPerToken(a);
	
	bool becomesNonRebasing = Certora_isNonRebasingAccount(a);
	// the only thing we can say for sure here is that if it was non rebasing, then it remains non rebasing
	if (_previousNonRebasingCreditsPerToken > 0) {
		assert becomesNonRebasing;
	} // can't say anything else because a contract will be migrated.
	
	// after we call _isNonRebasingAccount, and it returns true, it must be the case that nonRebasingCreditsPerToken is positive.
	if (becomesNonRebasing) {
		assert nonRebasingCreditsPerToken(a) > 0;
	} else {
		assert nonRebasingCreditsPerToken(a) == 0;
	}
}
