// Source: contracts/7/specs/VariableDebtToken.spec
// Literal property: rule inverseMintBurn, lines 102-109
// Literal dependency source lines: 1;3;5;7-8;10;13-15;102-109
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

rule inverseMintBurn(address a, address delegatedUser, uint256 amount, uint256 index) {
	env e;
	uint256 balancebefore = balanceOf(a);
	mint(e, delegatedUser, a, amount, index);
	burn(e, a, amount, index);
	uint256 balanceAfter = balanceOf(a);
	assert balancebefore == balanceAfter, "burn is not the inverse of mint";
}
