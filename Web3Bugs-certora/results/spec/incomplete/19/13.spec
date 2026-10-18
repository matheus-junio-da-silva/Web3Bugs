// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousd.spec lines 169-186; target: OUSDHarness

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

definition MAX_UINT256() returns uint 
	= 115792089237316195423570985008687907853269984665640564039457584007913129639935 ;

rule additiveBurn(address burned, uint256 x, uint256 y) {
	env e;
    // require rebasingCreditsPerToken() == ONE() && nonRebasingCreditsPerToken(burned) == ONE(); // only in this case it might be true - but it's not the case as we progress.
    storage init = lastStorage;

    burn(e, burned, x);
    burn(e, burned, y);

    uint b1 = balanceOf(burned);
    
    require x+y <= MAX_UINT256();
    uint sumXY = x+y;
    burn(e, burned, sumXY) at init;

    uint b2 = balanceOf(burned);
    
    assert b1 == b2, "burn is not additive in balance of burned";
}
