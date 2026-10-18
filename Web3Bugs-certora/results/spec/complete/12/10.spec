// Original: contracts/12/specs/VariableDebtToken.spec:6-20; no additional CVL declarations
// Target: VariableDebtToken; historical POOL harness binding shown when used.
// CVL syntax preserved verbatim; CVL2 migration is outside catalog scope.
rule balanceOfChange(address a, address b, method f)
{
	env e;
	require a != b;
	uint256 balanceABefore = sinvoke balanceOf(e, a);
	uint256 balanceBBefore = sinvoke balanceOf(e, b);
	 
	calldataarg arg;
	sinvoke f(e, arg); 

	uint256 balanceAAfter = sinvoke balanceOf(e, a);
	uint256 balanceBAfter = sinvoke balanceOf(e, b);
	
	assert (balanceABefore == balanceAAfter || balanceBBefore == balanceBAfter);
}
