// Original source: contracts/12/specs/StableDebtToken.spec:42-56
// Original dependency lines: none
// Target: StableDebtTokenHarness (historical simplified model)
// CVL syntax preserved verbatim; not migrated to CVL2.
rule integirtyBalanceOfTotalSupply(address a, method f )
{
	env e;
	require sinvoke getIncentivesController(e) == 0;
	uint256 balanceABefore = sinvoke balanceOf(e, a);
	uint256 totalSupplyBefore = sinvoke totalSupply(e);
	 
	calldataarg arg;
	sinvoke f(e, arg); 
	require (f.selector != burn(address, uint256).selector);
	uint256 balanceAAfter = sinvoke balanceOf(e, a);
	uint256 totalSupplyAfter = sinvoke totalSupply(e);

	assert  (balanceAAfter != balanceABefore  => (balanceAAfter - balanceABefore  == totalSupplyAfter - totalSupplyBefore));
}
