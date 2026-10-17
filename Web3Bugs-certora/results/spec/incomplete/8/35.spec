// Source: PropertyGPT/certora_projects/aave_vault; Project 8, example 35.
// Original property body preserved verbatim; no ghost axioms normalized or repaired.
// Shared imports are inlined selectively without duplicated import statements.
// Historical CVL syntax not migrated. No Certora Prover run has been reproduced.

// Original CVL: contracts/8/specs/methods_base.spec:3;4;5 (using declarations)
using AToken as _AToken
using DummyERC20_aTokenUnderlying as Underlying
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1

// Original CVL: contracts/8/specs/methods_base.spec:16;18;20;21;28;29;30 (selected method declarations)
methods {
    getFee() returns (uint256) envfree
    totalSupply() returns uint256 envfree
    getLastVaultBalance() returns (uint256) envfree;
    getAccumulatedFees() returns (uint128) envfree;
    _AToken.balanceOf(address) returns (uint256) envfree;
    _AToken.scaledTotalSupply() returns (uint256) envfree;
    _AToken.scaledBalanceOf(address) returns (uint256) envfree;
}

// Original CVL: contracts/8/specs/methods_base.spec:68 (shared constants)
definition SCALE() returns uint256 = 1000000000000000000;

// Original CVL: contracts/8/specs/methods_base.spec:207-207
function maxUint128() returns uint128 {return 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;}


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


// Original CVL: contracts/8/specs/positiveSupply_imply_positiveAssets.spec:181-219
function positiveSupply_imply_positiveAssets_RW(method f)
{
    env e;

    require e.msg.sender != currentContract;
    
    require getFee() <= SCALE();  // SCALE is 10^18
    require _AToken.balanceOf(currentContract) <= maxUint128();
    require totalSupply() <= maxUint128();
    require Underlying.totalSupply() <= maxUint128();
    require _AToken.scaledTotalSupply() <= maxUint128();
    requireInvariant inv_sumAllBalance_eq_totalSupply__underline(); 
    requireInvariant inv_sumAllBalance_eq_totalSupply__atoken(); 
    requireInvariant inv_sumAllBalance_eq_totalSupply();
    requireInvariant lastVaultBalance_OK();
    requireInvariant inv_fee_LEQ_ATokenBal();
    
    uint256 ind = _SymbolicLendingPoolL1.getLiquidityIndex();
    uint256 s_bal = _AToken.scaledBalanceOf(currentContract);

    // The following require means: (s_bal - ass/ind)*ind == s_bal*ind - ass
    require (forall uint256 ass.
             rayMul_g(to_uint256(s_bal-rayDiv_g(ass,ind)),ind) == to_uint256(rayMul_g(s_bal,ind)-ass)
            );

    require(totalSupply() != 0 => totalAssets() != 0);

    uint256 totS=totalSupply();
    uint256 totA=totalAssets();
    
    require (forall uint256 assets. forall uint8 rnd.
             totA-assets == 0  =>  totS-mulDiv4_g(assets,totS,totA,rnd) == 0
            );

    calldataarg args;
    f(e,args);

    assert(totalSupply() != 0 => totalAssets() != 0);
}


// Original CVL: contracts/8/specs/positiveSupply_imply_positiveAssets.spec:59-60
invariant inv_sumAllBalance_eq_totalSupply__underline()
    sumAllBalance_underline() == Underlying.totalSupply()


// Original CVL: contracts/8/specs/positiveSupply_imply_positiveAssets.spec:62-63
invariant inv_sumAllBalance_eq_totalSupply__atoken()
    sumAllBalance_atoken() == _AToken.scaledTotalSupply()


// Original CVL: contracts/8/specs/positiveSupply_imply_positiveAssets.spec:65-66
invariant inv_sumAllBalance_eq_totalSupply()
    sumAllBalance() == totalSupply()


// Original CVL: contracts/8/specs/positiveSupply_imply_positiveAssets.spec:74-75
invariant lastVaultBalance_OK()
    getLastVaultBalance() <= _AToken.balanceOf(currentContract)


// Original CVL: contracts/8/specs/positiveSupply_imply_positiveAssets.spec:82-85
invariant inv_fee_LEQ_ATokenBal()
//        to_uint256(                     );
    (getAccumulatedFees()+(_AToken.balanceOf(currentContract)-getLastVaultBalance()))
                                                       <= _AToken.balanceOf(currentContract)


// Original CVL: contracts/8/specs/positiveSupply_imply_positiveAssets.spec:236-239
rule positiveSupply_imply_positiveAssets_specific_RW(method f)
{
    positiveSupply_imply_positiveAssets_RW(f);
}

