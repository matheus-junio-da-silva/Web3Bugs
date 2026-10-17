// Source: PropertyGPT/certora_projects/aave_vault; Project 8, example 21.
// Original property body preserved verbatim; no ghost axioms normalized or repaired.
// Shared imports are inlined selectively without duplicated import statements.
// Historical CVL syntax not migrated. No Certora Prover run has been reproduced.

// Original CVL: contracts/8/specs/methods_base.spec:3;4;5 (using declarations)
using AToken as _AToken
using DummyERC20_aTokenUnderlying as Underlying
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1

// Original CVL: contracts/8/specs/methods_base.spec:29 (selected method declarations)
methods {
    _AToken.scaledTotalSupply() returns (uint256) envfree;
}

// Original CVL: contracts/8/specs/methods_base.spec:183-193
ghost sumAllBalance_atoken() returns mathint {
    init_state axiom sumAllBalance_atoken() == 0;
}

hook Sstore _AToken._userState[KEY address a] .(offset 0) uint128 balance (uint128 old_balance) STORAGE {
  havoc sumAllBalance_atoken assuming sumAllBalance_atoken@new() == sumAllBalance_atoken@old() + balance - old_balance;
}

hook Sload uint128 balance _AToken._userState[KEY address a] .(offset 0) STORAGE {
    require balance <= sumAllBalance_atoken();
}


// Original CVL: contracts/8/specs/lastVaultBal_LEQ_ATokenBalThis.spec:1-39

methods {
    Underlying.totalSupply() envfree;
    havoc_all() envfree;
    _SymbolicLendingPoolL1.getLiquidityIndex() envfree;

    rayMul(uint256 a,uint256 b) returns (uint256) => rayMul_g(a,b);
    rayDiv(uint256 a,uint256 b) returns (uint256) => rayDiv_g(a,b);
    mulDiv(uint256 x, uint256 y, uint256 denominator) returns uint256 => mulDiv3_g(x,y,denominator);
    
    havoc_all_dummy() => HAVOC_ALL;
}

ghost mulDiv3_g(uint256 , uint256 , uint256) returns uint256 {
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator.
        mulDiv3_g(x,y,denominator)*denominator <= x*y;
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



// ******************************************************************************
// The following 3 invariants are proved in totalSupply_EQ_sumAllBal.spec
// ******************************************************************************


// Original CVL: contracts/8/specs/lastVaultBal_LEQ_ATokenBalThis.spec:43-44
invariant inv_sumAllBalance_eq_totalSupply__atoken()
    sumAllBalance_atoken() == _AToken.scaledTotalSupply()

