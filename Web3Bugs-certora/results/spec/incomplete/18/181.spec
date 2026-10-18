// HISTORICAL CERTORA CVL — Project 18
// Source: contracts/18/specs/sanity.spec lines 10-15
// Target: UNRESOLVED (generic method probe)
// Exact selected property body is copied literally; original CVL syntax is not modernized.



rule sanity(method f) {
    env e;
    calldataarg arg;
    f(e, arg);
    assert false;
}
