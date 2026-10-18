// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/Initializable.spec lines 58-64
// Target: Initializable / multi-inheritance verification harness (historical name not stated)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: Initializable.spec:3-16
methods {
    reinitialize(uint256, uint256, uint256, uint8) envfree
    initialized() returns uint8 envfree
    a() returns uint256 envfree
    b() returns uint256 envfree
    val() returns uint256 envfree
}

// Original CVL declaration: Initializable.spec:28-28
definition isInitializedOnce() returns bool = initialized() == 1;

rule reinitializeEffects {
    uint256 val; uint256 a; uint256 b;

    reinitialize(val, a, b, 1);

    assert isInitializedOnce(), "reinitialize(1) must set _initialized to 1";
}
