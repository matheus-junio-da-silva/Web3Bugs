// Original source: contracts/12/specs/StableDebtToken.spec:174-184
// Original dependency lines: none
// Target: StableDebtTokenHarness (historical simplified model)
// CVL syntax preserved verbatim; not migrated to CVL2.
rule inverseMintBurn(address a, uint256 x) {
	env e;
	address delegatedUser;
	require sinvoke getIncentivesController(e) == 0;
	uint256 index;
	uint256 balancebefore = sinvoke balanceOf(e, a);
	sinvoke mint(e, delegatedUser, a, x, index);
	sinvoke burn(e, a, x);
	uint256 balanceAfter = sinvoke balanceOf(e, a);
	assert balancebefore == balanceAfter, "burn is not the inverse of mint";
}
