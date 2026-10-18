// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Pausable.spec lines 40-48
// Target: ERC1155PausableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Pausable.spec:3-3
methods {
    paused() returns bool envfree
}

rule pauseMethodPausesContract {
    require !paused();

    env e;
    pause(e);

    assert paused(), 
        "Calling pause must pause an unpaused contract";
}
