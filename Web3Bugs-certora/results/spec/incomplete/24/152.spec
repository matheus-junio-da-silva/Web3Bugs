// Project 24 source contracts/24/spec/Staking.spec lines 186-209; original CVL syntax, no CVL2 migration.
// Original prerequisite CVL declarations from Staking.spec
import "../helpers/erc20.spec"

////////////////////////////////////////////////////////////////////////////
//                      Methods                                           //
////////////////////////////////////////////////////////////////////////////
using DummyERC20Impl as joe
using DummyERC20A as A

using RocketJoeToken as rJoe

methods {
    // external functions
    mint(address, uint256) returns (uint256) => DISPATCHER(true) // does not seem to be functioning

    // generated getters 
    lastRewardTimestamp() returns (uint256) envfree
    accRJoePerShare() returns (uint256) envfree
    rJoePerSec() returns (uint256) envfree
    totalJoeStaked() returns (uint256) envfree
    // mapping(address => UserInfo) public userInfo;
    // Initialize(IERC20Upgradeable _joe, RocketJoeToken _rJoe, uint256 _rJoePerSec)
    
    // internal functions
    pendingRJoe(address) returns (uint256)
    deposit(uint256)
    withdraw(uint256)
    emergencyWithdraw()
    updatePool()
    updateEmissionRate(uint256)
    // _safeRJoeTransfer(address, uint256) // internal

    // harness functions
    userJoeStaked(address) returns (uint256) envfree
    userRewardDebt(address) returns (uint256) envfree
    getOwner() returns (address) envfree
    PRECISION() returns (uint256) envfree
}

// rule sanity(method f) {
//     env e; calldataarg args;
//     f(e, args);
//     assert false;
// }

ghost sum_user_balance() returns uint256;
// {
// //     init_state axiom sum_user_balance() == 0;
//     // axiom forall address a. forall address b. sum_user_balance() >= userJoeStaked(a) + userJoeStaked(b);
// }

ghost sum_user_rewards() returns uint256;
// {
//     init_state axiom sum_user_rewards() == 0;
// }

// user sum balance hook
hook Sstore userInfo[KEY address user].amount uint256 userBalance (uint256 oldUserBalance) STORAGE {
    havoc sum_user_balance assuming
        sum_user_balance@new() == sum_user_balance@old() + userBalance - oldUserBalance;
}

hook Sstore rJoe._balances[KEY address user] uint256 reward (uint256 oldReward) STORAGE {
    havoc sum_user_rewards assuming
        sum_user_rewards@new() == sum_user_rewards@old() + reward - oldReward;
}

// initialization invariance 

ghost initialized() returns bool;

ghost initializing() returns bool;

// hook Sload bool init currentContract._initialized STORAGE {
//   havoc initialized assuming initialized@new() == init;
// }

hook Sstore currentContract._initialized bool init STORAGE {
    havoc initialized assuming initialized@new() == init;
}

hook Sstore currentContract._initializing bool initing STORAGE {
    havoc initializing assuming initializing@new() == initing;
}

// helper invariants

// Unresolved requireInvariant totalJoeStaked_sums_user_balance

// Required invariant is_initialized
invariant is_initialized()
    initialized()
{ preserved {
    requireInvariant not_initializing();
}}

// Required invariant not_initializing
invariant not_initializing()
    !initializing()

// Verbatim active rule follows
rule staking_non_trivial_rJoe() {
    // requireInvariant totalJoeStaked_sums_user_balance();
    requireInvariant is_initialized();
    requireInvariant not_initializing();
    require PRECISION() > 0;
    require rJoePerSec() > 0 && rJoePerSec() < 1000000; // realistic range to help the tool run this rule faster

    uint256 amount;
    require amount > 0;
    env e0; env e1;
    require e0.msg.sender == e1.msg.sender;

    deposit(e0, amount);
    require e1.block.timestamp > lastRewardTimestamp();
    require userRewardDebt(e0.msg.sender) < max_uint256;
    uint dt = e1.block.timestamp - lastRewardTimestamp(); // store this as a variable for more readable cex
    uint256 rewards = pendingRJoe(e1, e0.msg.sender);
    assert exists uint256 t. (t == dt) => rewards > 0,  "trivial rJoe";

    // doing the min interval calculations would likely be a better rule but causes timeouts, left for future consideration
    // uint256 min_interval = totalJoeStaked() / rJoePerSec();
    // require min_interval < (max_uint256 / 10) && min_interval > 0; // divide by 10 to reduce the scope of the problem
    // assert dt > min_interval => rJoe != 0, "trivial rJoe";
}
