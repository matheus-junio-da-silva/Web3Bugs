// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 65-76
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:2-8
methods {
    isApprovedForAll(address, address) returns(bool) envfree
    setApprovalForAll(address, bool)
}

rule onlyOneAllowanceChange(method f, env e) {
    address owner; address operator; address user; 
    bool approved;

    bool userApproveBefore = isApprovedForAll(owner, user);

    setApprovalForAll(e, operator, approved);

    bool userApproveAfter = isApprovedForAll(owner, user);

    assert userApproveBefore != userApproveAfter => (e.msg.sender == owner && operator == user), "Imposter!";
}
