// Original source: contracts/12/specs/StableDebtToken.spec:126-142
// Original dependency lines: none
// Target: StableDebtTokenHarness (historical simplified model)
// CVL syntax preserved verbatim; not migrated to CVL2.
rule additiveMint(address a, uint256 x, uint256 y) {
	env e;
	address delegatedUser;
	require sinvoke getIncentivesController(e) == 0;
	require getUserStableRate(e, a) == 0;
	uint256 index;
	storage initialStorage = lastStorage;
	sinvoke mint(e, delegatedUser, a, x, index);
	sinvoke mint(e, delegatedUser, a, y, index);
	uint256 balanceScenario1 = sinvoke balanceOf(e, a);
	
	uint256 t = x + y;
	sinvoke mint(e, delegatedUser, a, t ,index) at initialStorage;
	
	uint256 balanceScenario2 = sinvoke balanceOf(e, a);
	assert balanceScenario1 == balanceScenario2, "mint is not additive";
}
