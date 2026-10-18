// Project 24 source contracts/24/spec/Staking.spec lines 355-372; original CVL syntax, no CVL2 migration.
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
rule verify_deposit() {
    env e;
    require e.msg.sender != currentContract;
    uint256 amount; 

    uint256 balance_pre = userJoeStaked(e.msg.sender);
    uint256 reward_debt_pre = userRewardDebt(e.msg.sender);
    uint256 total_pre = totalJoeStaked();
    deposit(e, amount);
    uint256 balance_post = userJoeStaked(e.msg.sender);
    uint256 reward_debt_post = userRewardDebt(e.msg.sender);
    uint256 total_post = totalJoeStaked();

    assert total_post == total_pre + amount, "totalJoeStaked not updated properly";
    assert balance_post - amount == balance_pre, "improper amount deposited";
    assert (e.block.timestamp > lastRewardTimestamp() => reward_debt_post > reward_debt_pre)  || userJoeStaked(e.msg.sender) == 0, "reward debt not increased";
    assert pendingRJoe(e, e.msg.sender) == 0, "user has unclaimed rewards";
}
