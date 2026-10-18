// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/bentobox.spec:226-265 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenA

using DummyWeth as wethTokenImpl

using SymbolicStrategy as strategyInstance

using Borrower as borrower

methods {
	balanceOf(address) => DISPATCHER(true) 
	harvest(uint256 balance, address sender) => DISPATCHER(true)  
	harvest(uint256 balance) => DISPATCHER(true)
	totalTokenAmount(address token) returns (uint128) envfree
	totalTokenShare(address token) returns (uint128) envfree
	tokenBalanceOfUser(address token, address user) returns (uint256) envfree // external balanceOf
	balanceOf(address token, address account) returns (uint256) envfree // internal balanceOf
	toAmount(address token, uint256 share, bool roundUp) returns (uint256) envfree
	harnessFrom() returns (address) envfree
	transfer(address to, uint256 amount) => DISPATCHER(true)
	wethTokenImpl.deposit() => DISPATCHER(true)
	wethTokenImpl.withdraw(uint256 amount) => DISPATCHER(true)
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

rule preserveTotalAssetsOfUser(address token, address from, address to,
					    	   address user, uint256 amount, uint256 share,
							   method f) {
	env e;

	// verifying a simplified version
	require totalTokenAmount(token) == totalTokenShare(token);

	uint256 _userShares = balanceOf(token, user);

	// roundUp = true or false shouldn't matter as long as they are consistent
	mathint _userAssets = tokenBalanceOfUser(token, user) + toAmount(token, balanceOf(token, user), true); 

	require user != currentContract &&  user == from && user == harnessFrom() && user == to;
	//for transfermultiple we assume that all transfer are to the same user
	callFunctionWithParams(token, from, to, amount, share, f);

	// roundUp = true or false shouldn't matter as long as they are consistent
	mathint userAssets_ = tokenBalanceOfUser(token, user) + toAmount(token, balanceOf(token, user), true);

	uint256 userShares_ = balanceOf(token, user);
	
	// transferMultiple transfer from user to some arbitrary other user so we expect assets to be preserved
	require  f.selector != transferMultiple(address,address,address[],uint256[]).selector; 
	
	// flash loan can reduce asset of user due to fee, and strategy can also reduce user assets due to negative profit
	if (f.selector != 0xf1676d37 && // hascode of flashLoan 
		f.selector != setStrategy(address,address).selector &&
		f.selector != harvest(address,bool,uint256).selector)
	{
		assert (_userAssets <= userAssets_,
			"total user assets not preserved");
	}
	else  {
		// however on those functions, a user's share should not change
		assert (_userShares == userShares_,
			"total user assets not preserved");
	}
	
}
