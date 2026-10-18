// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155.spec lines 352-363
// Target: ERC1155Mock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155.spec:2-9
methods {
    isApprovedForAll(address, address) returns(bool) envfree
    safeTransferFrom(address, address, uint256, uint256, bytes)
}

rule noTransferForNotApproved(env e) {
    address from; address operator;
    address to; uint256 id; uint256 amount; bytes data;

    require from != e.msg.sender;

    bool approve = isApprovedForAll(from, e.msg.sender);

    safeTransferFrom@withrevert(e, from, to, id, amount, data);

    assert !approve => lastReverted, "You don't have king's approval!";
}   
