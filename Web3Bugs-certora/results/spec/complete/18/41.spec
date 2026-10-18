// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 733-744
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-13
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    burn(address, uint256, uint256)
}

rule cantBurnOtherBalances(env e){
    address from; uint256 id; uint256 amount;
    address other;

    uint256 otherBalanceBefore = balanceOf(other, id);

    burn(e, from, id, amount);

    uint256 otherBalanceAfter = balanceOf(other, id);
    
    assert other != from => otherBalanceBefore == otherBalanceAfter, "I like to see your money disappearing";
}
