// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 749-770
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-14
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    burnBatch(address, uint256[], uint256[])
}

rule cantBurnBatchOtherBalances(env e){
    address from;
    uint256 id1; uint256 id2; uint256 id3; 
    uint256 amount1; uint256 amount2; uint256 amount3;
    uint256[] ids; uint256[] amounts;
    address other;

    uint256 otherBalanceBefore1 = balanceOf(other, id1);
    uint256 otherBalanceBefore2 = balanceOf(other, id2);
    uint256 otherBalanceBefore3 = balanceOf(other, id3);

    burnBatch(e, from, ids, amounts);

    uint256 otherBalanceAfter1 = balanceOf(other, id1);
    uint256 otherBalanceAfter2 = balanceOf(other, id2);
    uint256 otherBalanceAfter3 = balanceOf(other, id3);
    
    assert other != from => (otherBalanceBefore1 == otherBalanceAfter1 
                                && otherBalanceBefore2 == otherBalanceAfter2 
                                && otherBalanceBefore3 == otherBalanceAfter3)
                                , "I like to see your money disappearing";
}
