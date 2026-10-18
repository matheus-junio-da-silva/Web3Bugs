// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 473-483
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-11
methods {
    balanceOf(address, uint256) returns(uint256) envfree
    mint(address, uint256, uint256, bytes)
}

rule mintCorrectWork(env e){
    address to; uint256 id; uint256 amount; bytes data;

    uint256 otherBalanceBefore = balanceOf(to, id);

    mint(e, to, id, amount, data);

    uint256 otherBalanceAfter = balanceOf(to, id);
    
    assert otherBalanceBefore == otherBalanceAfter - amount, "Something is wrong";
}
