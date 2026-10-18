// Project 13 Notional Finance V2; historical CVL retained verbatim.
// Property: depositsMustIncreaseCashBalance; instance 8; Status: incomplete.
// Original property: certora/accountContext/Balances.spec:3-10
// Included original CVL ranges: certora/accountContext/Balances.spec:3-10
// CVL1 era; no modernization or replacement assumptions.

rule depositsMustIncreaseCashBalance(address account, uint256 depositAmount) {
    env e;
    int256 cashBalance = getCashBalance(account);
    deposit(e, account, depositAmount);
    // check balanceOf ERC20 on account and contract

    assert cashBalance + depositAmount == getCashBalance(account);
}
