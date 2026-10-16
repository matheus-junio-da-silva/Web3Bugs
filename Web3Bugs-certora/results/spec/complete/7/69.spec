// Historical extract: contracts/7/specs/VariableDebtToken.spec:182-199
// Source preamble: contracts/7/specs/VariableDebtToken.spec:1-39
// Dependency status: complete; CVL2 migration intentionally not attempted.
methods {
	// summarization for elimination the raymul operation in balance of and totalSupply.
	getReserveNormalizedVariableDebt(address asset) returns (uint256) => gRNVB()
	setAdditionalData(address user, uint128 data) envfree
    handleAction(address, uint256, uint256) => NONDET
    scaledBalanceOfToBalanceOf(uint256) returns (uint256) envfree
    balanceOf(address) returns (uint256) envfree
}

definition ray() returns uint = 1000000000000000000000000000;
definition bound() returns uint = ((gRNVB() / ray()) + 1 ) / 2;
// summerization for scaledBlanaceOf -> regularBalanceOf + 0.5 (canceling the rayMul)
ghost gRNVB() returns uint256 {
	axiom gRNVB() == 7 * ray();
}
/*
Due to rayDiv and RayMul Rounding (+ 0.5) - blance could increase by (gRNI() / Ray() + 1) / 2.
*/
definition bounded_error_eq(uint x, uint y, uint scale) returns bool = x <= y + (bound() * scale) && x + (bound() * scale) >= y;



definition disAllowedFunctions(method f) returns bool = 
            f.selector == transfer(address, uint256).selector ||
            f.selector == allowance(address, address).selector ||
            f.selector == approve(address, uint256).selector ||
            f.selector == transferFrom(address, address, uint256).selector ||
            f.selector == increaseAllowance(address, uint256).selector ||
            f.selector == decreaseAllowance(address, uint256).selector;


ghost sumAllBalance() returns uint256 {
    init_state axiom sumAllBalance() == 0;
}

hook Sstore _userState[KEY address a].balance uint128 balance (uint128 old_balance) STORAGE {
  havoc sumAllBalance assuming sumAllBalance@new() == sumAllBalance@old() + balance - old_balance;
}

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
