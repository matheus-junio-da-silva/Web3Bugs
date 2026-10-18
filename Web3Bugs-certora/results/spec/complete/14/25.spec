// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/ValidBalances.spec:242-251
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using DummyERC20C as collateralToken

using OtokenHarnessA as shortOtoken

using OtokenHarnessB as longOtoken

methods {
    isVaultExpired(address, uint256) returns bool
    smallVault(address, uint256, uint256) returns bool envfree
    anOtokenA() returns address envfree
    anOtokenB() returns address envfree
    dummyERC20C() returns address envfree
}

function links() {
    require anOtokenA() == shortOtoken;
    require anOtokenB() == longOtoken;
    require dummyERC20C() == collateralToken;
}

rule cantSettleUnexpiredVault(address owner, uint256 vaultId)
{
    links();
    env e;
    require !isVaultExpired(e, owner, vaultId);
    require smallVault(owner, vaultId, 1);
    address whoever;
    sinvoke settleVault(e, owner, vaultId, whoever);
    assert false; // will pass because cannot sinvoke settleVault when dealing with a non-expired vault
}
