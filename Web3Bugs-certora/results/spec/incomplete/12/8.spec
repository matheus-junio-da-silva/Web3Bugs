// Original source: contracts/12/specs/StableDebtToken.spec:155-167
// Original dependency lines: none
// Target: StableDebtTokenHarness (historical simplified model)
// CVL syntax preserved verbatim; not migrated to CVL2.
rule additiveBurn(address a, uint256 x,  uint256 y) {
	env e;
	require sinvoke getIncentivesController(e) == 0;
	storage initialStorage = lastStorage;
	sinvoke burn(e, a, x);
	sinvoke burn(e, a, y);
	uint256 balanceScenario1 = balanceOf(e, a);
	uint256 t = x + y;
	sinvoke burn(e, a, t) at initialStorage;

	uint256 balanceScenario2 = balanceOf(e, a);
	assert balanceScenario1 == balanceScenario2, "burn is not additive";
}
