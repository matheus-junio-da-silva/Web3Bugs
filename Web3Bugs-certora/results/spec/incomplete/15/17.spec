// HELIX Project 15 historical CVL extraction
// Source contracts/15/VariableDebtToken.spec property lines 311-328
// Historic syntax unchanged; dependency-incomplete, no CVL2 migration

// Original CVL non-property helpers from contracts/15/VariableDebtToken.spec
methods {
	// summarization for elimination the raymul operation in balance of and totalSupply.
	//getReserveNormalizedVariableDebt(address asset) returns (uint256) => indexAtTimestamp(e.block.timestamp)
	//setAdditionalData(address user, uint128 data) envfree
    handleAction(address, uint256, uint256) => NONDET
	scaledBalanceOfToBalanceOf(uint256) returns (uint256) envfree
    //balanceOf(address) returns (uint256) envfree
}

definition ray() returns uint = 1000000000000000000000000000; // 10^27
definition wad() returns uint = 1000000000000000000; // 10^18
definition bound(uint256 index) returns uint = ((index / ray()) + 1 ) / 2;
// summerization for scaledBlanaceOf -> regularBalanceOf + 0.5 (canceling the rayMul)
// ghost gRNVB() returns uint256 {
// 	axiom gRNVB() == 7 * ray();
// }
/*
Due to rayDiv and RayMul Rounding (+ 0.5) - blance could increase by (gRNI() / Ray() + 1) / 2.
*/
definition bounded_error_eq(uint x, uint y, uint scale, uint256 index) returns bool = x <= y + (bound(index) * scale) && x + (bound(index) * scale) >= y;



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

// Exact literal original property follows
rule integrityMint_atoken(address a, uint256 x) {
	env e;
	address delegatedUser;
	uint256 index = indexAtTimestamp(e.block.timestamp);
	uint256 underlyingBalanceBefore = balanceOf(e, a);
	uint256 atokenBlanceBefore = scaledBalanceOf(a);
	uint256 totalATokenSupplyBefore = scaledTotalSupply(e);
	mint(e, delegatedUser, a, x, index);
	
	uint256 underlyingBalanceAfter = balanceOf(e, a);
	uint256 atokenBlanceAfter = scaledBalanceOf(a);
	uint256 totalATokenSupplyAfter = scaledTotalSupply(e);

	assert atokenBlanceAfter - atokenBlanceBefore == totalATokenSupplyAfter - totalATokenSupplyBefore;
	//assert totalATokenSupplyAfter > totalATokenSupplyBefore;
    //assert bounded_error_eq(underlyingBalanceAfter, underlyingBalanceBefore+x, 1, index);
    // assert balanceAfter == balancebefore+x;
}
