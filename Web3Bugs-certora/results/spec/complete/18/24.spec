// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 403-416
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:2-10
methods {
    isApprovedForAll(address, address) returns(bool) envfree
    safeBatchTransferFrom(address, address, uint256[], uint256[], bytes)
}

rule noTransferBatchEffectOnApproval(env e){
    address from; address to;
    address owner; address operator;
    uint256[] ids; uint256[] amounts;
    bytes data;

    bool approveBefore = isApprovedForAll(owner, operator);

    safeBatchTransferFrom(e, from, to, ids, amounts, data);

    bool approveAfter = isApprovedForAll(owner, operator);

    assert approveBefore == approveAfter, "Something was effected";
}
