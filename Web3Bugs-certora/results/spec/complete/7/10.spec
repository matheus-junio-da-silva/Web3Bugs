// Historical extract: contracts/7/specs/AToken.spec:249-266
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

rule additiveBurn(address user1, address user2, address to1, address to2, uint256 x, uint256 y) 
{
	env e;
	uint256 indexRay = gRNI();
	require (user1 != user2 && to1 != to2 && user1 != to2 && user2 != to1 && 
	        (user1 == to1 <=> user2 == to2) &&
			 balanceOf(user1) == balanceOf(user2) && balanceOf(to1) == balanceOf(to2));
	require user1 != currentContract && user2 != currentContract;

	sinvoke burn(e, user1, to1, x, indexRay);
	sinvoke burn(e, user1, to1, y, indexRay);
	uint256 balanceUserScenario1 = balanceOf(user1);
	
	sinvoke burn(e, user2, to2, x+y, indexRay);
	uint256 balanceUserScenario2 = balanceOf(user2);
	
	assert 	bounded_error_eq(balanceUserScenario1, balanceUserScenario2, 3), "burn is not additive";
}
