// Source: contracts/7/specs/AToken.spec
// Literal property: rule burnNoChangeToOther, lines 271-287
// Literal dependency source lines: 9;12-15;21;23;37-39;271-287
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

rule burnNoChangeToOther(address user, address recieverOfUnderlying, uint256 amount, uint256 index, address other) 
{
  
	require other != user && other != recieverOfUnderlying;
	
	env e;
	uint256 otherDataBefore = additionalData(other);
	uint256 otherBalanceBefore = balanceOf(other);
	
	burn(e, user, recieverOfUnderlying, amount, index);
	
	uint256 otherDataAfter = additionalData(other);
	uint256 otherBalanceAfter = balanceOf(other);

	assert otherDataBefore == otherDataAfter && 
	       otherBalanceBefore == otherBalanceAfter;
}
