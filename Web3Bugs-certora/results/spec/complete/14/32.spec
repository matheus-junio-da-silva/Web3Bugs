// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/controller.spec:101-120
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
methods {
    getVaultCollateralAmount(address, uint256, uint256)  returns uint256 envfree
}

rule onlyOneVaultModified (address owner1, address owner2, uint256 vaultId1, uint256 vaultId2, address to,  method f) {
    require owner1 != owner2 || vaultId1 != vaultId2;
    uint256 collateralAmt1Before = getVaultCollateralAmount(owner1, vaultId1, 0);
    uint256 collateralAmt2Before = getVaultCollateralAmount(owner2, vaultId2, 0); 
    env e;
    calldataarg arg;
    sinvoke f(e, arg);
    uint256 collateralAmt1After = getVaultCollateralAmount@withrevert(owner1, vaultId1, 0);
    bool r1 = lastReverted;
    if (r1) {
       collateralAmt1After = 0;
    }
    uint256 collateralAmt2After = getVaultCollateralAmount@withrevert(owner2, vaultId2, 0);
    bool r2 = lastReverted;
    if (r2) {
       collateralAmt2After = 0;
    }
    assert !r1 || !r2, "at most one vault could have been deleted";
    assert (collateralAmt1Before != collateralAmt1After => collateralAmt2Before==collateralAmt2After), "two vaults were updated";
 }
