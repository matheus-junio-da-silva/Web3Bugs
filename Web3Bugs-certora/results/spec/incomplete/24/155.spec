// Project 24 source contracts/24/spec/Staking.spec lines 256-284; original CVL syntax, no CVL2 migration.
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



// Verbatim active rule follows
rule deposit_no_frontrunning(method f) // passes
{
    // setup
    env e; calldataarg args;
    uint256 x;
    require userJoeStaked(currentContract) > x;
    uint256 bal_pre_clean = userJoeStaked(e.msg.sender);
    uint256 user_bal_pre_clean = joe.balanceOf(e, e.msg.sender);
    storage init = lastStorage;

    // run with frontrunning
    f(e, args);
    require userJoeStaked(currentContract) > x;
    uint256 bal_pre_f = userJoeStaked(e.msg.sender);
    uint256 user_bal_pre_f = joe.balanceOf(e, e.msg.sender);
    deposit(e, x);
    uint256 bal_post_f = userJoeStaked(e.msg.sender);
    uint256 user_bal_post_f = joe.balanceOf(e, e.msg.sender);
    uint256 delta_f = bal_post_f - bal_pre_f;

    // run without frontrunning
    deposit(e, x) at init;
    uint256 bal_post_clean = userJoeStaked(e.msg.sender);
    uint256 user_bal_post_clean = joe.balanceOf(e, e.msg.sender);
    uint256 delta_clean = bal_post_clean - bal_pre_clean;

    assert delta_f == delta_clean, "frontrunning found";
    assert user_bal_pre_clean - user_bal_post_clean == user_bal_pre_f - user_bal_post_f, "balance not received by user";
}
