// Source: contracts/7/specs/VariableDebtToken.spec
// Literal property: rule additiveMint, lines 162-176
// Literal dependency source lines: 1;3;5;7-8;10-11;13-15;19;162-176
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

rule additiveMint(address user1, address user2, address user3, uint256 x, uint256 y) {
	env e;
	uint256 index = gRNVB();
    require (user1 != user2  && balanceOf(user1) == balanceOf(user2));

    mint(e, user3, user1, x, index);
	mint(e, user3, user1, y, index);
	uint256 balanceScenario1 = balanceOf(user1);

	mint(e, user3, user2, x+y, index);
	uint256 balanceScenario2 = balanceOf(user2);

    assert bounded_error_eq(balanceScenario1, balanceScenario2, 3), "burn is not additive";
	// assert balanceScenario1 == balanceScenario2, "burn is not additive";
}
