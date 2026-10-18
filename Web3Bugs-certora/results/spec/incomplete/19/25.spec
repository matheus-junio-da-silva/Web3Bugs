// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousd.spec lines 368-377; target: OUSDHarness

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

function executeAFunction(method f) {
	env e;
	calldataarg arg;
	if (f.selector == init_state().selector) {
		require false; // this is a harness
	} else {
		sinvoke f(e, arg);
	}
}

rule onceRebaseStateWasSelectedCannotUnsetIt(address a, method f) {
	uint8 _rebaseState = rebaseState(a);
	bool _isSet = _rebaseState == OPT_IN() || _rebaseState == OPT_OUT();
	
	executeAFunction(f);
	
	uint8 rebaseState_ = rebaseState(a);
	bool isSet_ = rebaseState_ == OPT_IN() || rebaseState_ == OPT_OUT();
	assert _isSet => isSet_, "If opted-in or out before executing a function, it must still be an explicit state of opting in or out afterwards";
}
