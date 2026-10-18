// Project 10 — literal active senderIsAlwaysCleanedUp from contracts/10/specs/proxy.spec:393-401
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


methods {
    getSender() returns (address) envfree
}

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule senderIsAlwaysCleanedUp(method f) {
    address before = getSender();

    arbitrary(f);

    address after = getSender();

    assert before == 0 => after == 0;
}
