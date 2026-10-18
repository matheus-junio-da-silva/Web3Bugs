// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 117-129
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:4-4
methods {
    balanceOfBatch(address[], uint256[]) returns(uint256[]) envfree
}

rule balanceOfBatchRevertCases(env e){
    address[] accounts; uint256[] ids;
    address account1; address account2; address account3;
    uint256 id1; uint256 id2; uint256 id3;

    require accounts.length == 3; 
    require ids.length == 3; 

    require accounts[0] == account1; require accounts[1] == account2; require accounts[2] == account3;

    balanceOfBatch@withrevert(accounts, ids);
    assert lastReverted => (account1 == 0 || account2 == 0 || account3 == 0), "Houston, we have a problem";
}
