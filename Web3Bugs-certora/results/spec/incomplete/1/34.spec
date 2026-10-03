// Extracted from: contracts/1/specs/complexity.spec
// Property: whoChangedBalanceOf
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
    balanceOf(address)                    returns (uint256) => DISPATCHER(true)
}

rule whoChangedBalanceOf(method f, address u) {
    env eB;
    env eF;
    calldataarg args;
    uint256 before = balanceOf(eB, u);
    f(eF,args);
    assert balanceOf(eB, u) == before, "balanceOf changed";
}
