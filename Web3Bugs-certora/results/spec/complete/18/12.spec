// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 140-157
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-9
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    safeTransferFrom(address, address, uint256, uint256, bytes)
}

rule transferAdditivity(env e){
    address from; address to; uint256 id; bytes data;
    uint256 amount; uint256 amount1; uint256 amount2;
    require amount == amount1 + amount2;

    storage initialStorage = lastStorage;

    safeTransferFrom(e, from, to, id, amount, data);

    uint256 balanceAfterSingleTransaction = balanceOf(to, id);

    safeTransferFrom(e, from, to, id, amount1, data) at initialStorage;
    safeTransferFrom(e, from, to, id, amount2, data);

    uint256 balanceAfterDoubleTransaction = balanceOf(to, id);

    assert balanceAfterSingleTransaction == balanceAfterDoubleTransaction, "Not additive";
}
