// Project 10 — literal active unregisterCallerIsPermanent from contracts/10/specs/registry.spec:63-70
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


methods {
    callers(address) returns (bytes32) envfree
}

definition deprecated() returns bytes32 = 0x6465707265636174656400000000000000000000000000000000000000000000;

function callArbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule unregisterCallerIsPermanent(method f, address caller) {
    env e;
    unregisterCaller(e, caller);

    callArbitrary(f);

    assert callers(caller) == deprecated(), "unexpected caller info after unregister";
}
