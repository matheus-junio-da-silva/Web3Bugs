// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 385-398
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:2-9
methods {
    isApprovedForAll(address, address) returns(bool) envfree
    safeTransferFrom(address, address, uint256, uint256, bytes)
}

rule noTransferEffectOnApproval(env e){
    address from; address to;
    address owner; address operator;
    uint256 id; uint256 amount; 
    bytes data;

    bool approveBefore = isApprovedForAll(owner, operator);

    safeTransferFrom(e, from, to, id, amount, data);

    bool approveAfter = isApprovedForAll(owner, operator);

    assert approveBefore == approveAfter, "Something was effected";
}
