// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/Initializable.spec lines 77-85
// Target: Initializable / flat verification harness (historical name not stated)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: Initializable.spec:4-14
methods {
    initialized() returns uint8 envfree
    a() returns uint256 envfree
}

// Original CVL declaration: Initializable.spec:32-32
definition isDisabled() returns bool = initialized() == 255;

rule disabledStaysDisabled(method f) {
    env e; calldataarg args; 

    bool disabledBefore = isDisabled();
    f(e, args);
    bool disabledAfter = isDisabled();

    assert disabledBefore => disabledAfter, "a disabled initializer must stay disabled";
}
