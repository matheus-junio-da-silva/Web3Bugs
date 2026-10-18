// Source: contracts/7/specs/StableDebtToken.spec
// Literal property: rule integrityTimeStamp, lines 166-174
// Literal dependency source lines: 1;10;14-20;166-174
// Historical syntax retained; no reconstruction or CVL2 migration.

definition disAllowedFunctions(method f) returns bool = 
            f.selector == transfer(address, uint256).selector ||
            f.selector == allowance(address, address).selector ||
            f.selector == approve(address, uint256).selector ||
            f.selector == transferFrom(address, address, uint256).selector ||
            f.selector == increaseAllowance(address, uint256).selector ||
            f.selector == decreaseAllowance(address, uint256).selector;

rule integrityTimeStamp(address user, method f) 
    filtered { f ->  !f.isView && !disAllowedFunctions(f) }
{
	env e;
	require getUserLastUpdated(e, user) <= e.block.timestamp;
	calldataarg arg;
    f(e,arg);
	assert getUserLastUpdated(e, user) <= e.block.timestamp;
}
