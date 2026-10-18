// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousd.spec lines 304-308; target: OUSDHarness

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

function transferCheckEffects(address from, address to, uint256 value, uint256 expectedValueChange)
{
	require to != 0;
	require value != 0;

	env e;
	require e.msg.sender == from;
    uint256 origBalanceOfFrom = balanceOf(from);
    uint256 origBalanceOfTo = balanceOf(to);
	bool result = transfer(e, to, value);
	
	uint256 newBalanceOfTo = balanceOf(to);
	uint256 newBalanceOfFrom = balanceOf(from);

	// Compute the expected new balance.
	uint expectedNewBalanceOfTo;
	uint expectedNewBalanceOfFrom;
	if  (from != to && result) {
		require expectedNewBalanceOfTo == origBalanceOfTo + expectedValueChange;
		require expectedNewBalanceOfFrom == origBalanceOfFrom - expectedValueChange;
	} else {
		require expectedNewBalanceOfTo == origBalanceOfTo;
		require expectedNewBalanceOfFrom == origBalanceOfFrom;
	}
	
	// Effects: new balance of recipient is as expected, and it should also be not less than the original balance
	assert newBalanceOfTo == expectedNewBalanceOfTo && newBalanceOfTo >= origBalanceOfTo, "invalid new balance of to";
	assert newBalanceOfFrom == expectedNewBalanceOfFrom && newBalanceOfFrom <= origBalanceOfFrom, "invalid new balance of from";
}

rule transferIntegrityCheck(address from, address to) {
    uint256 amount;
    transferCheckEffects(from, to, amount, amount);
    assert true; // assertions are in transferCheckEffects
}
