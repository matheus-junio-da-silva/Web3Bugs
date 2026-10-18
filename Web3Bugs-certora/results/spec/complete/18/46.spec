// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Burnable.spec lines 8-20
// Target: ERC1155BurnableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Burnable.spec:2-3
methods {
    balanceOf(address, uint256) returns uint256 envfree
    isApprovedForAll(address,address) returns bool envfree
}

rule onlyHolderOrApprovedCanReduceBalance(method f) 
{
    address holder; uint256 token; uint256 amount;
    uint256 balanceBefore = balanceOf(holder, token);

    env e; calldataarg args;
    f(e, args);

    uint256 balanceAfter = balanceOf(holder, token);

    assert balanceAfter < balanceBefore => e.msg.sender == holder || isApprovedForAll(holder, e.msg.sender), 
        "An account balance may only be reduced by the holder or a holder-approved agent";
}
