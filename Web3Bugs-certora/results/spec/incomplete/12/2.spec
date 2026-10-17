// Original source: contracts/12/specs/StableDebtToken.spec:21-36
// Original dependency lines: none
// Target: StableDebtTokenHarness (historical simplified model)
// CVL syntax preserved verbatim; not migrated to CVL2.
rule balanceOfChange(address a, address b, method f)
{
	env e;
	require a!=b;
	require sinvoke getIncentivesController(e) == 0;
	uint256 balanceABefore = sinvoke balanceOf(e, a);
	uint256 balanceBBefore = sinvoke balanceOf(e, b);
	 
	calldataarg arg;
	sinvoke f(e, arg); 

	uint256 balanceAAfter = sinvoke balanceOf(e, a);
	uint256 balanceBAfter = sinvoke balanceOf(e, b);
	
	assert (balanceABefore == balanceAAfter || balanceBBefore == balanceBAfter );
}
