// Source: contracts/7/specs/AToken.spec
// Literal property: rule balanceOfChange, lines 79-95
// Literal dependency source lines: 9;13-14;21;23;37-39;79-95
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
	getReserveNormalizedIncome(address u) returns (uint256) => gRNI()
	balanceOf(address) returns (uint256) envfree
}

definition ray() returns uint = 1000000000000000000000000000;

ghost gRNI() returns uint256 {
	axiom gRNI() == 7 * ray();
}

rule balanceOfChange(address a, address b, address c, method f ) filtered { f ->  !f.isView }
{
	env e;
	require a!=b && a!=c && b!=c;
	uint256 balanceABefore = balanceOf(a);
	uint256 balanceBBefore = balanceOf(b);
	uint256 balanceCBefore = balanceOf(c);
	 
	calldataarg arg;
	f(e, arg); 

	uint256 balanceAAfter = balanceOf(a);
	uint256 balanceBAfter = balanceOf(b);
	uint256 balanceCAfter = balanceOf(c);

	assert ( balanceABefore == balanceAAfter || balanceBBefore == balanceBAfter || balanceCBefore == balanceCAfter);
}
