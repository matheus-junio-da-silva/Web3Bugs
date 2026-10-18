// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 262-276
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-9
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    safeTransferFrom(address, address, uint256, uint256, bytes)
}

rule transferBalanceReduceEffect(env e){
    address from; address to; address other;
    uint256 id; uint256 amount; 
    bytes data;

    require other != to;

    uint256 otherBalanceBefore = balanceOf(other, id);

    safeTransferFrom(e, from, to, id, amount, data);

    uint256 otherBalanceAfter = balanceOf(other, id);

    assert from != other => otherBalanceBefore == otherBalanceAfter, "Don't touch my money!";
}
