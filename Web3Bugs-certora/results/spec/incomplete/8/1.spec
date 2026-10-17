// Source: PropertyGPT/certora_projects/aave_vault; Project 8, example 1.
// Original property body preserved verbatim; no ghost axioms normalized or repaired.
// Shared imports are inlined selectively without duplicated import statements.
// Historical CVL syntax not migrated. No Certora Prover run has been reproduced.

// Original CVL: contracts/8/specs/methods_base.spec:21 (selected method declarations)
methods {
    getAccumulatedFees() returns (uint128) envfree;
}

// Original CVL: contracts/8/specs/methods_base.spec:65 (shared constants)
definition RAY() returns uint256 = 10^27;


// Original CVL: contracts/8/specs/accrueYieldCheck.spec:1-38


methods{
    mulDiv(uint256 x, uint256 y, uint256 denominator, uint8 rounding) returns (uint256) envfree => mulDiv_g(x,y,denominator,rounding);
    rayMul(uint256 x, uint256 y) returns (uint256) envfree => rayMul_g(x,y);
    rayDiv(uint256 x, uint256 y) returns (uint256) envfree => rayDiv_g(x,y);
}

ghost mulDiv_g(uint256, uint256, uint256, uint8) returns uint256 {
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator. forall uint8 rounding.
    rounding == 0 => mulDiv_g(x, y, denominator, rounding)*denominator <= x*y;
    
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator. forall uint8 rounding.
    rounding == 1 => mulDiv_g(x, y, denominator, rounding)*denominator <= x*y+denominator;
    
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator. forall uint8 rounding. 
    rounding == 0 => x*y < mulDiv_g(x,y,denominator, rounding)*denominator + denominator;
    
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator. forall uint8 rounding.
    rounding == 1 => x*y < mulDiv_g(x,y,denominator, rounding)*denominator;
}

ghost rayMul_g(uint256, uint256) returns uint256{
    axiom forall uint256 x. forall uint256 y. rayMul_g(x,y)*RAY()<= x*y + RAY()/2;
    axiom forall uint256 x. forall uint256 y. x*y - RAY()/2< rayMul_g(x,y)*RAY();
}

ghost rayDiv_g(uint256, uint256) returns uint256{
    axiom forall uint256 x. forall uint256 y. rayDiv_g(x,y)*y<= x*RAY() + y/2;
    axiom forall uint256 x. forall uint256 y. x*RAY() - y/2 < rayDiv_g(x,y)*y;
}


// Rule to check the _accrueYield function
// 1. _s.accumulatedFees can only monotonically increase

// STATUS: Verified


// Original CVL: contracts/8/specs/accrueYieldCheck.spec:39-45
rule accrueYieldCheck(env e){
    uint128 _accumulatedFees = getAccumulatedFees();
    accrueYield(e);
    uint128 accumulatedFees_ = getAccumulatedFees();
    
    assert _accumulatedFees <= accumulatedFees_,"accumulated fee can only increase or stay the same";
}

