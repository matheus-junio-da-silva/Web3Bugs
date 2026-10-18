// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/Initializable.spec lines 40-48
// Target: Initializable / multi-inheritance verification harness (historical name not stated)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: Initializable.spec:5-14
methods {
    initializing() returns bool envfree
    a() returns uint256 envfree
}

invariant notInitializing()
    !initializing()


//////////////////////////////////////////////////////////////////////////////
////////////////////////////////// Rules /////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

/// @description An initializeable contract with a function that inherits the initializer modifier must be initializable only once"

