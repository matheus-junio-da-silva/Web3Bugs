// Project 24 source contracts/24/spec/LEVarTran.spec lines 71-83; original CVL syntax, no CVL2 migration.
// Original prerequisite CVL declarations from sanity.spec
import "../helpers/erc20.spec"

// using JoeFactory as Factory

methods{
    mint(address) returns uint256 => DISPATCHER(true)
    getPair(address, address) returns address envfree => DISPATCHER(true)
    feeTo() returns address => DISPATCHER(true)
    getReserves() returns uint112, uint112, uint32 => DISPATCHER(true)
    createPair(address, address) returns address => DISPATCHER(true)
    migrator() returns address => DISPATCHER(true)
    initialize(address, address) => DISPATCHER(true)
    newPair() returns address => NONDET
    desiredLiquidity()returns uint256 => NONDET     // in JoePair contract 
}

// Original prerequisite CVL declarations from LEPreset.spec
import "./sanity.spec"

using JoeFactory as Factory
using DummyERC20A as SymbERC20A
using DummyERC20B as SymbERC20B
using DummyWeth as Weth
using JoePair as JP
using RocketJoeToken as RJT

////////////////////////////////////////////////////////////////////////////
//                      Methods                                           //
////////////////////////////////////////////////////////////////////////////

methods {
    // functions
    initialize(address, uint256, address, uint256, uint256, uint256, uint256, uint256, uint256, uint256)
    currentPhase() returns (uint8)
    depositAVAX()
    withdrawAVAX(uint256)
    createPair()
    withdrawLiquidity()
    withdrawIncentives()
    emergencyWithdraw()
    allowEmergencyWithdraw()
    skim()
    getPenalty() returns (uint256)
    getReserves() returns (uint256, uint256)
    getRJoeAmount(uint256) returns (uint256)
    pairBalance(address) returns (uint256)
    _atPhase(uint8)
    getIncentives(address) returns (uint256)

    // generated getters
    issuer() returns(address) envfree
    auctionStart() returns(uint256) envfree           
    tokenIncentivesPercent() returns(uint256) envfree
    floorPrice() returns(uint256) envfree
    userTimelock() returns(uint256) envfree
    issuerTimelock() returns(uint256) envfree
    maxWithdrawPenalty() returns(uint256) envfree
    fixedWithdrawPenalty() returns(uint256) envfree
    rJoePerAvax() returns(uint256) envfree
    stopped() returns(bool) envfree
    maxAllocation() returns(uint256) envfree
    WAVAX() returns(address) envfree
    token() returns(address) envfree
    avaxAllocated() returns(uint256) envfree
    pair() returns(address) envfree
    tokenIncentivesBalance() returns(uint256) envfree
    tokenIncentivesForUsers() returns(uint256) envfree
    tokenIncentiveIssuerRefund() returns(uint256) envfree
    lpSupply() returns(uint256) envfree
    tokenReserve() returns(uint256) envfree
    avaxReserve() returns(uint256) envfree
    tokenAllocated() returns(uint256) envfree
    rJoe() returns(address) envfree
    phaseOneDuration() returns(uint256) envfree
    phaseOneNoFeeDuration() returns(uint256) envfree
    phaseTwoDuration() returns(uint256) envfree

    // harness functions
    getUserAllocation(address) returns(uint256) envfree
    getUserBalance(address) returns(uint256) envfree
    userHasWithdrawnPair(address) returns(bool) envfree
    userHasWithdrawnIncentives(address) returns(bool) envfree
    getNewWAVAX() returns (address) envfree
    getPenaltyCollector() returns (address) envfree
    getTokenBalanceOfThis() returns (uint256) envfree
    getWAVAXbalanceOfThis() returns (uint256) envfree
    getWAVAXbalanceOfPair() returns (uint256) envfree
    getPairBalanceOfThis() returns (uint256) envfree
    getOwner() returns (address) envfree
    getPairBalance(address) returns (uint256) envfree
    getTokenBalance(address) returns (uint256) envfree
    getPairTotalSupply() returns (uint256) envfree
    getPairTotalSupplyOfThis() returns (uint256) envfree
    getBalanceOfThis() returns (uint256) envfree
    factoryGetPairWT() returns (address) envfree
    factoryGetPairTW() returns (address) envfree
 
    isRJLaunchEvent(address) returns(bool) envfree => DISPATCHER(true)
    receiveETH() => DISPATCHER(true)
    
}

////////////////////////////////////////////////////////////////////////////
//                       Definitions                                      //
////////////////////////////////////////////////////////////////////////////


definition NotStarted() returns uint8 = 0;
definition PhaseOne() returns uint8 = 1;
definition PhaseTwo() returns uint8 = 2;
definition PhaseThree() returns uint8 = 3; 

definition oneMinute() returns uint256 = 60;
definition oneHour()   returns uint256 = 60 * oneMinute();
definition oneDay()    returns uint256 = 24 * oneHour();
definition twoDays()    returns uint256 = 2 * oneDay();
definition sevenDays()    returns uint256 = 7 * oneDay();



definition open() returns bool =
    pair() == 0 && !stopped();

definition closed() returns bool =
    pair() != 0 && !stopped();

definition openStopped() returns bool =
    pair() == 0 && stopped();

definition closedStopped() returns bool =
    pair() != 0 && stopped();

// Original prerequisite CVL declarations from LEValidStates.spec
import "./LEPreset.spec"

use invariant oneStateOnly

// This function is here because:
// 1. I requireInvariants from this file
// 2. Preset spec will need import this spec
// 3. Cyclic dependencies are forbidden
function addressDiversity(env e) {
    require token() != currentContract;
    require token() != Weth;
    require token() != JP;
    require token() != RJT;

    require Weth != currentContract;

    require e.msg.sender != currentContract;
    require e.msg.sender != Weth;
    require e.msg.sender != token();
    require e.msg.sender != getPenaltyCollector();

    require pair() != token();
    require pair() != Weth;
    require pair() != currentContract;
    require pair() != e.msg.sender;
    require pair() != RJT;

    require rJoe() != Weth;
    require rJoe() != token();
    require rJoe() != pair();
    require rJoe() != e.msg.sender;
    require rJoe() != currentContract;
}

function safeAssumptions(env e) {
    addressDiversity(e);
    require e.msg.sender != 0;

    requireInvariant alwaysInitialized();
    requireInvariant oneStateOnly();
    requireInvariant factoryGetPairCorrelationCurrentVals(e);

    requireInvariant al_issuerAllocationZero();
    requireInvariant al_balanceLessThanAllocation(e.msg.sender);
    requireInvariant al_userAllocationLessThanMaxAllocation(e.msg.sender);
    requireInvariant al_issuerTimelockNonZero();
    requireInvariant al_userTimelockSeven();
    requireInvariant al_timelocksCorrelation();
    
    requireInvariant op_incentivesCorrelation();  
    requireInvariant op_userNotWithdrawnPair(e.msg.sender);
    requireInvariant op_userNotWithdrawnIncentives(e.msg.sender);
    requireInvariant op_wavaxBalanceAndSumBalances();
    requireInvariant op_avaxAllocZero();
    requireInvariant op_lpSupplyZero();
    requireInvariant op_PairBalanceIsZero();
    requireInvariant op_AvaxCorrelation();
    requireInvariant op_PairAndTotalSupplyCorrelation();
    requireInvariant op_tokenCorrelation();
    
    requireInvariant cl_avaxAllocSumUserBalances();
    requireInvariant cl_avaxReservCheck();
    requireInvariant cl_incentivesCorrelation();
    requireInvariant cl_pairAndGetPairCorrelation();
    requireInvariant cl_AvaxCorrelation();

    requireInvariant os_tokenCorrelation();
    requireInvariant os_avaxAllocSumUserBalances();
}

////////////////////////////////////////////
// HELPERS
////////////////////////////////////////////

// Original prerequisite CVL declarations from LEVarTran.spec
import "./LEValidStates.spec"

use invariant alwaysInitialized
use invariant oneStateOnly
use invariant factoryGetPairCorrelationCurrentVals
use invariant al_issuer_allocation_zero
use invariant al_balance_less_than_allocation
use invariant al_userAllocation_less_than_maxAllocation
use invariant initIssuerTimelockNonZero
use invariant initUserTimelockSeven
use invariant initTimelocksCorrelation
use invariant op_incentivesCorrelation
use invariant op_user_not_withdrawn_pair
use invariant op_user_not_withdrawn_incentives
use invariant opWavaxBalanceAndSumBalances
use invariant op_avax_alloc_zero
use invariant op_lp_supply_zero
use invariant opPairBalanceIsZero
// use invariant opPairAndTotalSupplyCorrelation
// use invariant cl_pairTotalZero
use invariant cl_avax_alloc_sum_user_balances
use invariant cl_avaxReservCheck
// use invariant cl_PhaseCheck
// use invariant cl_AvaxCorrelation
// use invariant cl_pair_bal_eq_lp_sum
// use invariant cl_incentivesCorrelation
// use invariant cl_nonzero_user_pair_bal
// use invariant cl_bal_this_zero
use invariant cl_pairAndGetPairCorrelation


// ALWAYS


// STATUS - verified
// - user allocation cannot be decreased



// Verbatim active rule follows
rule op_balanceChangeByDepositOrWithdraw(method f, env e){     
    require open();
    
    address user;
    uint256 balanceBefore = getUserBalance(user);

    calldataarg args;
    f(e, args);

    uint256 balanceAfter = getUserBalance(user);

    assert balanceBefore != balanceAfter <=> (e.msg.sender == user && (f.selector == depositAVAX().selector || f.selector == withdrawAVAX(uint256).selector)), "pair was changed by wrong method";
}
