// Source: contracts/7/specs/AToken.spec
// Literal property: rule integrityMint, lines 101-119
// Literal dependency source lines: 9;12-14;18-19;21;23;25;30;37-39;101-119
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
	handleAction(address, uint256, uint256) => NONDET 
	getReserveNormalizedIncome(address u) returns (uint256) => gRNI()
	balanceOf(address) returns (uint256) envfree
	scaledTotalSupply() returns (uint256)
	scaledBalanceOf(address) returns (uint256)
}

definition ray() returns uint = 1000000000000000000000000000;

definition bound() returns uint = ((gRNI() / ray()) + 1 ) / 2;

definition bounded_error_eq(uint x, uint y, uint scale) returns bool = x <= y + (bound() * scale) && x + (bound() * scale) >= y;

ghost gRNI() returns uint256 {
	axiom gRNI() == 7 * ray();
}

rule integrityMint(address a, address b, uint256 x) 
{
	env e;
	uint256 indexRay = gRNI();

	uint256 underlyingBalanceBefore = balanceOf(a);
	uint256 atokenBlanceBefore = scaledBalanceOf(e, a);
	uint256 totalATokenSupplyBefore = scaledTotalSupply(e);

	mint(e,b,a,x,indexRay);
	
	uint256 underlyingBalanceAfter = balanceOf(a);
	uint256 atokenBlanceAfter = scaledBalanceOf(e, a);
	uint256 totalATokenSupplyAfter = scaledTotalSupply(e);

	assert atokenBlanceAfter - atokenBlanceBefore == totalATokenSupplyAfter - totalATokenSupplyBefore;
	assert totalATokenSupplyAfter > totalATokenSupplyBefore;
	assert bounded_error_eq(underlyingBalanceAfter, underlyingBalanceBefore+x, 1);
}
