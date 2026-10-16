// Historical source: contracts/8/specs/fees_LEQ_ATokenBal.spec:201-210
// Property getCLMFees_LEQ_ATokenBAL_RW (rule). Rule body and dependencies copied without modification.
// CVL2 migration and missing symbolic Solidity harness reconstruction out of scope.

// Original CVL: contracts/8/specs/fees_LEQ_ATokenBal.spec:1-55
import "methods_base.spec"


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

// Original CVL: contracts/8/specs/fees_LEQ_ATokenBal.spec:163-199
function getCLMFees_LEQ_ATokenBAL_2(method f) {
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
    //require (forall uint256 x. forall uint256 ind. forall uint256 z.
    //         rayMul_g(to_uint256(rayDiv_g(x,ind)+z),ind) == to_uint256(x+rayMul_g(z,ind))
    //        );
    
    //require(_AToken.balanceOf(currentContract) < 1000);
    //require(getAccumulatedFees()*2 <= _AToken.balanceOf(currentContract));
    require(max_possible_fees() <= _AToken.balanceOf(currentContract));
    
    calldataarg args;
    f(e,args);

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

// Original CVL: contracts/8/specs/methods_base.spec:1-7
import "erc20.spec"

using AToken as _AToken
using DummyERC20_aTokenUnderlying as Underlying
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1
using ATokenVaultHarness as _ATokenVaultHarness


// Original CVL: contracts/8/specs/methods_base.spec:8-63
methods{
    deposit(uint256, address) returns (uint256);
    //depositATokensWithSig(uint256, address, address, (uint8,bytes32,bytes32,uint256)) returns (uint256);
    depositATokensWithSig(uint256, address, address, _ATokenVaultHarness.EIP712Signature) returns (uint256);

    maxDeposit(address) returns (uint256) envfree;
    maxRedeem(address) returns (uint256);

    getFee() returns (uint256) envfree
    owner() returns (address) envfree
    totalSupply() returns uint256 envfree
    balanceOf(address) returns (uint256) envfree
    getLastVaultBalance() returns (uint256) envfree;
    getAccumulatedFees() returns (uint128) envfree;
    maxAssetsWithdrawableFromAave() returns (uint256) envfree;
    
    mulDivWrapper(uint256, uint256, uint256, uint8) envfree;
    previewRedeem(uint256) returns (uint256); 

    _AToken.totalSupply() returns uint256 envfree;
    _AToken.balanceOf(address) returns (uint256) envfree;
    _AToken.scaledTotalSupply() returns (uint256) envfree;
    _AToken.scaledBalanceOf(address) returns (uint256) envfree;
    _AToken.transferFrom(address,address,uint256) returns (bool);

    Underlying.balanceOf(address) returns (uint256) envfree;

    // //*********************  AToken.sol ********************************
    // // The following was copied from StaticATokenLM spec file
    // //*****************************************************************
    //    mint(address,address,uint256,uint256) returns (bool) => DISPATCHER(true)
    //burn(address,address,uint256,uint256) returns (bool) => DISPATCHER(true)
    getIncentivesController() returns (address) => CONSTANT;
    UNDERLYING_ASSET_ADDRESS() returns (address) => CONSTANT;


    // called by AToken.sol::224. A method of IPool.
    finalizeTransfer(address, address, address, uint256, uint256, uint256) => NONDET

    // called from: IncentivizedERC20.sol::207. A method of incentivesControllerLocal.
    handleAction(address,uint256,uint256) => NONDET

    // getPool() returns address => ALWAYS(100);
    getPool() returns address => NONDET;
    
    // // nissan Remark: not sure about the following 3 summarizations:

    // A method of Ipool
    // can this contract change the pool
    getReserveData(address) => CONSTANT;
    
    claimAllRewards(address[],address) => NONDET;

    // called in MetaTxHelpers.sol::27.
    isValidSignature(bytes32, bytes) => NONDET;
}

// Original CVL: contracts/8/specs/methods_base.spec:65-68
definition RAY() returns uint256 = 10^27;
definition RAY_HALF() returns uint256 = 5*10^26;
// In file Constants.sol we have "uint256 constant SCALE = 1e18;"
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

// Original CVL: contracts/8/specs/methods_base.spec:83-139
definition is_depositSig_method(method f) returns bool =
    (
     f.selector == depositWithSig(uint256,address,address,
                                  (uint8,bytes32,bytes32,uint256)).selector ||
     f.selector == depositATokensWithSig(uint256,address,address,
                                         (uint8,bytes32,bytes32,uint256)).selector
    );
definition is_mintSig_method(method f) returns bool =
    (
     f.selector == mintWithATokensWithSig(uint256,address,address,
                                          (uint8,bytes32,bytes32,uint256)).selector ||
     f.selector == mintWithSig(uint256,address,address,
                               (uint8,bytes32,bytes32,uint256)).selector
    );
definition is_withdrawSig_method(method f) returns bool =
    (
     f.selector == withdrawWithSig(uint256,address,address,
                                   (uint8,bytes32,bytes32,uint256)).selector ||
     f.selector == withdrawATokensWithSig(uint256,address,address,
                                          (uint8,bytes32,bytes32,uint256)).selector
    );
definition is_redeemSig_method(method f) returns bool =
    (
     f.selector == redeemWithSig(uint256,address,address,
                                 (uint8,bytes32,bytes32,uint256)).selector ||
     f.selector == redeemWithATokensWithSig(uint256,address,address,
                                            (uint8,bytes32,bytes32,uint256)).selector
    );

definition is_sig_method(method f) returns bool =
    (
     is_depositSig_method(f) || is_mintSig_method(f) || is_withdrawSig_method(f) || is_redeemSig_method(f)
    );


definition is_deposit_method(method f) returns bool =
    (f.selector == deposit(uint256, address).selector ||
     f.selector == depositATokens(uint256, address).selector ||
     is_depositSig_method(f)
    );
definition is_mint_method(method f) returns bool =
    (f.selector == mint(uint256, address).selector ||
     f.selector == mintWithATokens(uint256,address).selector ||
     is_mintSig_method(f)
    );
definition is_withdraw_method(method f) returns bool =
    (
     f.selector == withdraw(uint256,address,address).selector ||
     f.selector == withdrawATokens(uint256,address,address).selector ||
     is_withdrawSig_method(f)
    );
definition is_redeem_method(method f) returns bool =
    (
     f.selector == redeem(uint256,address,address).selector ||
     f.selector == redeemAsATokens(uint256,address,address).selector ||
     is_redeemSig_method(f)
    );

// Original CVL: contracts/8/specs/methods_base.spec:207-207
function maxUint128() returns uint128 {return 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;}

// Original CVL: contracts/8/specs/erc20.spec:1-12
// erc20 methods
methods {
    name()                                => DISPATCHER(true)
    symbol()                              => DISPATCHER(true)
    decimals()                            => DISPATCHER(true)
    totalSupply()                         => DISPATCHER(true)
    balanceOf(address)                    => DISPATCHER(true)
    allowance(address,address)            => DISPATCHER(true)
    approve(address,uint256)              => DISPATCHER(true)
    transfer(address,uint256)             => DISPATCHER(true)
    transferFrom(address,address,uint256) => DISPATCHER(true)
}

// Original CVL: contracts/8/specs/fees_LEQ_ATokenBal.spec:201-210
rule getCLMFees_LEQ_ATokenBAL_RW(method f) filtered {f ->
        !harnessOnlyMethods(f) &&
        !f.isView &&
        (is_withdraw_method(f) || is_redeem_method(f) ||
         f.selector == withdrawFees(address,uint256).selector
        )
}
{
    getCLMFees_LEQ_ATokenBAL_2(f);
}

