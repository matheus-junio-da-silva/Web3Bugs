// Project 13 Notional Finance V2; historical CVL retained verbatim.
// Property: withdrawsMustDecreaseCashBalance; instance 9; Status: incomplete.
// Original property: certora/accountContext/Balances.spec:12-16
// Included original CVL ranges: certora/accountContext/Balances.spec:12-16
// CVL1 era; no modernization or replacement assumptions.

rule withdrawsMustDecreaseCashBalance {
    env e;
    int256 cashBalance = getCashBalance(account);

}
