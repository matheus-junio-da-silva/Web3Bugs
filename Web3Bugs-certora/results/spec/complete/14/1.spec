// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/ControllerOrderOfOperations.spec:6-28
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
methods {
    getVaultCollateralAmount(address, uint256, uint256)  returns uint256 envfree
}

rule orderOfOperations (address owner, uint256 vaultId, method f1, method f2) { 
    if ( f1.selector  > f2.selector) {
        assert true;
    } else {
        storage initialStorage = lastStorage;
        env e1; 
        calldataarg arg1;
        sinvoke f1(e1, arg1);
        env e2;
        calldataarg arg2;
        sinvoke f2(e2, arg2);
        
        uint256 vaultCollateralAmount1 = getVaultCollateralAmount(owner, vaultId,0);

        sinvoke f2(e2, arg2) at initialStorage;
        sinvoke f1(e1, arg1);
        
        uint256 vaultCollateralAmount2 = getVaultCollateralAmount(owner, vaultId,0);
        // run first method and then second method and store the result 
        // run the second method then first method and compare result 
        assert vaultCollateralAmount1 == vaultCollateralAmount2;
    }
}
