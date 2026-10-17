// Project 10 — literal active cubeCounterIsAlwaysCleanedUp from contracts/10/specs/proxy.spec:403-412
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


methods {
    getSender() returns (address) envfree
    getCubeCounter() returns (uint256) envfree
}

invariant cubeCounterGreaterThan0IffSenderInitialized() getCubeCounter() > 0 <=> getSender() != 0 {
    preserved {
        require getCubeCounter() < MAX_UINT256();
    }
}

definition MAX_UINT256() returns uint256 = 115792089237316195423570985008687907853269984665640564039457584007913129639935
    ;

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule cubeCounterIsAlwaysCleanedUp(method f) {
    requireInvariant cubeCounterGreaterThan0IffSenderInitialized();
    uint256 before = getCubeCounter();

    arbitrary(f);

    uint256 after = getCubeCounter();

    assert before == 0 => after == 0;
}
