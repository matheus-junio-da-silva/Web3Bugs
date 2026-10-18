// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/ERC1155Pausable.spec lines 97-105
// Target: ERC1155PausableMock
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: ERC1155Pausable.spec:3-3
methods {
    paused() returns bool envfree
}

rule whenPausedModifierCausesRevertIfUnpaused {
    require !paused();

    env e; calldataarg args;
    onlyWhenPausedMethod@withrevert(e, args);

    assert lastReverted, 
        "Functions with the whenPaused modifier must revert if the contract is not paused";
}
