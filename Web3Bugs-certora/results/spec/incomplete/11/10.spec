// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: additiveWithdraw (original lines 324-346)
// Original CVL dependency source lines: 14,16,17,24,26,27,28;32-33;324-346
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    balanceOf(address) returns uint256 envfree
    beneficiaryOf(address) returns address envfree
    ownerOf(address) returns address envfree
    unbondedValue(address) returns uint256 envfree
    withdraw(uint256, address)
}

definition MAXINT() returns uint256 =
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

rule additiveWithdraw(address operator, address owner, address beneficiary, uint256 x, uint y) {
    env e;
    require ownerOf(operator) == owner && beneficiaryOf(operator) == beneficiary;
    require beneficiary != currentContract;
    require x + y < MAXINT();
    require balanceOf(beneficiary) + x + y <= MAXINT();

    storage init_storage = lastStorage; // store the current state
    invoke withdraw(e, x, operator);
    bool successX = !lastReverted;
    invoke withdraw(e, y, operator);
    bool successY = !lastReverted;
    uint256 uScenario1 = unbondedValue(operator);
    uint256 bScenario1 = balanceOf(beneficiary);

    invoke withdraw(e, x + y, operator) at init_storage; // back to the initial state
    bool successXY = !lastReverted;
    uint256 uScenario2 = unbondedValue(operator);
    uint256 bScenario2 = balanceOf(beneficiary);
    assert (successX && successY) <=> successXY, "withdraw is not additive";
    assert successXY => (uScenario1 == uScenario2 && bScenario1 == bScenario2),
        "withdraw is not additive";
}
