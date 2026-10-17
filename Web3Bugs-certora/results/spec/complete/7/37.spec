// Source: contracts/7/specs/StableDebtToken.spec
// Literal property: rule integrityDelegationWithSig, lines 176-181
// Literal dependency source lines: 1;10;176-181
// Historical syntax retained; no reconstruction or CVL2 migration.

rule integrityDelegationWithSig(address delegator, address delegatee, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s) {
    env e;
    uint256 oldNonce = nonces(e, delegator);
    delegationWithSig(e, delegator, delegatee, value, deadline, v, r, s);
    assert nonces(e, delegator) == oldNonce + 1 && borrowAllowance(e, delegator, delegatee) == value;
}
