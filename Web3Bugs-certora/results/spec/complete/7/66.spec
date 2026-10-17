// Source: contracts/7/specs/VariableDebtToken.spec
// Literal property: rule integrityOfBurn, lines 122-135
// Literal dependency source lines: 1;3;5;7-8;10-11;13-15;19;122-135
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

rule integrityOfBurn(address u, uint256 amount) {
	env e;
	uint256 index = gRNVB();
	uint256 balanceBeforeUser = balanceOf(u);
	uint256 totalSupplyBefore = totalSupply(e); 

	burn(e, u, amount, index);
	
	uint256 balanceAfterUser = balanceOf(u);
	uint256 totalSupplyAfter = totalSupply(e);

    assert bounded_error_eq(totalSupplyAfter, totalSupplyBefore - amount, 1), "total supply integrity"; // total supply reduced
    assert bounded_error_eq(balanceAfterUser, balanceBeforeUser - amount, 1), "integrity break";  // user burns ATokens to recieve underlying
}
