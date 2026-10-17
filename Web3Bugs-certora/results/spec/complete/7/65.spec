// Source: contracts/7/specs/VariableDebtToken.spec
// Literal property: rule integrityDelegationWithSig, lines 111-116
// Literal dependency source lines: 1;8;111-116
// Historical syntax retained; no reconstruction or CVL2 migration.

rule integrityDelegationWithSig(address delegator, address delegatee, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s) {
    env e;
    uint256 oldNonce = nonces(e, delegator);
    delegationWithSig(e, delegator, delegatee, value, deadline, v, r, s);
    assert nonces(e, delegator) == oldNonce + 1 && borrowAllowance(e, delegator, delegatee) == value;
}
