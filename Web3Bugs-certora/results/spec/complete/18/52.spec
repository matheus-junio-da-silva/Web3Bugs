// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Pausable.spec lines 8-21
// Target: ERC1155PausableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Pausable.spec:2-3
methods {
    balanceOf(address, uint256) returns uint256 envfree
    paused() returns bool envfree
}

rule balancesUnchangedWhenPaused() {
    address user; uint256 token;
    uint256 balanceBefore = balanceOf(user, token);

    require paused();

    method f; calldataarg arg; env e;
    f(e, arg);

    uint256 balanceAfter = balanceOf(user, token);

    assert balanceBefore == balanceAfter, 
        "Token balance for a user must not change in a paused contract";
}
