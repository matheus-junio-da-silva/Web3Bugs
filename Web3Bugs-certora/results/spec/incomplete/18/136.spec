// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/Initializable.spec lines 49-55
// Target: Initializable / multi-inheritance verification harness (historical name not stated)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: Initializable.spec:2-16
methods {
    initialize(uint256, uint256, uint256) envfree
    initialized() returns uint8 envfree
    a() returns uint256 envfree
    b() returns uint256 envfree
    val() returns uint256 envfree
}

// Original CVL declaration: Initializable.spec:26-26
definition isInitialized() returns bool = initialized() > 0;

rule initOnce() {
    uint256 val; uint256 a; uint256 b;

    require isInitialized();
    initialize@withrevert(val, a, b);
    assert lastReverted, "contract must only be initialized once";
}
