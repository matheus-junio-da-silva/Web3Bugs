// Project 13 — historical Notional Finance V2; original property is verbatim.
// Property: sanity; instance 37; Status: incomplete.
// Original property: certora/asset/LiquidityCurve.spec:264-269
// Included original CVL ranges: certora/asset/LiquidityCurve.spec:264-269
// No migration to CVL2.

rule sanity(method f) {
    env e;
    calldataarg args;
    f(e,args);
    assert false;
}
