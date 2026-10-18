// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 182-221
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-10
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    safeBatchTransferFrom(address, address, uint256[], uint256[], bytes)
}

rule transferBatchCorrectness(env e){
    address from; address to; uint256[] ids; uint256[] amounts; bytes data;
    uint256 idToCheck1; uint256 amountToCheck1;
    uint256 idToCheck2; uint256 amountToCheck2;
    uint256 idToCheck3; uint256 amountToCheck3;

    require to != from;
    require idToCheck1 != idToCheck2 && idToCheck3 != idToCheck2 && idToCheck1 != idToCheck3;
    
    require ids.length == 3;        
    require amounts.length == 3;    
    require ids[0] == idToCheck1; require amounts[0] == amountToCheck1;
    require ids[1] == idToCheck2; require amounts[1] == amountToCheck2;
    require ids[2] == idToCheck3; require amounts[2] == amountToCheck3;

    uint256 fromBalanceBefore1 = balanceOf(from, idToCheck1);
    uint256 fromBalanceBefore2 = balanceOf(from, idToCheck2);
    uint256 fromBalanceBefore3 = balanceOf(from, idToCheck3);

    uint256 toBalanceBefore1 = balanceOf(to, idToCheck1);
    uint256 toBalanceBefore2 = balanceOf(to, idToCheck2);
    uint256 toBalanceBefore3 = balanceOf(to, idToCheck3);

    safeBatchTransferFrom(e, from, to, ids, amounts, data);

    uint256 fromBalanceAfter1 = balanceOf(from, idToCheck1);
    uint256 fromBalanceAfter2 = balanceOf(from, idToCheck2);
    uint256 fromBalanceAfter3 = balanceOf(from, idToCheck3);

    uint256 toBalanceAfter1 = balanceOf(to, idToCheck1);
    uint256 toBalanceAfter2 = balanceOf(to, idToCheck2);
    uint256 toBalanceAfter3 = balanceOf(to, idToCheck3);

    assert (fromBalanceBefore1 == fromBalanceAfter1 + amountToCheck1)
                && (fromBalanceBefore2 == fromBalanceAfter2 + amountToCheck2)
                && (fromBalanceBefore3 == fromBalanceAfter3 + amountToCheck3), "Something wet wrong";
    assert (toBalanceBefore1 == toBalanceAfter1 - amountToCheck1)
                && (toBalanceBefore2 == toBalanceAfter2 - amountToCheck2)
                && (toBalanceBefore3 == toBalanceAfter3 - amountToCheck3), "Something wet wrong";
}
