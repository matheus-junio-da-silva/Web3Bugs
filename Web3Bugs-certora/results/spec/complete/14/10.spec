// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/MarginVault.spec:201-220
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
methods {
	addShort(address, uint256, uint256) envfree
	collateralAmountLength() returns uint256 envfree
	collateralAssetsLength() returns uint256 envfree
	totalShortAmount() returns uint256 envfree
	shortAmountLength() returns uint256 envfree
	shortOtokensLength() returns uint256 envfree
	longAmountLength() returns uint256 envfree
	longOtokensLength() returns uint256 envfree
}

definition MAXINT() returns uint256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

definition ADDRESSZERO() returns address = 0;

invariant validVault() 	longAmountLength() == longOtokensLength() &&  
						shortAmountLength() == shortOtokensLength() &&
						collateralAmountLength() == collateralAssetsLength()

rule additiveAddShort(address shortOtoken, uint256 x, uint256 y, uint256 index)
{
	requireInvariant validVault();
	require shortOtoken != ADDRESSZERO();
	require index < MAXINT(); // no violation when limiting index
	require x > 0 && y > 0 ;
	uint256 t = x + y ;
    require( t >= x && t >= y); //no overflow
    storage initialStorage = lastStorage;
	invoke addShort(shortOtoken, x, index);
	bool call1 = !lastReverted;
	invoke addShort(shortOtoken, y, index);
	bool call2 = !lastReverted;
	uint256 shortAmountScenario1 = totalShortAmount();
	invoke addShort(shortOtoken, t, index) at initialStorage;
	bool call3 = !lastReverted;
	uint256 shortAmountScenario2 = totalShortAmount();
	assert (call1 && call2) <=> call3, "addShort is not additive, one scenario reverts" ;
	assert call3 => shortAmountScenario1 == shortAmountScenario2, "addShort is not additive" ;
}
