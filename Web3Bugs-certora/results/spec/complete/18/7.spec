// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 56-60
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:2-2
methods {
    isApprovedForAll(address, address) returns(bool) envfree
}

rule approvalRevertCases(env e){
    address account; address operator;
    isApprovedForAll@withrevert(account, operator);
    assert !lastReverted, "Houston, we have a problem";
}
