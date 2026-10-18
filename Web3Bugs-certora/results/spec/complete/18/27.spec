// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 459-468
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:12-12
methods {
    mintBatch(address, uint256[], uint256[], bytes)
}

rule mintBatchRevertCases(env e){
    address to; uint256[] ids; uint256[] amounts; bytes data;

    require ids.length < 1000000000;
    require amounts.length < 1000000000;

    mintBatch@withrevert(e, to, ids, amounts, data);

    assert (ids.length != amounts.length || to == 0) => lastReverted, "Should revert";
}
