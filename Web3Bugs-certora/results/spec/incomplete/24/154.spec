// Project 24 source contracts/24/spec/Staking.spec lines 226-249; original CVL syntax, no CVL2 migration.
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
rule longer_stake_greater_return() { // passes

    storage init = lastStorage; 
    uint256 amount;
    require amount > 0;
    env e0;
    env e1; 
    env e2; 

    // accessing the same account, not current contract
    require e0.msg.sender != currentContract && e1.msg.sender == e0.msg.sender && e2.msg.sender == e0.msg.sender;
    // account 2 stakes longer than account 1, which stakes more than 0 seconds
    require e1.block.timestamp > e0.block.timestamp && e2.block.timestamp > e1.block.timestamp;

    

    deposit(e0, amount);
    uint256 rJoe1 = pendingRJoe(e1, e0.msg.sender);
    deposit(e0, amount) at init;
    uint256 rJoe2 = pendingRJoe(e2, e0.msg.sender);

    // assert rJoe2 > rJoe1; 
    assert exists uint256 dt. e2.block.timestamp - e1.block.timestamp >= dt => rJoe2 > rJoe1;
}
