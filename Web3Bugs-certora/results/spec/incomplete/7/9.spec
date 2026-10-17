// Source: contracts/7/specs/AToken.spec
// Literal property: rule integrityBurn, lines 207-243
// Literal dependency source lines: 7;9;12-14;21;23;25;30;37-39;207-243
// Historical syntax retained; no reconstruction or CVL2 migration.

using SimpleERC20 as _underlyingAsset

methods {
	handleAction(address, uint256, uint256) => NONDET 
	getReserveNormalizedIncome(address u) returns (uint256) => gRNI()
	balanceOf(address) returns (uint256) envfree
}

definition ray() returns uint = 1000000000000000000000000000;

definition bound() returns uint = ((gRNI() / ray()) + 1 ) / 2;

definition bounded_error_eq(uint x, uint y, uint scale) returns bool = x <= y + (bound() * scale) && x + (bound() * scale) >= y;

ghost gRNI() returns uint256 {
	axiom gRNI() == 7 * ray();
}

rule integrityBurn(address user, address to, uint256 amount)
{
	env e;
	uint256 indexRay = gRNI();

	require user != currentContract;
	uint256 balanceBeforeUser = balanceOf(user);
	uint256 balanceBeforeTo = balanceOf(to);
	uint256 underlyingBeforeTo =  _underlyingAsset.balanceOf(e, to);
	uint256 underlyingBeforeUser =  _underlyingAsset.balanceOf(e, user);
	uint256 underlyingBeforeSystem =  _underlyingAsset.balanceOf(e, currentContract);
	uint256 totalSupplyBefore = totalSupply(e); 

	burn(e, user, to, amount, indexRay);
	
	uint256 balanceAfterUser = balanceOf(user);
	uint256 balanceAfterTo = balanceOf(to);
	uint256 underlyingAfterTo =  _underlyingAsset.balanceOf(e, to);
	uint256 underlyingAfterUser =  _underlyingAsset.balanceOf(e, user);
	uint256 underlyingAfterSystem =  _underlyingAsset.balanceOf(e, currentContract);
	uint256 totalSupplyAfter = totalSupply(e);

	if (user != to) {
		assert balanceAfterTo == balanceBeforeTo && // balanceOf To should not change
		bounded_error_eq(underlyingBeforeUser, underlyingAfterUser, 1), "integrity break on user!=to";
	}

	if (to != currentContract) {
		assert bounded_error_eq(underlyingAfterSystem, underlyingBeforeSystem - amount, 1) && // system transfer underlying_asset
		bounded_error_eq(underlyingAfterTo,  underlyingBeforeTo + amount, 1) , "integrity break on to!=currentContract";
	} else {
		assert underlyingAfterSystem == underlyingBeforeSystem, "integrity break on to==currentContract";
	} 

    assert bounded_error_eq(totalSupplyAfter, totalSupplyBefore - amount, 1), "total supply integrity"; // total supply reduced
    assert bounded_error_eq(balanceAfterUser, balanceBeforeUser - amount, 1), "integrity break";  // user burns ATokens to recieve underlying
}
