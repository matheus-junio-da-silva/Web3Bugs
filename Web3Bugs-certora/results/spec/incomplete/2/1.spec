// Extracted from: contracts/2/specs/aggregator.spec
// Property: notAllReservesBacked_UnbackedArry_Correlation
// Dependency status: incomplete
// Original source ranges included: 1;12-13;57-63
// CVL2 migration is intentionally out of scope for this catalog stage.

methods {
    allBacked() returns (bool) envfree
}

rule notAllReservesBacked_UnbackedArry_Correlation(){
    env e; address[] assets;
    
    bool reservesArrayIsBacked = areAllReservesBackedCorrelation(e, assets);
    bool areAllReservesBacked = allBacked();
    assert reservesArrayIsBacked == areAllReservesBacked;
}
