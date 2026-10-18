// Original source: contracts/12/specs/StableDebtToken.spec:62-101
// Original dependency lines: none
// Target: StableDebtTokenHarness (historical simplified model)
// CVL syntax preserved verbatim; not migrated to CVL2.
rule integirtyBalanceOfTotalSupplyOnBurn(address a, uint256 x)
{
	env e;
	require sinvoke getIncentivesController(e) == 0;
	
	uint256 balanceABefore = sinvoke balanceOf(e, a);
	
	uint256 totalSupplyBefore = sinvoke totalSupply(e);
	uint256 averageStableRateBefore = sinvoke getAverageStableRate(e);
	uint256 debtSupplyBefore = sinvoke rayWadMul(e, averageStableRateBefore, totalSupplyBefore);
	
	uint256 stableRateA = sinvoke getUserStableRate(e, a);
	uint256 repaidDebtA = sinvoke rayWadMul(e, stableRateA, x);
	
	
	sinvoke burn(e, a, x); 
	uint256 balanceAAfter = sinvoke balanceOf(e, a);
	uint256 totalSupplyAfter = sinvoke totalSupply(e);

	if(totalSupplyBefore > x) {
	    /* The amount being burned (x) is smaller than the total supply */
		if(repaidDebtA >= debtSupplyBefore) {
			/*
			The user debt being repaid is at least the debt supply.
			The total supply becomes 0.
			*/
			assert(totalSupplyAfter == 0);
		}
		else {
			assert(balanceAAfter != balanceABefore  =>
			(balanceAAfter - balanceABefore  == totalSupplyAfter - totalSupplyBefore));
		}
	}
	else {
	/* The amount being burned (x) is at least the total supply.
	   The total supply becomes 0.
	*/
		assert (totalSupplyAfter == 0);
	}
}
