// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/Initializable.spec lines 109-117
// Target: Initializable / multi-inheritance verification harness (historical name not stated)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: Initializable.spec:3-16
methods {
    reinitialize(uint256, uint256, uint256, uint8) envfree
    initialized() returns uint8 envfree
    initializing() returns bool envfree
    a() returns uint256 envfree
    b() returns uint256 envfree
    val() returns uint256 envfree
}

// Original CVL declaration: Initializable.spec:40-48
invariant notInitializing()
    !initializing()


//////////////////////////////////////////////////////////////////////////////
////////////////////////////////// Rules /////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

/// @description An initializeable contract with a function that inherits the initializer modifier must be initializable only once"

rule reinitializeLiveness {
    uint256 val; uint8 n; uint256 a; uint256 b;

    requireInvariant notInitializing();
    uint8 initVal = initialized();
    reinitialize@withrevert(val, a, b, n);

    assert n > initVal => !lastReverted, "reinitialize(n) call must succeed if n was greater than _initialized";
}
