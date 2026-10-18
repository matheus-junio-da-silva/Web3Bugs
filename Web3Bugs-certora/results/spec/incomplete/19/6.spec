// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousd.spec lines 54-62; target: OUSDHarness

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

definition ONE() returns uint = 1000000000000000000 ; // 1e18

invariant rebasingCreditsPerTokenMustBeGreaterThan0() 
	rebasingCreditsPerToken() > 0

function executeAFunction(method f) {
	env e;
	calldataarg arg;
	if (f.selector == init_state().selector) {
		require false; // this is a harness
	} else {
		sinvoke f(e, arg);
	}
}

rule totalSupplyIntegrity(method f) {
	require totalSupply() >= (rebasingCredits()*ONE()) / rebasingCreditsPerToken() + nonRebasingSupply();
	requireInvariant rebasingCreditsPerTokenMustBeGreaterThan0;
	// need to require that nonRebasingCreditsPerToken is < 1e18?

    executeAFunction(f);

    assert totalSupply() >= (rebasingCredits()*ONE()) / rebasingCreditsPerToken() + nonRebasingSupply();
}
