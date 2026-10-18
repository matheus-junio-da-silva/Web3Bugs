// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 710-728
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-14
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    burnBatch(address, uint256[], uint256[])
}

rule cantBurnMoreBatch(env e){
    address from;
    uint256 id1; uint256 id2; uint256 id3; 
    uint256 amount1; uint256 amount2; uint256 amount3;
    uint256[] ids; uint256[] amounts;

    require ids.length == 3; 

    require ids[0] == id1; require ids[1] == id2; require ids[2] == id3;
    require amounts[0] == amount1; require amounts[1] == amount2; require amounts[2] == amount3;

    require to_mathint(balanceOf(from, id1) - amount1) < 0 
                || to_mathint(balanceOf(from, id2) - amount2) < 0 
                || to_mathint(balanceOf(from, id3) - amount3) < 0 ;

    burnBatch@withrevert(e, from, ids, amounts);
    
    assert lastReverted, "Don't be too greedy!";
}
