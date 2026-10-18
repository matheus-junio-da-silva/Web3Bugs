// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousd.spec lines 79-90; target: OUSDHarness

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

function executeAFunction(method f) {
	env e;
	calldataarg arg;
	if (f.selector == init_state().selector) {
		require false; // this is a harness
	} else {
		sinvoke f(e, arg);
	}
}

rule changesRebaseState(method f) {
	address who;
	
	uint8 _rebaseState = rebaseState(who);
	
	executeAFunction(f);
	
	uint8 rebaseState_ = rebaseState(who);
	assert _rebaseState == rebaseState_ 
			|| f.selector == rebaseOptIn().selector 
			|| f.selector == rebaseOptOut().selector;
}
