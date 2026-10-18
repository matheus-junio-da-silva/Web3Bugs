// Project 10 — literal active deprecatesHandler from contracts/10/specs/registry.spec:30-36
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

definition deprecated() returns bytes32 = 0x6465707265636174656400000000000000000000000000000000000000000000;

function callArbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule deprecatesHandler(method f, address handler) {
    bytes32 _regState;
    bytes32 regState_;
    handlerTransition(handler, _regState, regState_, f);
    assert (f.selector != unregister(address).selector) 
        => _regState != deprecated() /* non deprecated */ => regState_ != deprecated(), "method unexpectedly deprecates handler";
}
