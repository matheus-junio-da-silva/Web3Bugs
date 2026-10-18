// Project 10 — literal active notTouchingCache from contracts/10/specs/proxy.spec:343-347
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.

methods {
    cache(bytes32) returns (bytes32) envfree
}


ghost cacheTouched() returns bool;

hook Sstore cache[KEY bytes32 k] bytes32 value (bytes32 old_value) STORAGE {
    havoc cacheTouched assuming cacheTouched@new() == cacheTouched@old() || (value != old_value);
}

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule notTouchingCache(method f) {
    require !cacheTouched();
    arbitrary(f);
    assert !cacheTouched(), "Cache was touched maybe temporarily";
}
