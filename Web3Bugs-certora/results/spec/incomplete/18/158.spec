// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/Initializable.spec lines 154-159
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

rule inheritanceCheck {
    uint256 val; uint8 n; uint256 a; uint256 b;

    reinitialize(val, a, b, n);
    assert val() == val && a() == a && b() == b, "all child contract values must be initialized";
}
