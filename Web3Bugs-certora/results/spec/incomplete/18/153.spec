// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/Initializable.spec lines 138-143
// Target: Initializable / flat verification harness (historical name not stated)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: Initializable.spec:4-11
methods {
    initialized() returns uint8 envfree
    returnsAVN(uint8) returns uint256 envfree
}

rule reinitVersionCheckChild {
    uint8 n;

    returnsAVN(n);
    assert initialized() == n, "child contract's version n functions must only be callable in version n";
}
