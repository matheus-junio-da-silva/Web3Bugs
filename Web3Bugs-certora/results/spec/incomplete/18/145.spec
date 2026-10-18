// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/Initializable.spec lines 98-106
// Target: Initializable / flat verification harness (historical name not stated)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: Initializable.spec:3-16
methods {
    reinitialize(uint256, uint256, uint256, uint8) envfree
    initialized() returns uint8 envfree
    a() returns uint256 envfree
    b() returns uint256 envfree
    val() returns uint256 envfree
}

rule reinitializeIncreasesInit {
    uint256 val; uint8 n; uint256 a; uint256 b;

    uint8 initBefore = initialized();
    reinitialize(val, a, b, n);
    uint8 initAfter = initialized();

    assert initAfter > initBefore, "calling reinitialize must increase _initialized";
}
