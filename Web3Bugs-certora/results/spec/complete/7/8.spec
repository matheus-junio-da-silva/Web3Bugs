// Historical extract: contracts/7/specs/AToken.spec:178-201
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

rule additiveTransfer(address from1, address from2, address to1, address to2, uint256 x, uint256 y)
{
	env e1;
	env e2;
    uint256 indexRay = gRNI();
	require (from1 != from2 && to1 != to2 && from1 != to2 && from2 != to1 && 
	        (from1 == to1 <=> from2 == to2) &&
			 balanceOf(from1) == balanceOf(from2) && balanceOf(to1) == balanceOf(to2));

	require e1.msg.sender == from1;
	require e2.msg.sender == from2;
	transfer(e1, to1, x);
	transfer(e1, to1, y);
	uint256 balanceFromScenario1 = balanceOf(from1);
	uint256 balanceToScenario1 = balanceOf(to1);

	transfer(e2, to2, x+y);
	
	uint256 balanceFromScenario2 = balanceOf(from2);
	uint256 balanceToScenario2 = balanceOf(to2);
	
	assert 	bounded_error_eq(balanceFromScenario1, balanceFromScenario2, 3)  &&
	 		bounded_error_eq(balanceToScenario1, balanceToScenario2, 3), "transfer is not additive";
}
