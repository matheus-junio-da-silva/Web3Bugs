// Project 13 Notional Finance V2; historical CVL retained verbatim.
// Property: sanity; instance 1; Status: incomplete.
// Original property: certora/accountContext/AccountPortfolio.spec:63-68
// Included original CVL ranges: certora/accountContext/AccountPortfolio.spec:63-68
// CVL1 era; no modernization or replacement assumptions.

rule sanity(method f) {
    env e;
    calldataarg args;
    f(e,args);
    assert false;
}
