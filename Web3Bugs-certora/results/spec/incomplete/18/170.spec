// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/TimelockController.spec lines 155-164
// Target: TimelockController
// Exact selected property body is copied literally; original CVL syntax is not modernized.

// Original CVL declaration: TimelockController.spec:5-5
methods {
    _minDelay() returns(uint256) envfree
}

rule minDelayOnlyChange(method f, env e){
    uint256 delayBefore = _minDelay();    

    calldataarg args;
    f(e, args);

    uint256 delayAfter = _minDelay();

    assert delayBefore != delayAfter => e.msg.sender == currentContract, "You cannot change your destiny! Only I can!";
}
