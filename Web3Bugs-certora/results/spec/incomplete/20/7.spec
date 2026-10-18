// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/bentobox.spec:199-215 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenA

using DummyWeth as wethTokenImpl

using SymbolicStrategy as strategyInstance

using Borrower as borrower

methods {
	balanceOf(address) => DISPATCHER(true) 
	balanceOf(address token, address account) returns (uint256) envfree // internal balanceOf
	harnessOther() returns (address) envfree
	harnessFrom() returns (address) envfree
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

rule noChangeToOthersBalances(address token, address from, address to,
 							  address other, uint256 amount,
							  uint256 share, method f) {
	require from != other && to != other && other == harnessOther() &&
	from == harnessFrom();

	env e;

	uint256 _otherInternalBalance = balanceOf(token, other); // user's internal shares

	callFunctionWithParams(token, from, to, amount, share, f);

	uint256 otherInternalBalance_ = balanceOf(token, other);

	assert (_otherInternalBalance <= otherInternalBalance_ ),
								"operation changed some other user's balance";
}
