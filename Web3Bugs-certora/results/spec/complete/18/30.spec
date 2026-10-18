// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 521-529
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-11
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    mint(address, uint256, uint256, bytes)
}

rule cantMintMoreSingle(env e){
    address to; uint256 id; uint256 amount; bytes data;

    require to_mathint(balanceOf(to, id) + amount) > max_uint256;

    mint@withrevert(e, to, id, amount, data);
    
    assert lastReverted, "Don't be too greedy!";
}
