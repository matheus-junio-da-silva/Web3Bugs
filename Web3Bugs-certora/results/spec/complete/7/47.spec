// Source: contracts/7/specs/StableDebtToken.spec
// Literal property: rule disallowedFunctionalities, lines 338-344
// Literal dependency source lines: 1;10;14-20;338-344
// Historical syntax retained; no reconstruction or CVL2 migration.

definition disAllowedFunctions(method f) returns bool = 
            f.selector == transfer(address, uint256).selector ||
            f.selector == allowance(address, address).selector ||
            f.selector == approve(address, uint256).selector ||
            f.selector == transferFrom(address, address, uint256).selector ||
            f.selector == increaseAllowance(address, uint256).selector ||
            f.selector == decreaseAllowance(address, uint256).selector;

rule disallowedFunctionalities(method f)
    filtered { f -> disAllowedFunctions(f) }
{
    env e; calldataarg args;
    f@withrevert(e, args);
    assert lastReverted;
}
