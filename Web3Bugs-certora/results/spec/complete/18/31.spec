// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 534-553
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-12
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    mintBatch(address, uint256[], uint256[], bytes)
}

rule cantMintMoreBatch(env e){
    address to; bytes data;
    uint256 id1; uint256 id2; uint256 id3; 
    uint256 amount1; uint256 amount2; uint256 amount3;
    uint256[] ids; uint256[] amounts;

    require ids.length == 3; 
    require amounts.length == 3;

    require ids[0] == id1; require ids[1] == id2; require ids[2] == id3;
    require amounts[0] == amount1; require amounts[1] == amount2; require amounts[2] == amount3;

    require to_mathint(balanceOf(to, id1) + amount1) > max_uint256 
                || to_mathint(balanceOf(to, id2) + amount2) > max_uint256
                || to_mathint(balanceOf(to, id3) + amount3) > max_uint256;

    mintBatch@withrevert(e, to, ids, amounts, data);
    
    assert lastReverted, "Don't be too greedy!";
}
