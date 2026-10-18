// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/MarginVault.spec:176-183
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
methods {
	addCollateral(address, uint256, uint256) envfree
	removeCollateral(address, uint256, uint256) envfree
	totalCollateral() returns uint256 envfree
	collateralAmountLength() returns uint256 envfree
	collateralAssetsLength() returns uint256 envfree
	shortAmountLength() returns uint256 envfree
	shortOtokensLength() returns uint256 envfree
	longAmountLength() returns uint256 envfree
	longOtokensLength() returns uint256 envfree
}

invariant validVault() 	longAmountLength() == longOtokensLength() &&  
						shortAmountLength() == shortOtokensLength() &&
						collateralAmountLength() == collateralAssetsLength()

rule inverseAddRemoveCollateral(address asset, uint256 x, uint256 index) 
{
	requireInvariant validVault();
	uint256 collateralBefore = totalCollateral();
	sinvoke addCollateral(asset, x, index);
	invoke removeCollateral(asset, x, index);
	assert !lastReverted && totalCollateral() == collateralBefore, "removeCollateral is not inverse of addCollateral"; 
}
