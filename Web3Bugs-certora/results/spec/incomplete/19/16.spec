// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousd.spec lines 214-227; target: OUSDHarness

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

rule transferCheckPreconditions(env e, address to, uint256 value)
{
	require to != 0;
	require value != 0;
	
	address from = e.msg.sender;
	bool precondition = balanceOf(from) >= value;

	bool result = transfer@withrevert(e, to, value);
	bool transferReverted = lastReverted; // loading transferReverted

	// The transfer function must meet the precondition, or to revert.
	assert !precondition => (transferReverted || !result), "If transfer() precondition does not hold, must either revert or return 0";
}
