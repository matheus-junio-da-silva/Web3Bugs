// Project 10 — literal active nonExecutableWhenProxyIsBanned from contracts/10/specs/proxy.spec:426-435
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


using Registry as registry
using ProxyHarness as proxy // may also be the same as currentContract

methods {
    isHandler() returns (bool) envfree
    registry.bannedAgents(address) returns (uint256) envfree
}

rule nonExecutableWhenProxyIsBanned(method f) {
    require !isHandler();
    require !f.isView; // only non-view functions, that may modify the state, are interesting.
    env e;
    require registry.bannedAgents(currentContract) == 1; // proxy contract is banned

    calldataarg arg;
    f@withrevert(e, arg);
    assert lastReverted, "method invocation did not revert despite the contract has been banned in registry";
}
