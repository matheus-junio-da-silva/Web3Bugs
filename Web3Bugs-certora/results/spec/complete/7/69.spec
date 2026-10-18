// Source: contracts/7/specs/VariableDebtToken.spec
// Literal property: rule integrityMint, lines 182-199
// Literal dependency source lines: 1;3;5;7-8;10-11;13-15;19;182-199
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
	getReserveNormalizedVariableDebt(address asset) returns (uint256) => gRNVB()
    handleAction(address, uint256, uint256) => NONDET
    balanceOf(address) returns (uint256) envfree
}

definition ray() returns uint = 1000000000000000000000000000;

definition bound() returns uint = ((gRNVB() / ray()) + 1 ) / 2;

ghost gRNVB() returns uint256 {
	axiom gRNVB() == 7 * ray();
}

definition bounded_error_eq(uint x, uint y, uint scale) returns bool = x <= y + (bound() * scale) && x + (bound() * scale) >= y;

rule integrityMint(address a, uint256 x) {
	env e;
	address delegatedUser;
	uint256 index = gRNVB();
	uint256 underlyingBalanceBefore = balanceOf(a);
	uint256 atokenBlanceBefore = scaledBalanceOf(e, a);
	uint256 totalATokenSupplyBefore = scaledTotalSupply(e);
	mint(e, delegatedUser, a, x, index);
	
	uint256 underlyingBalanceAfter = balanceOf(a);
	uint256 atokenBlanceAfter = scaledBalanceOf(e, a);
	uint256 totalATokenSupplyAfter = scaledTotalSupply(e);

	assert atokenBlanceAfter - atokenBlanceBefore == totalATokenSupplyAfter - totalATokenSupplyBefore;
	assert totalATokenSupplyAfter > totalATokenSupplyBefore;
    assert bounded_error_eq(underlyingBalanceAfter, underlyingBalanceBefore+x, 1);
    // assert balanceAfter == balancebefore+x;
}
