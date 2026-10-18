// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 697-705
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-13
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    burn(address, uint256, uint256)
}

rule cantBurnMoreSingle(env e){
    address from; uint256 id; uint256 amount;

    require to_mathint(balanceOf(from, id) - amount) < 0;

    burn@withrevert(e, from, id, amount);
    
    assert lastReverted, "Don't be too greedy!";
}
