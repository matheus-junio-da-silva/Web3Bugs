// Project 10 — literal active nonExecutableWithUninitializedSender from contracts/10/specs/proxy.spec:448-458
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


using ProxyHarness as proxy // may also be the same as currentContract

methods {
    getSender() returns (address) envfree
    isHandler() returns (bool) envfree
}

rule nonExecutableWithUninitializedSender(method f) {
    require !isHandler();
    require !f.isView; // only non-view functions, that may modify the state, are interesting.
    require getSender() == 0; // no sender initialized;

    env e;
    calldataarg arg;
    f@withrevert(e, arg);
    assert (f.selector != proxy.batchExec(address[],bytes32[],bytes[]).selector/* && f.selector != certorafallback_0().selector*/ /* TODO */)
        => lastReverted, "method invocation did not revert despite being called without a set sender";
}
