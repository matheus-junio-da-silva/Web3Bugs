// Project 23 exact historical source: Reserve.spec
// Property tokensNonInterference original lines 120-170 SHA256 96c7fd27a357f8e8edd0f24cc58e608b17c710c6250f59abbb52fe2b03a71828
// ///////////////////////////////////////////////////////////////
// rule ideas for verification of the functions in Reserve.sol
// ///////////////////////////////////////////////////////////////

using DummyERC20Impl as dummyERC20Token
using DummyERC20A as tokenA
using DummyERC20B as tokenB
using ReserveHarness as reserveH

methods{
    ////////////////////////////////////////
	// ERC20 methods
	transferFrom(address, address, uint256) => DISPATCHER(true)
	transfer(address, uint256) => DISPATCHER(true)
	//
    tokenA.balanceOf(address) envfree
	tokenB.balanceOf(address) envfree
	dummyERC20Token.balanceOf(address) envfree
	//
    tokenA.totalSupply() envfree
	tokenB.totalSupply() envfree
	dummyERC20Token.totalSupply() envfree
    transfer() => DISPATCHER(true)

    ////////////////////////////////////////
    // Call resolutions for IReservePlugin
    afterStart(address, uint256) => NONDET //HAVOC_ALL
    afterDeposition(address, uint256) => NONDET //HAVOC_ALL
    beforeWithdrawal(address, uint256) => NONDET //HAVOC_ALL
    beforeEnd(address, uint256) => NONDET //HAVOC_ALL

    reserveH.getDeposited(address) envfree
    reserveH.getPlugins(address) envfree
}

// State variables of the Reserve.sol contract:
// mapping(address => bool) public isUser;           // The value is `true` if an address is a user, `false` otherwise.
// mapping(IERC20 => uint256) public deposited;      // How many tokens are deposited for each token address.
// mapping(IERC20 => IReservePlugin) public plugins; // The reserved plugins for each token address.

// function setPlugin(IERC20 token, IReservePlugin newPlugin) public onlyOwner
// function deposit(IERC20 token, address from, uint256 amt) public override onlyUser
// function withdraw(IERC20 token, address to, uint256 amt) public override onlyUser
// function forceWithdraw(IERC20 token, IReservePlugin plugin, address to, uint256 amt) public onlyOwner
// function setDeposited(IERC20 token, uint256 amt) public onlyOwner
// function addUser(address user) public onlyOwner
// function removeUser(address user) public onlyOwner
// function _pluginAddr(IReservePlugin plugin) internal view returns (address)
// function _transfer(IERC20 token, address from, address to, uint256 amt) internal


// sanity rule - must always fail

rule tokensNonInterference() {
    env e;
    calldataarg args;

    bool depositOrWithdraw;

    address user;
    uint256 amtDeposited;
    uint256 amtWithdrawn;
    uint256 tokenABalanceOfUserBefore;    uint256 tokenABalanceOfUserAfter;
    uint256 tokenBBalanceOfUserBefore;    uint256 tokenBBalanceOfUserAfter;
    uint256 tokenABalanceOfReserveBefore; uint256 tokenABalanceOfReserveAfter;
    uint256 tokenBBalanceOfReserveBefore; uint256 tokenBBalanceOfReserveAfter;
    uint256 tokenADepositedBefore;        uint256 tokenADepositedAfter;
    uint256 tokenBDepositedBefore;        uint256 tokenBDepositedAfter;

    tokenABalanceOfUserBefore = tokenA.balanceOf(user);
    tokenBBalanceOfUserBefore = tokenB.balanceOf(user);
    tokenABalanceOfReserveBefore = tokenA.balanceOf(reserveH);
    tokenBBalanceOfReserveBefore = tokenB.balanceOf(reserveH);
    tokenADepositedBefore = getDeposited(tokenA);
    tokenBDepositedBefore = getDeposited(tokenB);

    require tokenADepositedBefore == tokenABalanceOfReserveBefore;
    require tokenBDepositedBefore == tokenBBalanceOfReserveBefore;
    //require e.msg.sender != 0;
    require reserveH.getPlugins(tokenA) == 0;
    require reserveH.getPlugins(tokenB) == 0;

    //deposit(e, tokenA, user, amtDeposited);
    //f(e,args);
    //withdraw(e, tokenA, user, amtWithdrawn);
    if (depositOrWithdraw) {
        deposit(e, tokenA, user, amtDeposited);
    } else {
        withdraw(e, tokenA, user, amtWithdrawn);
    }

    require amtDeposited == amtWithdrawn;

    tokenABalanceOfUserAfter = tokenA.balanceOf(user);
    tokenBBalanceOfUserAfter = tokenB.balanceOf(user);
    tokenABalanceOfReserveAfter = tokenA.balanceOf(reserveH);
    tokenBBalanceOfReserveAfter = tokenB.balanceOf(reserveH);
    tokenADepositedAfter = getDeposited(tokenA);
    tokenBDepositedAfter = getDeposited(tokenB);

    assert tokenBBalanceOfUserBefore == tokenBBalanceOfUserAfter;
    assert tokenBBalanceOfReserveBefore == tokenBBalanceOfReserveAfter;
    assert tokenBDepositedBefore == tokenBDepositedAfter;
}
