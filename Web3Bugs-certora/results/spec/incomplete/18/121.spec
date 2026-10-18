// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorCountingSimple.spec lines 207-217
// Target: GovernorCountingSimple (historical governor harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorCountingSimple.spec:13-13
methods {
    timelock() returns address
}

rule privilegedOnlyTimelock(method f, uint256 newQuorumNumerator){
    env e;
    calldataarg arg;
    uint256 timelockBefore = timelock(e);

    f(e, arg);

    uint256 timelockAfter = timelock(e);

    assert timelockBefore != timelockAfter => e.msg.sender == timelockBefore, "non privileged user changed timelock";
}
