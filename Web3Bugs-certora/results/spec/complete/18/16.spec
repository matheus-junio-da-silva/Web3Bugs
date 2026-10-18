// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 238-257
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-10
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    safeBatchTransferFrom(address, address, uint256[], uint256[], bytes)
}

rule cannotTransferMoreBatch(env e){
    address from; address to; uint256[] ids; uint256[] amounts; bytes data;
    uint256 idToCheck1; uint256 amountToCheck1;
    uint256 idToCheck2; uint256 amountToCheck2;
    uint256 idToCheck3; uint256 amountToCheck3;

    uint256 balanceBefore1 = balanceOf(from, idToCheck1);
    uint256 balanceBefore2 = balanceOf(from, idToCheck2);
    uint256 balanceBefore3 = balanceOf(from, idToCheck3);

    require ids.length == 3;        
    require amounts.length == 3;    
    require ids[0] == idToCheck1; require amounts[0] == amountToCheck1;
    require ids[1] == idToCheck2; require amounts[1] == amountToCheck2;
    require ids[2] == idToCheck3; require amounts[2] == amountToCheck3;

    safeBatchTransferFrom@withrevert(e, from, to, ids, amounts, data);

    assert (amountToCheck1 > balanceBefore1 || amountToCheck2 > balanceBefore2 || amountToCheck3 > balanceBefore3) => lastReverted, "Achtung! Scammer!";
}
