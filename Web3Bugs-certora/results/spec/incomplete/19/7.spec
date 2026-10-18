// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousd.spec lines 66-77; target: OUSDHarness

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

function executeAFunctionWithSpecificSender(address x, method f) {
	env e;
	require e.msg.sender == x;
	calldataarg arg;
	if (f.selector == init_state().selector) {
		require false; // this is a harness
	} else {
		sinvoke f(e, arg);
	}
}

rule senderCannotDecreaseOthersBalance(address executor, address who, method f) {
	require executor != who;
	// no approval from who to executor
	require allowance(who, executor) == 0;
	
	uint256 previous = balanceOf(who);
	
	executeAFunctionWithSpecificSender(executor, f);
	
	uint256 current = balanceOf(who);
	assert current >= previous;
}	
