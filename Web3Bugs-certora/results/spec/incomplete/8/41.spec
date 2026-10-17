// Source: PropertyGPT/certora_projects/aave_vault; Project 8, example 41.
// Original property body preserved verbatim; no ghost axioms normalized or repaired.
// Shared imports are inlined selectively without duplicated import statements.
// Historical CVL syntax not migrated. No Certora Prover run has been reproduced.

// Original CVL: contracts/8/specs/methods_base.spec:4 (using declarations)
using DummyERC20_aTokenUnderlying as Underlying

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


// Original CVL: contracts/8/specs/totalSupply_EQ_sumAllBal.spec:1-28

methods {
    Underlying.totalSupply() envfree;
    rayMul(uint256 a,uint256 b) returns (uint256) => rayMul_g(a,b);
    rayDiv(uint256 a,uint256 b) returns (uint256) => rayDiv_g(a,b);
    mulDiv(uint256 x, uint256 y, uint256 denominator) returns uint256 => mulDiv3_g(x,y,denominator);
}


ghost rayMul_g(uint256 , uint256) returns uint256 {
    axiom 1==1;
}
ghost rayDiv_g(uint256 , uint256) returns uint256 {
    axiom 1==1;
}
ghost mulDiv3_g(uint256 , uint256 , uint256) returns uint256 {
    axiom 1==1;
}



// **********************************************
// ATokenVault:
// The total supply of ATokenVault equals the sum of all users' balances.
//
// Status: pass
// **********************************************


// Original CVL: contracts/8/specs/totalSupply_EQ_sumAllBal.spec:52-56
invariant inv_sumAllBalance_eq_totalSupply__underline()
    sumAllBalance_underline() == Underlying.totalSupply()
    filtered {f -> !f.isView &&
    f.selector != havoc_all().selector
   }

