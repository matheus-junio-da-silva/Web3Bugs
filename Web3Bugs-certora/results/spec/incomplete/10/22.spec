// Project 10 — literal active nonExecutableWhenHalted from contracts/10/specs/proxy.spec:437-446
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


using Registry as registry

methods {
    isHandler() returns (bool) envfree
    registry.fHalt() returns (bool) envfree
}

rule nonExecutableWhenHalted(method f) {
    require !isHandler();
    require !f.isView; // only non-view functions, that may modify the state, are interesting.
    require registry.fHalt(); // system is halted

    env e;
    calldataarg arg;
    f@withrevert(e, arg);
    assert lastReverted, "method invocation did not revert despite being called in a halted state";
}
