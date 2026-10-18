// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 626-632
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:13-13
methods {
    burn(address, uint256, uint256)
}

rule burnRevertCases(env e){
    address from; uint256 id; uint256 amount;

    burn@withrevert(e, from, id, amount);

    assert from == 0 => lastReverted, "Should revert";
}
