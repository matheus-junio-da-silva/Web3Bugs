// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 427-443
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-11
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    mint(address, uint256, uint256, bytes)
}

rule mintAdditivity(env e){
    address to; uint256 id; uint256 amount; uint256 amount1; uint256 amount2; bytes data;
    require amount == amount1 + amount2;

    storage initialStorage = lastStorage;

    mint(e, to, id, amount, data);

    uint256 balanceAfterSingleTransaction = balanceOf(to, id);

    mint(e, to, id, amount1, data) at initialStorage;
    mint(e, to, id, amount2, data);

    uint256 balanceAfterDoubleTransaction = balanceOf(to, id);

    assert balanceAfterSingleTransaction == balanceAfterDoubleTransaction, "Not additive";
}
