// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/Initializable.spec lines 88-95
// Target: Initializable / multi-inheritance verification harness (historical name not stated)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: Initializable.spec:4-4
methods {
    initialized() returns uint8 envfree
}

rule increasingInitialized(method f) {
    env e; calldataarg args;

    uint8 initBefore = initialized();
    f(e, args);
    uint8 initAfter = initialized();
    assert initBefore <= initAfter, "_initialized must only increase";
}
