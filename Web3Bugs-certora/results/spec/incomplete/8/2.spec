// Historical source: contracts/8/specs/changeInContractBalanceShouldCauseAccrual.spec:33-53
// Property changeInContractBalanceShouldCauseAccrual (rule). Rule body and dependencies copied without modification.
// CVL2 migration and missing symbolic Solidity harness reconstruction out of scope.

// Original CVL: contracts/8/specs/changeInContractBalanceShouldCauseAccrual.spec:1-32
import "methods_base.spec"


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

// Original CVL: contracts/8/specs/methods_base.spec:142-145
// ghost variable to track the calling of _accrueYield function
ghost bool accrueYieldCalled{
    init_state axiom accrueYieldCalled == false;
}

// Original CVL: contracts/8/specs/methods_base.spec:214-216
function accrueYieldSummary(){
    accrueYieldCalled = true;
}

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

