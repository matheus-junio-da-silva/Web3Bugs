// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/bentobox.spec:182-197 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenA

using DummyWeth as wethTokenImpl

using SymbolicStrategy as strategyInstance

using Borrower as borrower

methods {
	balanceOf(address) => DISPATCHER(true) 
	transfer(address to, uint256 amount) => DISPATCHER(true)
	wethTokenImpl.withdraw(uint256 amount) => DISPATCHER(true)
	withdraw(uint256 amount, uint256 balance) => DISPATCHER(true)
	balanceOf(address token, address account) returns (uint256) envfree // internal balanceOf
	harnessFrom() returns (address) envfree
	wethTokenImpl.deposit() => DISPATCHER(true)
	harvest(uint256 balance, address sender) => DISPATCHER(true)  
	harvest(uint256 balance) => DISPATCHER(true)
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

rule validDecreaseToBalanceOf(address token, address a,
							  address from, address to,
 							  address other, method f) {

	uint256 amount;
	uint256 share;
 	require  from == harnessFrom();

	uint256 vBefore = balanceOf(token, a);
	callFunctionWithParams(token, from, to, amount, share, f);
	uint256 vAfter = balanceOf(token, a);
	assert (vBefore > vAfter => ( from == a && (
	 		f.selector == transfer(address, address, address, uint256).selector ||
			f.selector == withdraw(address, address, address, uint256, uint256).selector ||
			f.selector == transferMultiple(address, address, address[], uint256[]).selector)));
}
