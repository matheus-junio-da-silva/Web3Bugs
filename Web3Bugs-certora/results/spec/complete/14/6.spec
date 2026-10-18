// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/MarginVault.spec:133-140
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
methods {
	addCollateral(address, uint256, uint256) envfree
	totalCollateral() returns uint256 envfree
	collateralAmountLength() returns uint256 envfree
	collateralAssetsLength() returns uint256 envfree
	shortAmountLength() returns uint256 envfree
	shortOtokensLength() returns uint256 envfree
	longAmountLength() returns uint256 envfree
	longOtokensLength() returns uint256 envfree
}

definition ADDRESSZERO() returns address = 0;

invariant validVault() 	longAmountLength() == longOtokensLength() &&  
						shortAmountLength() == shortOtokensLength() &&
						collateralAmountLength() == collateralAssetsLength()

rule integrityOfAddCollateral(address asset, uint256 x, uint256 index)
{
	requireInvariant validVault();
	require asset != ADDRESSZERO();
	uint256 collateralBefore = totalCollateral();
	sinvoke addCollateral(asset, x, index);
	assert totalCollateral() == collateralBefore + x, "integirty break of addCollateral";
}
