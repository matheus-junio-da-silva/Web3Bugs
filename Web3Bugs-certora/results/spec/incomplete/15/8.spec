// HELIX Project 15 historical CVL extraction
// Source contracts/15/VariableDebtToken.spec property lines 149-162
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
rule integrityOfBurn(address u, uint256 amount) {
	env e;
	uint256 index = indexAtTimestamp(e.block.timestamp);
	uint256 balanceBeforeUser = balanceOf(e, u);
	uint256 totalSupplyBefore = totalSupply(); 

	burn(e, u, amount, index);
	
	uint256 balanceAfterUser = balanceOf(e, u);
	uint256 totalSupplyAfter = totalSupply();

    assert bounded_error_eq(totalSupplyAfter, totalSupplyBefore - amount, 1, index), "total supply integrity"; // total supply reduced
    assert bounded_error_eq(balanceAfterUser, balanceBeforeUser - amount, 1, index), "integrity break";  // user burns ATokens to recieve underlying
}
