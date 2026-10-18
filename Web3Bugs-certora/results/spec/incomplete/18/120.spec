// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/GovernorCountingSimple.spec lines 194-205
// Target: GovernorCountingSimple (historical governor harness)
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: GovernorCountingSimple.spec:6-11
methods {
    quorum(uint256) returns uint256
    quorumNumerator() returns uint256
    getExecutor() returns address
}

rule privilegedOnlyNumerator(method f, uint256 newQuorumNumerator){
    env e;
    calldataarg arg;
    uint256 quorumNumBefore = quorumNumerator(e);

    f(e, arg);

    uint256 quorumNumAfter = quorumNumerator(e);
    address executorCheck = getExecutor(e);

    assert quorumNumBefore != quorumNumAfter => e.msg.sender == executorCheck, "non privileged user changed quorum numerator";
}
