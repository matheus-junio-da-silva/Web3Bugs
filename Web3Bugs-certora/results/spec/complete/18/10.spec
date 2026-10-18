// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 108-112
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:3-3
methods {
    balanceOf(address, uint256) returns(uint256) envfree
}

rule balanceOfRevertCases(env e){
    address account; uint256 id;
    balanceOf@withrevert(account, id);
    assert lastReverted => account == 0, "Houston, we have a problem";
}
