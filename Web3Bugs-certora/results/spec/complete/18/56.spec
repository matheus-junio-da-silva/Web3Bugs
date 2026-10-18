// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Pausable.spec lines 62-70
// Target: ERC1155PausableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Pausable.spec:3-3
methods {
    paused() returns bool envfree
}

rule cannotPauseWhilePaused {
    require paused();

    env e;
    pause@withrevert(e);

    assert lastReverted, 
        "A call to pause when already paused must revert";
}
