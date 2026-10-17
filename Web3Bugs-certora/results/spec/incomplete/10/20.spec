// Project 10 — literal active cacheIsAlwaysCleanedUp from contracts/10/specs/proxy.spec:414-424
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


methods {
    cache(bytes32) returns (bytes32) envfree
    MSG_SENDER_KEY() returns (bytes32) envfree
    CUBE_COUNTER_KEY() returns (bytes32) envfree
}

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule cacheIsAlwaysCleanedUp(bytes32 key, method f) {
    // not cube counter or sender which take part in initialization
    require key != MSG_SENDER_KEY() && key != CUBE_COUNTER_KEY();
    bytes32 before = cache(key);

    arbitrary(f);

    bytes32 after = cache(key);

    assert before == 0 => after == 0;
}
