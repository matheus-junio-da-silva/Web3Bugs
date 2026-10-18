// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/MarginVault.spec:101-123
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
methods {
	addCollateral(address, uint256, uint256) envfree
	collateralAmountLength() returns uint256 envfree
	collateralAssetsLength() returns uint256 envfree
	getCollateralAmount(uint256) returns uint256 envfree
	getCollateralAsset(uint256) returns address envfree
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

rule successOfAddCollateral(address asset, uint256 x, uint256 index)
{
	requireInvariant validVault();
	require asset != ADDRESSZERO();
	require x > 0;
	require index < MAXINT();
	// require index <= collateralAmountLength();
	if (index < collateralAmountLength()) {
		require asset == getCollateralAsset(index);
		require getCollateralAmount(index) + x < MAXINT();

		invoke addCollateral(asset, x, index);
		assert !lastReverted, "addCollateral may revert when precondition holds";
	}
	else if ((index == collateralAmountLength())) {
		invoke addCollateral(asset, x, index);
		assert !lastReverted, "addCollateral may revert when precondition holds";
	}
	else {
		invoke addCollateral(asset, x, index);
		assert lastReverted, "addCollateral may not revert when precondition not holds";
	}
}
