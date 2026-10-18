// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/MarginVault.spec:225-232
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
methods {
	addShort(address, uint256, uint256) envfree
	removeShort(address, uint256, uint256) envfree
	collateralAmountLength() returns uint256 envfree
	collateralAssetsLength() returns uint256 envfree
	totalShortAmount() returns uint256 envfree
	shortAmountLength() returns uint256 envfree
	shortOtokensLength() returns uint256 envfree
	longAmountLength() returns uint256 envfree
	longOtokensLength() returns uint256 envfree
}

invariant validVault() 	longAmountLength() == longOtokensLength() &&  
						shortAmountLength() == shortOtokensLength() &&
						collateralAmountLength() == collateralAssetsLength()

rule inverseAddRemoveShort(address shortOtoken, uint256 x, uint256 index) 
{
	requireInvariant validVault();
	uint256 shortAmountBefore = totalShortAmount();
	sinvoke addShort(shortOtoken, x, index);
	invoke removeShort(shortOtoken, x, index);
	assert !lastReverted && totalShortAmount() == shortAmountBefore, "removeShort is not inverse of addShort"; 
}
