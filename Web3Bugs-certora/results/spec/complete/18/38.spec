// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 666-692
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-14
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    burnBatch(address, uint256[], uint256[])
}

rule burnBatchCorrectWork(env e){
    address from;
    uint256 id1; uint256 id2; uint256 id3; 
    uint256 amount1; uint256 amount2; uint256 amount3;
    uint256[] ids; uint256[] amounts;

    require ids.length == 3; 

    require id1 != id2 && id2 != id3 && id3 != id1;
    require ids[0] == id1; require ids[1] == id2; require ids[2] == id3;
    require amounts[0] == amount1; require amounts[1] == amount2; require amounts[2] == amount3;

    uint256 otherBalanceBefore1 = balanceOf(from, id1);
    uint256 otherBalanceBefore2 = balanceOf(from, id2);
    uint256 otherBalanceBefore3 = balanceOf(from, id3);

    burnBatch(e, from, ids, amounts);

    uint256 otherBalanceAfter1 = balanceOf(from, id1);
    uint256 otherBalanceAfter2 = balanceOf(from, id2);
    uint256 otherBalanceAfter3 = balanceOf(from, id3);
    
    assert otherBalanceBefore1 == otherBalanceAfter1 + amount1
            && otherBalanceBefore2 == otherBalanceAfter2 + amount2
            && otherBalanceBefore3 == otherBalanceAfter3 + amount3
            , "Something is wrong";
}
