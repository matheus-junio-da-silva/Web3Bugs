// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Pausable.spec lines 73-81
// Target: ERC1155PausableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Pausable.spec:3-3
methods {
    paused() returns bool envfree
}

rule cannotUnpauseWhileUnpaused {
    require !paused();

    env e;
    unpause@withrevert(e);

    assert lastReverted, 
        "A call to unpause when already unpaused must revert";
}
