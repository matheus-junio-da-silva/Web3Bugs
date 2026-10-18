// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Pausable.spec lines 24-37
// Target: ERC1155PausableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Pausable.spec:3-3
methods {
    paused() returns bool envfree
}

rule transferMethodsRevertWhenPaused (method f)
filtered {
    f -> f.selector == safeTransferFrom(address,address,uint256,uint256,bytes).selector
      || f.selector == safeBatchTransferFrom(address,address,uint256[],uint256[],bytes).selector
}
{
    require paused();

    env e; calldataarg args;
    f@withrevert(e, args);

    assert lastReverted, 
        "Transfer methods must revert in a paused contract";
}
