// Original: contracts/12/specs/VariableDebtToken.spec:90-102; using declaration line 1
// Target: VariableDebtToken; historical POOL harness binding shown when used.
// CVL syntax preserved verbatim; CVL2 migration is outside catalog scope.
using LendingPoolHarnessForVariableDebtToken as POOL

rule integrityMint(address u, address delegatedUser, uint256 x) {
	env e;
	address asset;
	uint256 index = POOL.getReserveNormalizedVariableDebt(e,asset);
	uint256 balanceUBefore = balanceOf(e, u);
	uint256 balanceDelegatedUBefore = balanceOf(e, delegatedUser);
	sinvoke mint(e, delegatedUser, u, x, index);
	
	uint256 balanceUAfter = balanceOf(e, u);
	uint256 balanceDelegatedUAfter = balanceOf(e, delegatedUser);
	
	assert balanceUAfter == balanceUBefore + x && (u != delegatedUser => (balanceDelegatedUAfter == balanceDelegatedUBefore));
}
