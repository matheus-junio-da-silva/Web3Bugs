// Project 23 exact historical source: Reserve.spec
// Property totalMoneyIsConstant original lines 84-116 SHA256 96c7fd27a357f8e8edd0f24cc58e608b17c710c6250f59abbb52fe2b03a71828
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

rule totalMoneyIsConstant(method f) {
    env e; // env eB; env eF;
    calldataarg args;

    address user;
    uint256 amtDeposited;
    uint256 amtWithdrawn;
    uint256 balanceOfUserBefore;    uint256 balanceOfUserAfter;
    uint256 balanceOfReserveBefore; uint256 balanceOfReserveAfter;
    uint256 depositedBefore;        uint256 depositedAfter;

    balanceOfUserBefore = dummyERC20Token.balanceOf(user);
    balanceOfReserveBefore = dummyERC20Token.balanceOf(reserveH);
    depositedBefore = getDeposited(dummyERC20Token);

    require depositedBefore == balanceOfReserveBefore;
    //require e.msg.sender != 0;
    require reserveH.getPlugins(dummyERC20Token) == 0;

    deposit(e, dummyERC20Token, user, amtDeposited);
    //f(e,args);
    withdraw(e, dummyERC20Token, user, amtWithdrawn);

    require amtDeposited == amtWithdrawn;

    balanceOfUserAfter = dummyERC20Token.balanceOf(user);
    balanceOfReserveAfter = dummyERC20Token.balanceOf(reserveH);
    depositedAfter = getDeposited(dummyERC20Token);

    assert balanceOfUserBefore == balanceOfUserAfter;
    //assert balanceOfUserBefore + balanceOfReserveBefore == balanceOfUserAfter + balanceOfReserveAfter;
    //assert depositedAfter == depositedBefore + amtDeposited - amtWithdrawn;
}
