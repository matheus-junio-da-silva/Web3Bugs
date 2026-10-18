// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 162-177
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-9
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    safeTransferFrom(address, address, uint256, uint256, bytes)
}

rule transferCorrectness(env e){
    address from; address to; uint256 id; uint256 amount; bytes data;

    require to != from;

    uint256 fromBalanceBefore = balanceOf(from, id);
    uint256 toBalanceBefore = balanceOf(to, id);

    safeTransferFrom(e, from, to, id, amount, data);

    uint256 fromBalanceAfter = balanceOf(from, id);
    uint256 toBalanceAfter = balanceOf(to, id);

    assert fromBalanceBefore == fromBalanceAfter + amount, "Something wet wrong";
    assert toBalanceBefore == toBalanceAfter - amount, "Something wet wrong";
}
