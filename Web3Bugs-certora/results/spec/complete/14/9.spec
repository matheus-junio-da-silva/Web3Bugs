// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/MarginVault.spec:188-196
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
methods {
	addShort(address, uint256, uint256) envfree
	collateralAmountLength() returns uint256 envfree
	collateralAssetsLength() returns uint256 envfree
	totalShortAmount() returns uint256 envfree
	shortAmountLength() returns uint256 envfree
	shortOtokensLength() returns uint256 envfree
	getShortOtoken(uint256) returns address envfree
	longAmountLength() returns uint256 envfree
	longOtokensLength() returns uint256 envfree
}

definition ADDRESSZERO() returns address = 0;

invariant validVault() 	longAmountLength() == longOtokensLength() &&  
						shortAmountLength() == shortOtokensLength() &&
						collateralAmountLength() == collateralAssetsLength()

rule integrityOfAddShort(address shortOtoken, uint256 x, uint256 index)
{
	requireInvariant validVault();
	require shortOtoken != ADDRESSZERO();
	uint256 shortAmountBefore = totalShortAmount();
	sinvoke addShort(shortOtoken, x, index);
	assert  totalShortAmount() == shortAmountBefore + x &&
		    getShortOtoken(index) == shortOtoken, "integrity break of addShort";
}
