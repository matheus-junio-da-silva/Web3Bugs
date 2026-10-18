// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Burnable.spec lines 142-160
// Target: ERC1155BurnableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Burnable.spec:2-3
methods {
    balanceOf(address, uint256) returns uint256 envfree
    isApprovedForAll(address,address) returns bool envfree
}

rule burnBatchOnEmptyArraysChangesNothing {
    uint256 token; address nonHolderA; address nonHolderB;

    uint256 startingBalance = balanceOf(nonHolderA, token);
    bool startingPermission = isApprovedForAll(nonHolderA, nonHolderB);

    env e; address holder; uint256[] noTokens; uint256[] noBurnAmounts;
    require noTokens.length == 0; require noBurnAmounts.length == 0;

    burnBatch(e, holder, noTokens, noBurnAmounts);
    
    uint256 endingBalance = balanceOf(nonHolderA, token);
    bool endingPermission = isApprovedForAll(nonHolderA, nonHolderB);

    assert startingBalance == endingBalance, 
        "burnBatch must not change token balances if passed empty arrays";
    assert startingPermission == endingPermission, 
        "burnBatch must not change account permissions if passed empty arrays";
}
