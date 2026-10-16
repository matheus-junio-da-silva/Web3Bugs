// Historical extract: contracts/7/specs/AToken.spec:125-140
// Source preamble: contracts/7/specs/AToken.spec:1-44
// Dependency status: complete; CVL2 migration intentionally not attempted.
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

rule additiveMint(address a, address b, address c, uint256 x, uint256 y) 
{
	env e;
	uint256 indexRay = gRNI();
	require(balanceOf(a) == balanceOf(b) && a != b);
	uint256 balanceScenario0 = balanceOf(a);
	// storage initialStorage = lastStorage;
	mint(e,c,a,x,indexRay);
	mint(e,c,a,y,indexRay);
	uint256 balanceScenario1 = balanceOf(a);
	// mint(e,c, a, x+y ,indexRay) at initialStorage;
	mint(e, c, b, x+y ,indexRay);

	uint256 balanceScenario2 = balanceOf(b);
	assert bounded_error_eq(balanceScenario1, balanceScenario2, 3), "mint is not additive";
}
