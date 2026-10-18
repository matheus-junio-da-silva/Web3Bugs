// Source: contracts/7/specs/VariableDebtToken.spec
// Literal property: rule nonceChangePermits, lines 89-99
// Literal dependency source lines: 1;8;23-29;89-99
// Historical syntax retained; no reconstruction or CVL2 migration.

definition disAllowedFunctions(method f) returns bool = 
            f.selector == transfer(address, uint256).selector ||
            f.selector == allowance(address, address).selector ||
            f.selector == approve(address, uint256).selector ||
            f.selector == transferFrom(address, address, uint256).selector ||
            f.selector == increaseAllowance(address, uint256).selector ||
            f.selector == decreaseAllowance(address, uint256).selector;

rule nonceChangePermits(method f) 
    filtered { f ->  !f.isView && !disAllowedFunctions(f) } 
{
    env e;
    address user;
    uint256 oldNonce = nonces(e, user);
    calldataarg args;
    f(e, args);
    uint256 newNonce = nonces(e, user);
    assert oldNonce != newNonce => f.selector == delegationWithSig(address, address, uint256, uint256, uint8, bytes32, bytes32).selector;
}
