// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 368-380
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:2-10
methods {
    isApprovedForAll(address, address) returns(bool) envfree
    safeBatchTransferFrom(address, address, uint256[], uint256[], bytes)
}

rule noTransferBatchForNotApproved(env e) {
    address from; address operator; address to; 
    bytes data;
    uint256[] ids; uint256[] amounts;

    require from != e.msg.sender;

    bool approve = isApprovedForAll(from, e.msg.sender);

    safeBatchTransferFrom@withrevert(e, from, to, ids, amounts, data);

    assert !approve => lastReverted, "You don't have king's approval!";
}
