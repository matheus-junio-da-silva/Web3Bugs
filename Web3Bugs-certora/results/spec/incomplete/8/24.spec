// Source: PropertyGPT/certora_projects/aave_vault; Project 8, example 24.
// Original property body preserved verbatim; no ghost axioms normalized or repaired.
// Shared imports are inlined selectively without duplicated import statements.
// Historical CVL syntax not migrated. No Certora Prover run has been reproduced.

// Original CVL: contracts/8/specs/methods_base.spec:4;5 (using declarations)
using DummyERC20_aTokenUnderlying as Underlying
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1

// Original CVL: contracts/8/specs/methods_base.spec:167-177
ghost sumAllBalance_underline() returns mathint {
    init_state axiom sumAllBalance_underline() == 0;
}

hook Sstore Underlying.b[KEY address a] uint256 balance (uint256 old_balance) STORAGE {
  havoc sumAllBalance_underline assuming sumAllBalance_underline@new() == sumAllBalance_underline@old() + balance - old_balance;
}

hook Sload uint256 balance Underlying.b[KEY address a] STORAGE {
    require balance <= sumAllBalance_underline();
}


// Original CVL: contracts/8/specs/positiveSupply_imply_positiveAssets.spec:1-58

methods {
    totalAssets() returns uint256 envfree;
    Underlying.totalSupply() envfree;
    havoc_all() envfree;
    _SymbolicLendingPoolL1.getLiquidityIndex() envfree;

    rayMul(uint256 a,uint256 b) returns (uint256) => rayMul_g(a,b);
    rayDiv(uint256 a,uint256 b) returns (uint256) => rayDiv_g(a,b);
    
    havoc_all_dummy() => HAVOC_ALL;
    mulDiv(uint256 x, uint256 y, uint256 denominator, uint8 rounding) returns uint256 =>
        mulDiv4_g(x,y,denominator,rounding);
}

ghost mulDiv4_g(uint256 , uint256 , uint256, uint8) returns uint256 {
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator. forall uint8 rounding.
        (
         ( (x==0 || y==0) => mulDiv4_g(x,y,denominator,rounding)==0)
         &&
         (mulDiv4_g(x,y,denominator,rounding)*denominator <= x*y)
         &&
         (y<=denominator => mulDiv4_g(x,y,denominator,rounding)<=x)
        );
}


ghost rayMul_g(uint256 , uint256) returns uint256 {
    axiom forall uint256 x. forall uint256 y.
        (
         ((x==0||y==0) => rayMul_g(x,y)==0)
         &&
         x <= rayMul_g(x,y) && rayMul_g(x,y) <= 2*x
        );
}
ghost rayDiv_g(uint256 , uint256) returns uint256 {
    axiom forall uint256 x. forall uint256 y.
        (
         x/2 <= rayDiv_g(x,y) && rayDiv_g(x,y) <= x
        );
}



/*
ghost rayMul_g(uint256 , uint256) returns uint256 {
    axiom forall uint256 x. forall uint256 y.rayMul_g(x,y)==x;
}
ghost rayDiv_g(uint256 , uint256) returns uint256 {
    axiom forall uint256 x. forall uint256 y. rayDiv_g(x,y)==x;
}
*/


// ******************************************************************************
// The following 3 invariants are proved in totalSupply_EQ_sumAllBal.spec
// ******************************************************************************


// Original CVL: contracts/8/specs/positiveSupply_imply_positiveAssets.spec:59-60
invariant inv_sumAllBalance_eq_totalSupply__underline()
    sumAllBalance_underline() == Underlying.totalSupply()

