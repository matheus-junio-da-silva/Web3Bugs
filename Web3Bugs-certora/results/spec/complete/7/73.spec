// Source: contracts/7/specs/VariableDebtToken.spec
// Literal property: rule disallowedFunctionalities, lines 252-258
// Literal dependency source lines: 1;8;23-29;252-258
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
