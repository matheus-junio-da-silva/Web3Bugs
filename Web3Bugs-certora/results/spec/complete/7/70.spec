// Source: contracts/7/specs/VariableDebtToken.spec
// Literal property: rule burnZeroDoesntChangeBalance, lines 202-208
// Literal dependency source lines: 1;3;5;7-8;10;13-15;202-208
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
	getReserveNormalizedVariableDebt(address asset) returns (uint256) => gRNVB()
    handleAction(address, uint256, uint256) => NONDET
    balanceOf(address) returns (uint256) envfree
}

definition ray() returns uint = 1000000000000000000000000000;

ghost gRNVB() returns uint256 {
	axiom gRNVB() == 7 * ray();
}

rule burnZeroDoesntChangeBalance(address u, uint256 index) {
	env e;
	uint256 balanceBefore = balanceOf(u);
	invoke burn(e, u, 0, index);
	uint256 balanceAfter = balanceOf(u);
	assert balanceBefore == balanceAfter;
}
