// Historical extract: contracts/7/specs/AToken.spec:207-243
// Source preamble: contracts/7/specs/AToken.spec:1-44
// Dependency status: incomplete; CVL2 migration intentionally not attempted.
/**

- values of gRNI passing: ray, 2 * ray

*/

using SimpleERC20 as _underlyingAsset

methods { 
    nonces(address) returns (uint256) envfree
    allowance(address, address) returns (uint256) envfree
	handleAction(address, uint256, uint256) => NONDET 
	getReserveNormalizedIncome(address u) returns (uint256) => gRNI()
	balanceOf(address) returns (uint256) envfree
	additionalData(address) returns uint128 envfree
	finalizeTransfer(address, address, address, uint256, uint256, uint256) => NONDET

	scaledTotalSupply() returns (uint256)
	scaledBalanceOf(address) returns (uint256)
    scaledBalanceOfToBalanceOf(uint256)returns (uint256) envfree
}

definition ray() returns uint = 1000000000000000000000000000;
definition half_ray() returns uint = ray() / 2;
definition bound() returns uint = ((gRNI() / ray()) + 1 ) / 2;

/*
Due to rayDiv and RayMul Rounding (+ 0.5) - blance could increase by (gRNI() / Ray() + 1) / 2.
*/
definition bounded_error_eq(uint x, uint y, uint scale) returns bool = x <= y + (bound() * scale) && x + (bound() * scale) >= y;

ghost sumAllBalance() returns uint256 {
    init_state axiom sumAllBalance() == 0;
}

// summerization for scaledBlanaceOf -> regularBalanceOf + 0.5 (canceling the rayMul)
ghost gRNI() returns uint256 {
	axiom gRNI() == 7 * ray();
}

hook Sstore _userState[KEY address a].balance uint128 balance (uint128 old_balance) STORAGE {
    havoc sumAllBalance assuming sumAllBalance@new() == sumAllBalance@old() + balance - old_balance;
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
