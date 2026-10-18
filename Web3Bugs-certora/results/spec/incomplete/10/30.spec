// Historical CVL property, Project 10, contracts/10/specs/hbalancer.spec:65-73; helper contracts/10/specs/hbalancer.spec:75-79
// Only available dependency declarations; no historic signature edits and no CVL migration.

using Summary as summaryInstance // general summary for DeFi protocols

methods {
    summaryInstance.lenDelegated() returns (uint256) envfree
    summaryInstance.checkDelegated(address) returns (bool) envfree
    execute(address,bytes) returns (bytes32) => DISPATCHER(true) // should modify/havoc erc20 balances. The returns part is super important for soundness!
    BACTIONS() returns (address) envfree
}

function arbitrary(method f) {
    env e__;
    calldataarg arg__;
    f(e__, arg__);
}

rule executeDelegatesOnlyToAllowedAddresses(method f) {
    require summaryInstance.lenDelegated() == 0;

    arbitrary(f);

    uint pushed = summaryInstance.lenDelegated();
    assert pushed <= 3, "not expected to call execute more than 3 times";
    assert summaryInstance.checkDelegated(BACTIONS()), "not all delegated are allowed";
}
