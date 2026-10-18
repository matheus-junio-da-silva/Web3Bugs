// Project 10 — literal active sanity from contracts/10/specs/proxy.spec:351-354
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule sanity(method f) {
    arbitrary(f);
    assert false;
}
