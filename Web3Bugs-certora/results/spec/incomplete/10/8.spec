// Project 10 — literal active unregisterCallerIsPermanent2 from contracts/10/specs/registry.spec:80-86
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

rule unregisterCallerIsPermanent2(method f, address caller) {
    require callers(caller) == deprecated();

    callArbitrary(f);

    assert callers(caller) == deprecated(), "unexpected caller info after unregister";
}
