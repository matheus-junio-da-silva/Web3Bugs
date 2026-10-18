// Project 10; source contracts/10/specs/proxy.spec; exact original rule cubeCounterIsAlwaysCleanedUp.
// Target-specific catalog context: HSushiSwap; report check #29, physical PDF page 28.
// Historical driver: contracts/10/specs/scripts/runHSushiSwap.sh; no independent historical proof is asserted.
// Selected CVL dependencies come from generic Example 19 and original source lines 11;12;331-332;403-412;552-556;580-584.

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
