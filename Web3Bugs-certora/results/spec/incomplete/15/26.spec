// HELIX Project 15 historical CVL extraction
// Source contracts/15/flashMinter.spec property lines 98-113
// Historic syntax unchanged; dependency-incomplete, no CVL2 migration

// Original CVL non-property helpers from contracts/15/flashMinter.spec
using GhoToken as gho
using GhoAToken as atoken
using MockFlashBorrower as flashBorrower

methods{
    isPoolAdmin(address user) returns (bool) => retreivePoolAdminFromGhost(user)
    isFlashBorrower(address user) returns (bool) => retreiveFlashBorrowerFromGhost(user)
    onFlashLoan(address, address, uint256, uint256, bytes) returns (bytes32) => DISPATCHER(true)
    getACLManager() returns (address) => NONDET

    // FlashBorrower
    flashBorrower.action() returns (uint8) envfree
    flashBorrower._transferTo() returns (address) envfree
    gho.allowance(address, address) returns (uint256) envfree
    burn(uint256) => DISPATCHER(true)
    mint(address, uint256) => DISPATCHER(true)
    transfer(address, uint256) returns (bool) => DISPATCHER(true)
    balanceOf(address) returns (uint256) => DISPATCHER(true)
    
    decreaseBalanceFromInterest(address, uint256) => NONDET
    getBalanceFromInterest(address) => NONDET
    gho.totalSupply() returns (uint256) envfree
    gho.balanceOf(address) returns (uint256) envfree

    atoken.getGhoTreasury() returns (address) envfree
}

// keeps track of users with pool admin permissions in order to return a consistent value per user
ghost mapping(address => bool) poolAdmin_ghost;
// keeps track of users with flash borrower permissions in order to return a consistent value per user
ghost mapping(address => bool) flashBorrower_ghost;

// returns whether the user is a pool admin
function retreivePoolAdminFromGhost(address user) returns bool{
    return poolAdmin_ghost[user];
}

// returns whether the user is a flash borrower
function retreiveFlashBorrowerFromGhost(address user) returns bool{
    return flashBorrower_ghost[user];
}

// a set of assumptions needed for rules that call flashloan
function flashLoanReqs(env e){
    require e.msg.sender != currentContract;
    require gho.allowance(currentContract, e.msg.sender) == 0;
}

// an assumption that demands the sum of balances of 3 given users is no more than the total supply
function ghoBalanceOfTwoUsersLETotalSupply(address user1, address user2, address user3){
    require gho.balanceOf(user1) + gho.balanceOf(user2) + gho.balanceOf(user3) <= gho.totalSupply();
}

/**
 * @title The GHO balance of the flash minter should grow when calling any function, excluding distributeFees
 */

// Exact literal original property follows
rule availableLiquidityDoesntChange(method f, address token){
    env e; calldataarg args;
    uint256 _liquidity = maxFlashLoan(e, token);

    f(e, args);

    uint256 liquidity_ = maxFlashLoan(e, token);

    assert liquidity_ == _liquidity;
}

/**
 * @title Checks the integrity of distributeFees:
 *        1. As long as the treasury contract itself isn't acting as a flashloan minter, the flashloan facilitator's GHO balance should be empty after distribution
 *        2. The change in balances of the receiver (treasury) and the sender (flash minter) is the same. i.e. no money is being generated out of thin air
 */
