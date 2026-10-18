// Source: PropertyGPT/certora_projects/aave_vault; Project 8, example 2.
// Original property body preserved verbatim; no ghost axioms normalized or repaired.
// Shared imports are inlined selectively without duplicated import statements.
// Historical CVL syntax not migrated. No Certora Prover run has been reproduced.

// Original CVL: contracts/8/specs/methods_base.spec:3;4 (using declarations)
using AToken as _AToken
using DummyERC20_aTokenUnderlying as Underlying

// Original CVL: contracts/8/specs/methods_base.spec:20;28;33 (selected method declarations)
methods {
    getLastVaultBalance() returns (uint256) envfree;
    _AToken.balanceOf(address) returns (uint256) envfree;
    Underlying.balanceOf(address) returns (uint256) envfree;
}

// Original CVL: contracts/8/specs/methods_base.spec:65 (shared constants)
definition RAY() returns uint256 = 10^27;

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


// Original CVL: contracts/8/specs/methods_base.spec:214-216
function accrueYieldSummary(){
    accrueYieldCalled = true;
}


// Original CVL: contracts/8/specs/changeInContractBalanceShouldCauseAccrual.spec:2-32


methods{
    //    mulDiv(uint256 x, uint256 y, uint256 denominator, uint8 rounding) returns (uint256) envfree => mulDiv_g(x,y,denominator,rounding);
    mulDiv(uint256 x, uint256 y, uint256 denominator, uint8 rounding) returns (uint256) envfree => mulDiv4_g(x,y,denominator,rounding);
    rayMul(uint256 x, uint256 y) returns (uint256) envfree => rayMul_g(x,y);
    rayDiv(uint256 x, uint256 y) returns (uint256) envfree => rayDiv_g(x,y);

    _accrueYield() envfree => accrueYieldSummary()
}

ghost mulDiv4_g(uint256 , uint256 , uint256, uint8) returns uint256 {
    axiom 1==1;
}

ghost rayMul_g(uint256, uint256) returns uint256{
    axiom 1==1;
    //    axiom forall uint256 x. forall uint256 y. rayMul_g(x,y)*RAY()<= x*y + RAY()/2;
    //axiom forall uint256 x. forall uint256 y. x*y - RAY()/2< rayMul_g(x,y)*RAY();
}

ghost rayDiv_g(uint256, uint256) returns uint256{
    axiom 1==1;
    //    axiom forall uint256 x. forall uint256 y. rayDiv_g(x,y)*y<= x*RAY() + y/2;
    //axiom forall uint256 x. forall uint256 y. x*RAY() - y/2 < rayDiv_g(x,y)*y;
}


// STATUS: Verified
// rule to check that accrueYield function is called everytime some function causes a change 
// in the contract balances. This is crucial for correct accrual of fee.


// Original CVL: contracts/8/specs/changeInContractBalanceShouldCauseAccrual.spec:33-53
rule changeInContractBalanceShouldCauseAccrual(env e, method f)
filtered { f -> !harnessOnlyMethods(f) && !f.isView }
{
    uint256 _contractATokenBal = _AToken.balanceOf(currentContract);
    uint256 _contractULBal = Underlying.balanceOf(currentContract);
    // uint256 _lastUpdated = getLastUpdated();
    // require _lastUpdated + e.block.timestamp <= 0xffffffffff;
    
    calldataarg args;
    f(e, args);

    // uint256 lastUpdated_ = getLastUpdated();
    // uint256 lastVaultBalance_ = getLastVaultBalance();
    uint256 contractATokenBal_ = _AToken.balanceOf(currentContract);
    uint256 contractULBal_ = Underlying.balanceOf(currentContract);
    assert (contractATokenBal_ != _contractATokenBal || _contractULBal != contractULBal_) && 
            (f.selector != withdrawFees(address, uint256).selector && 
            f.selector != emergencyRescue(address, address, uint256).selector) => 
            accrueYieldCalled == true,
            "contract balance change should trigger yield accrual";
}

