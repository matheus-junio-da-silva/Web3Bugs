// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 226-233
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-9
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    safeTransferFrom(address, address, uint256, uint256, bytes)
}

rule cannotTransferMoreSingle(env e){
    address from; address to; uint256 id; uint256 amount; bytes data;
    uint256 balanceBefore = balanceOf(from, id);

    safeTransferFrom@withrevert(e, from, to, id, amount, data);

    assert amount > balanceBefore => lastReverted, "Achtung! Scammer!";
}
