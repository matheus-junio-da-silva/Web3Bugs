// Source: PropertyGPT/certora_projects/aave_vault; Project 8, example 42.
// Original property body preserved verbatim; no ghost axioms normalized or repaired.
// Shared imports are inlined selectively without duplicated import statements.
// Historical CVL syntax not migrated. No Certora Prover run has been reproduced.

// Original CVL: contracts/8/specs/methods_base.spec:3;4 (using declarations)
using AToken as _AToken
using DummyERC20_aTokenUnderlying as Underlying

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


// Original CVL: contracts/8/specs/totalSupply_EQ_sumAllBal.spec:69-73
invariant inv_sumAllBalance_eq_totalSupply__atoken()
    sumAllBalance_atoken() == _AToken.scaledTotalSupply()
    filtered {f -> !f.isView &&
              f.selector != havoc_all().selector
   }

