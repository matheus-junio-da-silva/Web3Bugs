// Historical extract: contracts/7/specs/VariableDebtToken.spec:54-66
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

rule whoChangeTotalSupply(method f) 
    filtered { f ->  !f.isView && !disAllowedFunctions(f) } 
{
    env e;
    uint256 oldTotalSupply = totalSupply(e);
    calldataarg args;
    f(e, args);
    uint256 newTotalSupply = totalSupply(e);
    assert oldTotalSupply != newTotalSupply => 
           (e.msg.sender == POOL(e) && 
           (f.selector == burn(address, uint256, uint256).selector || 
            f.selector == mint(address, address, uint256, uint256).selector));
}
