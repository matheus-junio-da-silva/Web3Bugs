// Source: contracts/7/specs/AToken.spec
// Literal property: rule permitIntegrity, lines 58-65
// Literal dependency source lines: 9-11;21;58-65
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    nonces(address) returns (uint256) envfree
    allowance(address, address) returns (uint256) envfree
}

rule permitIntegrity(address owner, address spender, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s) 
{
    env e;
    uint256 nonceBefore = nonces(owner);
    permit(e, owner, spender, value, deadline, v, r, s);
    assert allowance(owner, spender) == value;
    assert nonces(owner) == nonceBefore + 1;
}
