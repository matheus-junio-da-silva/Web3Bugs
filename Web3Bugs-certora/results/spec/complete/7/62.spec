// Source: contracts/7/specs/VariableDebtToken.spec
// Literal property: rule balanceOfChange, lines 71-86
// Literal dependency source lines: 1;3;7-8;10;13-15;23-29;71-86
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
	getReserveNormalizedVariableDebt(address asset) returns (uint256) => gRNVB()
    balanceOf(address) returns (uint256) envfree
}

definition ray() returns uint = 1000000000000000000000000000;

ghost gRNVB() returns uint256 {
	axiom gRNVB() == 7 * ray();
}

definition disAllowedFunctions(method f) returns bool = 
            f.selector == transfer(address, uint256).selector ||
            f.selector == allowance(address, address).selector ||
            f.selector == approve(address, uint256).selector ||
            f.selector == transferFrom(address, address, uint256).selector ||
            f.selector == increaseAllowance(address, uint256).selector ||
            f.selector == decreaseAllowance(address, uint256).selector;

rule balanceOfChange(address a, address b, method f) 
    filtered { f ->  !f.isView && !disAllowedFunctions(f) }
{
	env e;
	require a != b;
	uint256 balanceABefore = balanceOf(a);
	uint256 balanceBBefore = balanceOf(b);
	 
	calldataarg arg;
    f(e, arg); 

	uint256 balanceAAfter = balanceOf(a);
	uint256 balanceBAfter = balanceOf(b);
	
	assert (balanceABefore == balanceAAfter || balanceBBefore == balanceBAfter);
}
