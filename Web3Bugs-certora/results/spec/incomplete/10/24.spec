// Project 10 — literal active nonExecutableWithInitializedSender from contracts/10/specs/proxy.spec:461-473
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


using Registry as registry
using ProxyHarness as proxy // may also be the same as currentContract

methods {
    getSender() returns (address) envfree
    isHandler() returns (bool) envfree
}

rule nonExecutableWithInitializedSender(method f) {
    require !isHandler();
    require !f.isView; // only non-view functions, that may modify the state, are interesting.
    require getSender() != 0; // sender is initialized

    env e;
    bool isGoodCaller = registry.isValidCaller(e, e.msg.sender);
    calldataarg arg;
    f@withrevert(e, arg);
    assert (f.isFallback && !isGoodCaller) => lastReverted; // only valid callers should execute in fallback successfully (would violate since certora prover cannot distinguish between receive and fallback for now)
    assert (f.selector == execs(address[],bytes32[],bytes[]).selector && e.msg.sender != currentContract) => lastReverted; // `execs` is allowed to be called by proxy itself after initialized
    assert (!f.isFallback && f.selector != execs(address[],bytes32[],bytes[]).selector) => lastReverted; // all non-view functions other than above ones should revert if sender is already initialized
}
