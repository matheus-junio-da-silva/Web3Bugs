// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousd.spec lines 344-346; target: OUSDHarness

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

invariant optingInAndOutSyncdWithNonRebasingState(address a) 
	(rebaseState(a) == OPT_IN() => nonRebasingCreditsPerToken(a) == 0) &&
	(rebaseState(a) == OPT_OUT() => nonRebasingCreditsPerToken(a) > 0) // otherwise - no need to check
