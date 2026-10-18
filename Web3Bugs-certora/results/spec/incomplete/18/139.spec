// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/Initializable.spec lines 68-74
// Target: Initializable / flat verification harness (historical name not stated)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: Initializable.spec:2-16
methods {
    initialize(uint256, uint256, uint256) envfree
    initialized() returns uint8 envfree
    a() returns uint256 envfree
    b() returns uint256 envfree
    val() returns uint256 envfree
}

// Original CVL declaration: Initializable.spec:28-28
definition isInitializedOnce() returns bool = initialized() == 1;

rule initalizeEffects {
    uint256 val; uint256 a; uint256 b;

    initialize(val, a, b);

    assert isInitializedOnce(), "initialize() must set _initialized to 1";
}
