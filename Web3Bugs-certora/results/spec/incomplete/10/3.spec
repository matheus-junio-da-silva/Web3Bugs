// Project 10 — literal active changesCaller from contracts/10/specs/registry.spec:38-44
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


methods {
    callers(address) returns (bytes32) envfree
}

function callerTransition(address caller, bytes32 before, bytes32 after, method f) {
    require before == callers(caller);
    callArbitrary(f);
    require after == callers(caller);
}

function callArbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule changesCaller(method f, address caller) {
    bytes32 _regState;
    bytes32 regState_;
    callerTransition(caller, _regState, regState_, f);
    assert (f.selector != registerCaller(address,bytes32).selector && f.selector != unregisterCaller(address).selector) 
        => _regState == regState_, "method unexpectedly changes caller info";
}
