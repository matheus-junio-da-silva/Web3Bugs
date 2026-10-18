// Project 20 - Sushi BentoBox, historical CVL; no CVL2 migration.
// Source: contracts/20/spec/bentobox.spec:152-173 (literal property below)
// Target-specific execution context recorded in companion documentation.
using DummyERC20A as tokenA

using DummyWeth as wethTokenImpl

using SymbolicStrategy as strategyInstance

using Borrower as borrower

methods {
	balanceOf(address) => DISPATCHER(true) 
	wethTokenImpl.deposit() => DISPATCHER(true)
	balanceOf(address token, address account) returns (uint256) envfree // internal balanceOf
}

definition MAX_UINT256() returns uint256 =
	0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;

rule additivity(uint x, uint y, address token, address who) {
	env e;
	storage init = lastStorage;
	address from = e.msg.sender;
	require e.msg.value == 0;
	
	deposit(e, token, from, who, 0, x);
	deposit(e, token, from, who, 0, y);
	
	uint256 splitScenarioBalanceWho = balanceOf(token, who);
	uint256 splitScenarioBalanceSender = balanceOf(token, from);
		
	require x + y <= MAX_UINT256();
	uint256 sum = x + y;
	deposit(e, token, from, who, 0, sum) at init;
	
	uint256 sumScenarioBalanceWho = balanceOf(token, who);
	uint256 sumScenarioBalanceSender = balanceOf(token, from);
	
	assert sumScenarioBalanceWho == splitScenarioBalanceWho, "function is not additive for argument address";
	assert sumScenarioBalanceSender == splitScenarioBalanceSender, "function is not additive for sender";
}
