// Project 10 — literal active haltingIsReversible from contracts/10/specs/registry.spec:104-119
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


methods {
    owner() returns (address) envfree
}

function callArbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule haltingIsReversible(method f) {
    require owner() != 0;
    env e;
    halt(e);

    // call some function for covering more cases
    require f.selector != unhalt().selector;
    callArbitrary(f);

    env e2;
    require e2.msg.value == 0;
    require e2.msg.sender == e.msg.sender;
    assert e.msg.sender != 0, "Cannot send transactions from 0 address";
    unhalt@withrevert(e2);
    assert !lastReverted, "Unhalting should succeed";
}
