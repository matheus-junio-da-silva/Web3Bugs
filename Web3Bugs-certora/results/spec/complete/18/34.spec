// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 605-621
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-13
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    burn(address, uint256, uint256)
}

rule burnAdditivity(env e){
    address from; uint256 id; uint256 amount; uint256 amount1; uint256 amount2;
    require amount == amount1 + amount2;

    storage initialStorage = lastStorage;

    burn(e, from, id, amount);

    uint256 balanceAfterSingleTransaction = balanceOf(from, id);

    burn(e, from, id, amount1) at initialStorage;
    burn(e, from, id, amount2);

    uint256 balanceAfterDoubleTransaction = balanceOf(from, id);

    assert balanceAfterSingleTransaction == balanceAfterDoubleTransaction, "Not additive";
}
