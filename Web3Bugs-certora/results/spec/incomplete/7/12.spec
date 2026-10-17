// Source: contracts/7/specs/AToken.spec
// Literal property: rule mintNoChangeToOther, lines 292-306
// Literal dependency source lines: 9;12-15;21;23;37-39;292-306
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
	handleAction(address, uint256, uint256) => NONDET 
	getReserveNormalizedIncome(address u) returns (uint256) => gRNI()
	balanceOf(address) returns (uint256) envfree
	additionalData(address) returns uint128 envfree
}

definition ray() returns uint = 1000000000000000000000000000;

ghost gRNI() returns uint256 {
	axiom gRNI() == 7 * ray();
}

rule mintNoChangeToOther(address user, uint256 amount, uint256 index, address other)
{
	require other != user;

	env e;
	uint128 otherDataBefore = additionalData(other);
	uint256 otherBalanceBefore = balanceOf(other);
	address caller; 
	mint(e, caller, user, amount, index);

	uint128 otherDataAfter = additionalData(other);
	uint256 otherBalanceAfter = balanceOf(other);

	assert otherBalanceBefore == otherBalanceAfter && otherDataBefore == otherDataAfter;
}
