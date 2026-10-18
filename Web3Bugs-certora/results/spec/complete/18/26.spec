// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 448-454
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:11-11
methods {
    mint(address, uint256, uint256, bytes)
}

rule mintRevertCases(env e){
    address to; uint256 id; uint256 amount; bytes data;

    mint@withrevert(e, to, id, amount, data);

    assert to == 0 => lastReverted, "Should revert";
}
