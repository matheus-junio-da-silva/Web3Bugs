// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousd.spec lines 33-39; target: OUSDHarness

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

invariant rebasingCreditsPerTokenMustBeGreaterThan0() 
	rebasingCreditsPerToken() > 0

rule neverRevert_BalanceOf {
	// probably must assume invariant rebasingCreditsPerTokenMustBeGreaterThan0
	requireInvariant rebasingCreditsPerTokenMustBeGreaterThan0();
	address who;
	invoke balanceOf(who);
	assert !lastReverted;
}
