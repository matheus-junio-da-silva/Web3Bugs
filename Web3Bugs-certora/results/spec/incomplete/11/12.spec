// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: inverseOfDepositAndWithdraw (original lines 419-438)
// Original CVL dependency source lines: 14,16,17,20,24,26,27,28;32-33;35-36;419-438
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    balanceOf(address) returns uint256 envfree
    beneficiaryOf(address) returns address envfree
    deposit(address)
    ownerOf(address) returns address envfree
    unbondedValue(address) returns uint256 envfree
    withdraw(uint256, address)
}

definition MAXINT() returns uint256 =
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

definition safeAdd(uint256 x, uint256 y) returns bool =
        x + y >= y && x + y >=x && x+y <= MAXINT();

rule inverseOfDepositAndWithdraw(address operator, address owner, address beneficiary, uint256 x) {
    require (ownerOf(operator) == owner && beneficiaryOf(operator) == beneficiary);
    require (beneficiary != currentContract);
    uint256 u = unbondedValue(operator);
    uint256 b = balanceOf(currentContract);
    // successful deposit
    env eDeposit;
    require eDeposit.msg.value == x;
    require (eDeposit.msg.sender != currentContract);
    deposit(eDeposit, operator);
    env eWithdraw;
    require eWithdraw.msg.sender == operator || eWithdraw.msg.sender == owner;
    require eWithdraw.msg.value == 0;
    require _hasDelegationLockPassed(eWithdraw, operator);
    require safeAdd(balanceOf(beneficiary), x);
    invoke withdraw(eWithdraw, x, operator);
    bool success = !lastReverted;
    // verify that succeeded and the the value is as expected
    assert success &&  u  == unbondedValue(operator) && b == balanceOf(currentContract);
}
