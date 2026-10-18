// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/ousdExtras.spec lines 29-65; target: OUSDHarness

using OUSDHarness as ousd

methods {
	totalSupply() returns uint256 envfree
	balanceOf(address) returns uint256 envfree
	allowance(address,address) returns uint256 envfree

	rebasingCreditsPerToken() returns uint256 envfree
	nonRebasingCreditsPerToken(address) returns uint256 envfree
	nonRebasingSupply() returns uint256 envfree
	rebasingCredits() returns uint256 envfree

	rebaseState(address) returns uint8 envfree

	// certora harnesses
	Certora_maxSupply() returns uint256 envfree
	Certora_isNonRebasingAccount(address) returns bool envfree
}

definition MAX_UINT256() returns uint 
	= 115792089237316195423570985008687907853269984665640564039457584007913129639935 ;

invariant rebasingCreditsPerTokenMustBeGreaterThan0() 
	rebasingCreditsPerToken() > 0

rule additiveBurnRanges(address burned, uint256 x, uint256 y) {
    env e;
    requireInvariant rebasingCreditsPerTokenMustBeGreaterThan0();
    uint256 _rebasingCreditsPerToken = rebasingCreditsPerToken();
	
    uint256 _x = x;
    uint256 _y = y;
    require x+y <= MAX_UINT256();
    uint sumXY = x+y;
    require balanceOf(burned) > sumXY;


    require rebasingCreditsPerToken() >= 1000000;

    storage init = lastStorage;

    uint b0 = balanceOf(burned);

    burn(e, burned, x);
    burn(e, burned, y);

    uint b1 = balanceOf(burned);
    
    
    burn(e, burned, sumXY) at init;

    uint b2 = balanceOf(burned);

    uint diff = 0;
    if(b1 > b2){
        diff = b1 - b2;
    } else {
        diff = b2 - b1;
    }
    
    assert diff < 1000000, "burn is not additive in balance of burned";
}
