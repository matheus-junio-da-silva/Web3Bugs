// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/Initializable.spec lines 146-151
// Target: Initializable / multi-inheritance verification harness (historical name not stated)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: Initializable.spec:4-13
methods {
    initialized() returns uint8 envfree
    returnsBVN(uint8) returns uint256 envfree
}

rule reinitVersionCheckGrandchild {
    uint8 n;

    returnsBVN(n);
    assert initialized() == n, "gransdchild contract's version n functions must only be callable in version n";
}
