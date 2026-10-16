// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: noRedeemOutOfUnstakeWindow
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:10-10; certora/specs/base.spec:20-20; certora/specs/base.spec:21-21; certora/specs/base.spec:23-23; certora/specs/base.spec:42-42; certora/specs/base.spec:48-48; certora/specs/allProps.spec:268-279

methods {
    UNSTAKE_WINDOW() returns (uint256) envfree
    stakersCooldowns(address) returns (uint40, uint216) envfree
    getCooldownSeconds() returns (uint256) envfree
    inPostSlashingPeriod() returns (bool) envfree
    redeem(address,uint256)
}
rule noRedeemOutOfUnstakeWindow(address to, uint256 amount){
    env e;

    uint72 cooldown;
    cooldown, _ = stakersCooldowns(e.msg.sender);
    redeem(e, to, amount);

    // assert cooldown is inside the unstake window or it's a post slashing period
    assert inPostSlashingPeriod() ||
     (e.block.timestamp > cooldown + getCooldownSeconds() &&
        e.block.timestamp - (cooldown + getCooldownSeconds()) <= UNSTAKE_WINDOW());
}
