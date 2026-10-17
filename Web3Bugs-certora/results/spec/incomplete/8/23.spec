// Source: PropertyGPT/certora_projects/aave_vault; Project 8, example 23.
// Original property body preserved verbatim; no ghost axioms normalized or repaired.
// Shared imports are inlined selectively without duplicated import statements.
// Historical CVL syntax not migrated. No Certora Prover run has been reproduced.

// Original CVL: contracts/8/specs/methods_base.spec:3;4;5;6 (using declarations)
using AToken as _AToken
using DummyERC20_aTokenUnderlying as Underlying
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1
using ATokenVaultHarness as _ATokenVaultHarness

// Original CVL: contracts/8/specs/methods_base.spec:11;16;18;20;28;29 (selected method declarations)
methods {
    depositATokensWithSig(uint256, address, address, _ATokenVaultHarness.EIP712Signature) returns (uint256);
    getFee() returns (uint256) envfree
    totalSupply() returns uint256 envfree
    getLastVaultBalance() returns (uint256) envfree;
    _AToken.balanceOf(address) returns (uint256) envfree;
    _AToken.scaledTotalSupply() returns (uint256) envfree;
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


// Original CVL: contracts/8/specs/lastVaultBal_LEQ_ATokenBalThis.spec:40-41
invariant inv_sumAllBalance_eq_totalSupply__underline()
    sumAllBalance_underline() == Underlying.totalSupply()


// Original CVL: contracts/8/specs/lastVaultBal_LEQ_ATokenBalThis.spec:43-44
invariant inv_sumAllBalance_eq_totalSupply__atoken()
    sumAllBalance_atoken() == _AToken.scaledTotalSupply()


// Original CVL: contracts/8/specs/lastVaultBal_LEQ_ATokenBalThis.spec:46-47
invariant inv_sumAllBalance_eq_totalSupply()
    sumAllBalance() == totalSupply()


// Original CVL: contracts/8/specs/lastVaultBal_LEQ_ATokenBalThis.spec:63-132
rule lastVaultBalance_LEQ_ATokenBalThis(env e, method f) filtered {f ->
    f.selector != initialize(address,uint256,string,string,uint256).selector &&
    !harnessOnlyMethods(f) &&
    !f.isView
    //    f.selector != havoc_all().selector
}
{
    require e.msg.sender != currentContract;
    require getFee() <= SCALE();  // SCALE is 10^18
    //require _AToken.balanceOf(currentContract) <= maxUint128();
    //require totalSupply() <= maxUint128();
    //require Underlying.totalSupply() <= maxUint128();
    //require _AToken.scaledTotalSupply() <= maxUint128();
    requireInvariant inv_sumAllBalance_eq_totalSupply__underline(); 
    requireInvariant inv_sumAllBalance_eq_totalSupply__atoken(); 
    requireInvariant inv_sumAllBalance_eq_totalSupply();
    
    // The following require means: (x/ind+z)*ind == x+z*ind +-1
    
    require (forall uint256 x. forall uint256 ind. forall uint256 z.
             rayMul_g(to_uint256(rayDiv_g(x,ind)+z),ind) == to_uint256(x+rayMul_g(z,ind))
             ||
             rayMul_g(to_uint256(rayDiv_g(x,ind)+z),ind) == to_uint256(x+rayMul_g(z,ind))+1
             ||
             rayMul_g(to_uint256(rayDiv_g(x,ind)+z),ind)+1 == to_uint256(x+rayMul_g(z,ind))
             );
    //    require (forall uint256 x. forall uint256 ind. forall uint256 z.
    //         rayMul_g(to_uint256(rayDiv_g(x,ind)+z),ind) == to_uint256(x+rayMul_g(z,ind))
    //        );
    

    require (getLastVaultBalance() <= _AToken.balanceOf(currentContract));
    //    uint256 _last_vault_bal = getLastVaultBalance();
    // uint256 _atoken_bal = _AToken.balanceOf(currentContract);
    //uint256 _the_diff = _last_vault_bal <= _atoken_bal ? 0 : _last_vault_bal-_atoken_bal;

    if (f.selector == withdrawFees(address,uint256).selector) {
        address to; uint256 amount;
        require to != currentContract;
        withdrawFees(e,to,amount);
    }
    else if (f.selector == depositATokensWithSig(uint256,address,address,
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

    assert (getLastVaultBalance() <= _AToken.balanceOf(currentContract));

    //uint256 last_vault_bal_ = getLastVaultBalance();
    //uint256 atoken_bal_ = _AToken.balanceOf(currentContract);
    //uint256 the_diff_ = last_vault_bal_ <= atoken_bal_ ? 0 : last_vault_bal_-atoken_bal_;

    //assert (the_diff_ <= _the_diff + 1);
}

