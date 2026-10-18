// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 26-36
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:2-8
methods {
    isApprovedForAll(address, address) returns(bool) envfree
    setApprovalForAll(address, bool)
}

rule unexpectedAllowanceChange(method f, env e) filtered { f -> f.selector != setApprovalForAll(address, bool).selector } {
    address account; address operator;
    bool approveBefore = isApprovedForAll(account, operator); 

    calldataarg args;
    f(e, args);

    bool approveAfter = isApprovedForAll(account, operator);

    assert approveBefore == approveAfter, "You couldn't get king's approval this way!";
}
