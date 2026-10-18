// Original source: contracts/12/specs/StableDebtToken.spec:144-153
// Original dependency lines: none
// Target: StableDebtTokenHarness (historical simplified model)
// CVL syntax preserved verbatim; not migrated to CVL2.
rule integrityBurn(address a, uint256 x) {
	env e;
	require sinvoke getIncentivesController(e) == 0;
	uint256 index;
	uint256 balancebefore = sinvoke balanceOf(e, a);
	sinvoke burn(e,a,x);
	
	uint256 balanceAfter = sinvoke balanceOf(e, a);
	assert balanceAfter == balancebefore - x;
}
