// Project 10 — literal active unregisterHandlerIsPermanent from contracts/10/specs/registry.spec:54-61
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


methods {
    handlers(address) returns (bytes32) envfree
}

definition deprecated() returns bytes32 = 0x6465707265636174656400000000000000000000000000000000000000000000;

function callArbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule unregisterHandlerIsPermanent(method f, address handler) {
    env e;
    unregister(e, handler);

    callArbitrary(f);

    assert handlers(handler) == deprecated(), "unexpected handler info after unregister";
}
