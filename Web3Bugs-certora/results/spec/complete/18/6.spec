// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 41-51
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:2-8
methods {
    isApprovedForAll(address, address) returns(bool) envfree
    setApprovalForAll(address, bool)
}

rule onlyOwnerCanApprove(env e){
    address owner; address operator; bool approved;

    bool aprovalBefore = isApprovedForAll(owner, operator);

    setApprovalForAll(e, operator, approved);

    bool aprovalAfter = isApprovedForAll(owner, operator);

    assert aprovalBefore != aprovalAfter => owner == e.msg.sender, "There should be only one owner";
}
