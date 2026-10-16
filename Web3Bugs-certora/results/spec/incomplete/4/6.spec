// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: noEntryUntilSlashingSettled
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:23-23; certora/specs/base.spec:41-41; certora/specs/base.spec:48-48; certora/specs/allProps.spec:217-224

methods {
    inPostSlashingPeriod() returns (bool) envfree
    stake(address,uint256)
}
rule noEntryUntilSlashingSettled(uint256 amount){
    env e;

    stake@withrevert(e, e.msg.sender, amount);

    bool reverted = lastReverted;
    assert inPostSlashingPeriod() => reverted;
}
