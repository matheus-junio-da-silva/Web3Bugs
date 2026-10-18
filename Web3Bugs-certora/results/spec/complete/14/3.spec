// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/MarginVault.spec:43-66
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
methods {
	addShort(address, uint256, uint256) envfree
	addLong(address, uint256, uint256) envfree
	addCollateral(address, uint256, uint256) envfree
	getCollateralAmount(uint256) returns uint256 envfree
	getCollateralAsset(uint256) returns address envfree
	getShortOtoken(uint256) returns address envfree
	getShortAmount(uint256) returns uint256 envfree
	getLongOtoken(uint256) returns address envfree
	getLongAmount(uint256) returns uint256 envfree
}

definition ADDRESSZERO() returns address = 0;

invariant validEntityIndex(uint256 index)
						(getLongAmount(index) > 0 <=> getLongOtoken(index) != 0) &&
						(getShortAmount(index) > 0 <=> getShortOtoken(index) != 0) &&
						(getCollateralAmount(index) > 0 <=> getCollateralAsset(index) != 0)
{
	preserved addLong(address asset, uint256 amt, uint256 _index)
	{
		requireInvariant validEntityIndex(_index);
		requireInvariant validEntityIndex(index);
		require asset != ADDRESSZERO();
	}
	preserved addShort(address asset, uint256 amt, uint256 _index)
	{
		requireInvariant validEntityIndex(_index);
		requireInvariant validEntityIndex(index);
		require asset != ADDRESSZERO();
	}
	preserved addCollateral(address asset, uint256 amt, uint256 _index)
	{
		requireInvariant validEntityIndex(_index);
		requireInvariant validEntityIndex(index);
		require asset != ADDRESSZERO();
	}
}
