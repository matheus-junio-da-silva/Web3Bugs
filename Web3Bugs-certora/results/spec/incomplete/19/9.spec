// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousd.spec lines 96-119; target: OUSDHarness

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

invariant rebasingCreditsPerTokenMustBeGreaterThan0() 
	rebasingCreditsPerToken() > 0

rule reverseOptInThenOut(address u) {
	requireInvariant rebasingCreditsPerTokenMustBeGreaterThan0(); // had typo, TODO rerun
	env eF;
	require eF.msg.sender == u;
	
	uint256 _nonRebasingSupply = nonRebasingSupply();
	uint256 _rebasingCredits = rebasingCredits();
	uint256 _balance = balanceOf(u);
	uint256 _nonRebasingCreditsPerToken = nonRebasingCreditsPerToken(u);
	
	// assume currently not opt-in // TODO: Strengthen - should be explicity it's opt-out or require that it is not rebasing at the moment it's run
	require rebaseState(u) != OPT_IN();
	sinvoke rebaseOptIn(eF);
	sinvoke rebaseOptOut(eF);

	uint256 nonRebasingSupply_ = nonRebasingSupply();
	assert _nonRebasingSupply == nonRebasingSupply_, "non rebasing supply must be preserved when opting-in and immediately opting-out";
	
	uint256 rebasingCredits_ = rebasingCredits();
	assert _rebasingCredits == rebasingCredits_, "rebasing credits must be preserved when opting-in and immediately opting-out";
	
	uint256 balance_ = balanceOf(u);
	assert _balance == balance_, "balance of user must be preserved if user opts-in and immediately opts-out";
}
