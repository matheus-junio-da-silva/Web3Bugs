// Project 10; source contracts/10/specs/proxy.spec; exact original rule cacheIsAlwaysCleanedUp.
// Target-specific catalog context: HStakingRewardsAdapter; report check #30, physical PDF page 29.
// Historical driver: contracts/10/specs/scripts/runHStakingRewardsAdapter.sh; no independent historical proof is asserted.
// Selected CVL dependencies come from generic Example 20 and original source lines 10;15;16;414-424;580-584.

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
