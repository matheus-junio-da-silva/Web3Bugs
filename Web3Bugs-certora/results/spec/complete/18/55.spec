// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Pausable.spec lines 51-59
// Target: ERC1155PausableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Pausable.spec:3-3
methods {
    paused() returns bool envfree
}

rule unpauseMethodUnpausesContract {
    require paused();

    env e;
    unpause(e);

    assert !paused(), 
        "Calling unpause must unpause a paused contract";
}
