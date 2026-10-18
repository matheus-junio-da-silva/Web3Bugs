// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 558-569
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-11
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    mint(address, uint256, uint256, bytes)
}

rule cantMintOtherBalances(env e){
    address to; uint256 id; uint256 amount; bytes data;
    address other;

    uint256 otherBalanceBefore = balanceOf(other, id);

    mint(e, to, id, amount, data);

    uint256 otherBalanceAfter = balanceOf(other, id);
    
    assert other != to => otherBalanceBefore == otherBalanceAfter, "I like to see your money disappearing";
}
