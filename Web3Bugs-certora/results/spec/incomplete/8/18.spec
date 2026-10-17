// Source: PropertyGPT/certora_projects/aave_vault; Project 8, example 18.
// Original property body preserved verbatim; no ghost axioms normalized or repaired.
// Shared imports are inlined selectively without duplicated import statements.
// Historical CVL syntax not migrated. No Certora Prover run has been reproduced.

// Original CVL: contracts/8/specs/methods_base.spec:3;4;5;6 (using declarations)
using AToken as _AToken
using DummyERC20_aTokenUnderlying as Underlying
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1
using ATokenVaultHarness as _ATokenVaultHarness

// Original CVL: contracts/8/specs/methods_base.spec:11;16;18;20;21;28;29;30 (selected method declarations)
methods {
    depositATokensWithSig(uint256, address, address, _ATokenVaultHarness.EIP712Signature) returns (uint256);
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

// Original CVL: contracts/8/specs/methods_base.spec:70-81
definition harnessOnlyMethods(method f) returns bool =
    (f.selector == havoc_all().selector ||
     f.selector == accrueYield().selector ||
     f.selector == getAccumulatedFees().selector ||
     f.selector == mulDiv__(uint256,uint256,uint256,uint8).selector ||
     f.selector == rayMul__(uint256,uint256).selector ||
     f.selector == rayDiv__(uint256,uint256).selector ||
     f.selector == handleDeposit_wrapper(uint256,address,address, bool).selector ||
     f.selector == handleMint_wrapper(uint256,address,address,bool).selector ||
     f.selector == handleWithdraw_wrapper(uint256,address,address,address,bool).selector ||
     f.selector == handleRedeem_wrapper(uint256,address,address,address,bool).selector
    );


// Original CVL: contracts/8/specs/methods_base.spec:207-207
function maxUint128() returns uint128 {return 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;}


// Original CVL: contracts/8/specs/fees_LEQ_ATokenBal.spec:1-55


methods {
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


function max_possible_fees() returns uint256 {
    return to_uint256(getAccumulatedFees()
                      +
                      (_AToken.balanceOf(currentContract)-getLastVaultBalance())
                     );
}





// ******************************************************************************
// The following 3 invariants are proved in totalSupply_EQ_sumAllBal.spec
// ******************************************************************************


// Original CVL: contracts/8/specs/fees_LEQ_ATokenBal.spec:91-148
function getCLMFees_LEQ_ATokenBAL_1(method f) {
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
    
    uint256 ind = _SymbolicLendingPoolL1.getLiquidityIndex();
    uint256 s_bal = _AToken.scaledBalanceOf(currentContract);


    // The following require means: (s_bal - ass/ind)*ind == s_bal*ind - ass
    require (forall uint256 ass.
             rayMul_g(to_uint256(s_bal-rayDiv_g(ass,ind)),ind) == to_uint256(rayMul_g(s_bal,ind)-ass)
            );

    // The following require means: (x/ind+z)*ind == x+z*ind 
    require (forall uint256 x. forall uint256 ind. forall uint256 z.
             rayMul_g(to_uint256(rayDiv_g(x,ind)+z),ind) == to_uint256(x+rayMul_g(z,ind))
            );
    
    require(max_possible_fees() <= _AToken.balanceOf(currentContract));

    if (f.selector == depositATokensWithSig(uint256,address,address,
                                            (uint8,bytes32,bytes32,uint256)).selector) {
        uint256 assets; address receiver; address depositor;
        _ATokenVaultHarness.EIP712Signature sig;
        
        require depositor != currentContract;
        depositATokensWithSig(e,assets,receiver,depositor,sig);
    }
    else if (f.selector == mintWithATokensWithSig(uint256,address,address,
                                             (uint8,bytes32,bytes32,uint256)).selector) {
        uint256 shares; address receiver; address depositor;
        _ATokenVaultHarness.EIP712Signature sig;
        
        require depositor != currentContract;
        mintWithATokensWithSig(e, shares, receiver, depositor, sig);
    }
    else {
        calldataarg args;
        f(e,args);
    }

    require _AToken.balanceOf(currentContract) <= maxUint128();
    require totalSupply() <= maxUint128();
    //    require Underlying.totalSupply() <= maxUint128();
    //require _AToken.scaledTotalSupply() <= maxUint128();

    assert(max_possible_fees() <= _AToken.balanceOf(currentContract));
}


// Original CVL: contracts/8/specs/fees_LEQ_ATokenBal.spec:56-57
invariant inv_sumAllBalance_eq_totalSupply__underline()
    sumAllBalance_underline() == Underlying.totalSupply()


// Original CVL: contracts/8/specs/fees_LEQ_ATokenBal.spec:59-60
invariant inv_sumAllBalance_eq_totalSupply__atoken()
    sumAllBalance_atoken() == _AToken.scaledTotalSupply()


// Original CVL: contracts/8/specs/fees_LEQ_ATokenBal.spec:62-63
invariant inv_sumAllBalance_eq_totalSupply()
    sumAllBalance() == totalSupply()


// Original CVL: contracts/8/specs/fees_LEQ_ATokenBal.spec:69-70
invariant lastVaultBalance_OK()
    getLastVaultBalance() <= _AToken.balanceOf(currentContract)


// Original CVL: contracts/8/specs/methods_base.spec:128-133
definition is_withdraw_method(method f) returns bool =
    (
     f.selector == withdraw(uint256,address,address).selector ||
     f.selector == withdrawATokens(uint256,address,address).selector ||
     is_withdrawSig_method(f)
    );

// Original CVL: contracts/8/specs/methods_base.spec:134-139
definition is_redeem_method(method f) returns bool =
    (
     f.selector == redeem(uint256,address,address).selector ||
     f.selector == redeemAsATokens(uint256,address,address).selector ||
     is_redeemSig_method(f)
    );

// Original CVL: contracts/8/specs/methods_base.spec:151-153
ghost sumAllBalance() returns mathint {
    init_state axiom sumAllBalance() == 0;
}

// Original CVL: contracts/8/specs/methods_base.spec:155-157
hook Sstore _balances[KEY address a] uint256 balance (uint256 old_balance) STORAGE {
  havoc sumAllBalance assuming sumAllBalance@new() == sumAllBalance@old() + balance - old_balance;
}

// Original CVL: contracts/8/specs/methods_base.spec:159-161
hook Sload uint256 balance _balances[KEY address a] STORAGE {
    require balance <= sumAllBalance();
}

// Original CVL: contracts/8/specs/methods_base.spec:183-185
ghost sumAllBalance_atoken() returns mathint {
    init_state axiom sumAllBalance_atoken() == 0;
}

// Original CVL: contracts/8/specs/methods_base.spec:187-189
hook Sstore _AToken._userState[KEY address a] .(offset 0) uint128 balance (uint128 old_balance) STORAGE {
  havoc sumAllBalance_atoken assuming sumAllBalance_atoken@new() == sumAllBalance_atoken@old() + balance - old_balance;
}

// Original CVL: contracts/8/specs/methods_base.spec:191-193
hook Sload uint128 balance _AToken._userState[KEY address a] .(offset 0) STORAGE {
    require balance <= sumAllBalance_atoken();
}

// Original CVL: contracts/8/specs/methods_base.spec:167-169
ghost sumAllBalance_underline() returns mathint {
    init_state axiom sumAllBalance_underline() == 0;
}

// Original CVL: contracts/8/specs/methods_base.spec:171-173
hook Sstore Underlying.b[KEY address a] uint256 balance (uint256 old_balance) STORAGE {
  havoc sumAllBalance_underline assuming sumAllBalance_underline@new() == sumAllBalance_underline@old() + balance - old_balance;
}

// Original CVL: contracts/8/specs/methods_base.spec:175-177
hook Sload uint256 balance Underlying.b[KEY address a] STORAGE {
    require balance <= sumAllBalance_underline();
}

// Original CVL: contracts/8/specs/methods_base.spec:97-103
definition is_withdrawSig_method(method f) returns bool =
    (
     f.selector == withdrawWithSig(uint256,address,address,
                                   (uint8,bytes32,bytes32,uint256)).selector ||
     f.selector == withdrawATokensWithSig(uint256,address,address,
                                          (uint8,bytes32,bytes32,uint256)).selector
    );

// Original CVL: contracts/8/specs/methods_base.spec:104-110
definition is_redeemSig_method(method f) returns bool =
    (
     f.selector == redeemWithSig(uint256,address,address,
                                 (uint8,bytes32,bytes32,uint256)).selector ||
     f.selector == redeemWithATokensWithSig(uint256,address,address,
                                            (uint8,bytes32,bytes32,uint256)).selector
    );

// Original CVL: contracts/8/specs/fees_LEQ_ATokenBal.spec:150-159
rule getCLMFees_LEQ_ATokenBAL_DM_other(method f) filtered {f ->
    !harnessOnlyMethods(f) &&
    !f.isView &&
    !is_withdraw_method(f) &&
    !is_redeem_method(f) &&
    f.selector != withdrawFees(address,uint256).selector
}
{
    getCLMFees_LEQ_ATokenBAL_1(f);
}

