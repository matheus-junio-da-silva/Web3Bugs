// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/bentobox.spec:93-130 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenA

using DummyWeth as wethTokenImpl

using SymbolicStrategy as strategyInstance

using Borrower as borrower

methods {
	strategyInstance.token() returns address envfree
	strategyInstance.owner() returns address envfree
	totalTokenAmount(address token) returns (uint128) envfree
	tokenBalanceOf(address token) returns (uint256) envfree
	tokenBalanceOfUser(address token, address user) returns (uint256) envfree // external balanceOf
	harnessBorrower() returns (address) envfree
	harnessToken() returns (address) envfree
	strategy(address) returns (address) envfree
	getStrategyTokenBalance(address token) returns (uint256) envfree
	transfer(address to, uint256 amount) => DISPATCHER(true)
	wethTokenImpl.deposit() => DISPATCHER(true)
	wethTokenImpl.withdraw(uint256 amount) => DISPATCHER(true)
	harvest(uint256 balance, address sender) => DISPATCHER(true)  
	harvest(uint256 balance) => DISPATCHER(true)
	withdraw(uint256 amount, uint256 balance) => DISPATCHER(true)
}

function callFunctionWithParams(address token, address from, address to,
 								uint256 amount, uint256 share, method f) {
	env e;

	if (f.selector == deposit(address, address, address, uint256, uint256).selector) {
		deposit(e, token, from, to, amount, share);
	} else if (f.selector == withdraw(address, address, address, uint256, uint256).selector) {
		withdraw(e, token, from, to, amount, share); 
	} else if  (f.selector == transfer(address, address, address, uint256).selector) {
		transfer(e, token, from, to, share);
	} else if (f.selector == setStrategy(address, address).selector) {
		address newStra;
		setStrategy(e, token, newStra);
	} else if (f.selector == harvest(address, bool, uint256).selector) {
		bool balance;
		uint256 maxChangeAmount;
		harvest(e, token, balance, maxChangeAmount);
	} else {
		calldataarg args;
		f(e,args);
	}
}

rule solvency(address token, address from, address to,
								  uint256 amount, uint256 share, method f,
								  uint256 _strategy,
								  uint256 strategy_,
								  address straToken,
								  uint256 _systemBalance,
								  uint256 systemBalance_,
								  uint256 _strategyBalance,
								  uint256 strategyBalance_  ) {
	//link the strategy to the current token
	require strategyInstance.token() == token;
	// link the strategy owner to the bentobox
	require strategyInstance.owner() == currentContract;
	require harnessBorrower() == borrower;
	require harnessToken() == token;

	mathint _actual = tokenBalanceOf(token); //casting form uint256
	require _systemBalance == tokenBalanceOfUser(token, currentContract);
	mathint _asElastic = totalTokenAmount(token); //casting from uint128

	require _actual == _asElastic;
	require _strategy == getStrategyTokenBalance(token);
	
	require straToken == strategy(token);
	//proven in zeroStrategy
	require straToken == 0 => _strategy == 0;
	require _strategyBalance == tokenBalanceOfUser(token, straToken);

	env e;
	calldataarg args;
	callFunctionWithParams(token, from, to, amount, share, f);

	mathint actual_ = tokenBalanceOf(token); //casting form uint256
	require systemBalance_ == tokenBalanceOfUser(token, currentContract);
	mathint asElastic_ = totalTokenAmount(token); //casting from uint128
	require strategy_ == getStrategyTokenBalance(token);
	assert actual_ >= asElastic_, "system solvency is broken";
}
