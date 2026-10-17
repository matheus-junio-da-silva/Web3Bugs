// Original: contracts/12/specs/VariableDebtToken.spec:108-121; using declaration line 1
// Target: VariableDebtToken; historical POOL harness binding shown when used.
// CVL syntax preserved verbatim; CVL2 migration is outside catalog scope.
using LendingPoolHarnessForVariableDebtToken as POOL

rule additiveMint(address a, address delegatedUser, uint256 x, uint256 y) {
	env e;
	address asset;
	uint256 index = POOL.getReserveNormalizedVariableDebt(e, asset);
	storage initialStorage = lastStorage;
	sinvoke mint(e, delegatedUser, a, x, index);
	sinvoke mint(e, delegatedUser, a, y, index);
	uint256 balanceScenario1 = balanceOf(e, a);
	uint256 t = x + y;
	sinvoke mint(e, delegatedUser, a, t ,index) at initialStorage;

	uint256 balanceScenario2 = balanceOf(e, a);
	assert balanceScenario1 == balanceScenario2, "mint is not additive";
}
