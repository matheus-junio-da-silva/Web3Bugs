// Project 10 — literal active banningIsReversible from contracts/10/specs/registry.spec:88-102
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

rule banningIsReversible(address agent, method f) {
    require owner() != 0;
    env e;
    ban(e, agent);

    // call some function for covering more cases
    require f.selector != unban(address).selector;
    callArbitrary(f);

    env e2;
    require e2.msg.value == 0;
    require e2.msg.sender == e.msg.sender;
    unban@withrevert(e2, agent);
    assert !lastReverted, "Unbanning should succeed";
}
