// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/Initializable.spec lines 130-135
// Target: Initializable / multi-inheritance verification harness (historical name not stated)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: Initializable.spec:4-9
methods {
    initialized() returns uint8 envfree
    returnsVN(uint8) returns uint256 envfree
}

rule reinitVersionCheckParent {
    uint8 n;

    returnsVN(n);
    assert initialized() == n, "parent contract's version n functions must only be callable in version n";
}
