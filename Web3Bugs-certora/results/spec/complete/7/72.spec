// Source: contracts/7/specs/VariableDebtToken.spec
// Literal property: rule mintNoChangeToOther, lines 230-247
// Literal dependency source lines: 1;3;5;7-8;10;13-15;230-247
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

rule mintNoChangeToOther(address user, address onBehalfOf, uint256 amount, uint256 index, address other) {
	require other != user && other != onBehalfOf;

	env e;
	uint256 userBalanceBefore = balanceOf(user);
	uint256 otherBalanceBefore = balanceOf(other);

	mint(e, user, onBehalfOf, amount, index);

  	uint256 userBalanceAfter = balanceOf(user);
	uint256 otherBalanceAfter = balanceOf(other);

	if (user != onBehalfOf) {
		assert userBalanceBefore == userBalanceAfter ; 
	}

	assert otherBalanceBefore == otherBalanceAfter ;
}
