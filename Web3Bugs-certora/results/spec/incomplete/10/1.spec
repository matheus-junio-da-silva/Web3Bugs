// Project 10 — literal active changesHandler from contracts/10/specs/registry.spec:22-28
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


methods {
    handlers(address) returns (bytes32) envfree
}

function handlerTransition(address handler, bytes32 before, bytes32 after, method f) {
    require before == handlers(handler);
    callArbitrary(f);
    require after == handlers(handler);
}

function callArbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule changesHandler(method f, address handler) {
    bytes32 _regState;
    bytes32 regState_;
    handlerTransition(handler, _regState, regState_, f);
    assert (f.selector != register(address,bytes32).selector && f.selector != unregister(address).selector) 
        => _regState == regState_, "method unexpectedly changes handler info";
}
