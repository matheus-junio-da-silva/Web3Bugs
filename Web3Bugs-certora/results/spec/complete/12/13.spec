// Original: contracts/12/specs/VariableDebtToken.spec:65-79; using declaration line 1
// Target: VariableDebtToken; historical POOL harness binding shown when used.
// CVL syntax preserved verbatim; CVL2 migration is outside catalog scope.
using LendingPoolHarnessForVariableDebtToken as POOL

rule integirtyBalanceOfTotalSupplyOnMint(address u, address delegatedUser)
{
	env e;
	
	uint256 balanceUBefore = balanceOf(e, u);
	uint256 totalSupplyBefore = totalSupply(e);
	 
	uint256 x;
	address asset;
	uint256 index = POOL.getReserveNormalizedVariableDebt(e, asset);
	sinvoke mint(e, delegatedUser, u, x, index); 
	uint256 balanceUAfter = balanceOf(e, u);
	uint256 totalSupplyAfter = totalSupply(e);
	assert (balanceUAfter != balanceUBefore  => (balanceUAfter - balanceUBefore  == totalSupplyAfter - totalSupplyBefore));
}
