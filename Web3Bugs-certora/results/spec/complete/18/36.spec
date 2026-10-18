// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 637-646
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:14-14
methods {
    burnBatch(address, uint256[], uint256[])
}

rule burnBatchRevertCases(env e){
    address from; uint256[] ids; uint256[] amounts;

    require ids.length < 1000000000;
    require amounts.length < 1000000000;

    burnBatch@withrevert(e, from, ids, amounts);

    assert (from == 0 || ids.length != amounts.length) => lastReverted, "Should revert";
}
