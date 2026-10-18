// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 488-516
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-12
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    mintBatch(address, uint256[], uint256[], bytes)
}

rule mintBatchCorrectWork(env e){
    address to;
    uint256 id1; uint256 id2; uint256 id3; 
    uint256 amount1; uint256 amount2; uint256 amount3;
    uint256[] ids; uint256[] amounts;
    bytes data;

    require ids.length == 3; 
    require amounts.length == 3; 

    require id1 != id2 && id2 != id3 && id3 != id1;
    require ids[0] == id1; require ids[1] == id2; require ids[2] == id3;
    require amounts[0] == amount1; require amounts[1] == amount2; require amounts[2] == amount3;

    uint256 otherBalanceBefore1 = balanceOf(to, id1);
    uint256 otherBalanceBefore2 = balanceOf(to, id2);
    uint256 otherBalanceBefore3 = balanceOf(to, id3);

    mintBatch(e, to, ids, amounts, data);

    uint256 otherBalanceAfter1 = balanceOf(to, id1);
    uint256 otherBalanceAfter2 = balanceOf(to, id2);
    uint256 otherBalanceAfter3 = balanceOf(to, id3);
    
    assert otherBalanceBefore1 == otherBalanceAfter1 - amount1
            && otherBalanceBefore2 == otherBalanceAfter2 - amount2
            && otherBalanceBefore3 == otherBalanceAfter3 - amount3
            , "Something is wrong";
}
