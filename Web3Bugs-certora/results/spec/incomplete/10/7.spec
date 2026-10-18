// Project 10 — literal active unregisterHandlerIsPermanent2 from contracts/10/specs/registry.spec:72-78
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

rule unregisterHandlerIsPermanent2(method f, address handler) {
    require handlers(handler) == deprecated();

    callArbitrary(f);

    assert handlers(handler) == deprecated(), "unexpected handler info after unregister";
}
