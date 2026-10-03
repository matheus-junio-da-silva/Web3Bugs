// Extracted from: contracts/1/specs/Optimism_ArbitrumBridge.spec
// Property: executeRevertsBeforeDelay
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getDelay() returns (uint256) envfree 
	getActionsSetCount() returns(uint256) envfree
	getActionsSetExecutionTime(uint256) returns (uint256) envfree
	delegatecall(bytes) => NONDET
}

definition stateVariableUpdate(method f)
	returns bool = (
		f.selector == updateDelay(uint256).selector ||
		f.selector == updateGuardian(address).selector ||
		f.selector == updateGracePeriod(uint256).selector ||
		f.selector == updateMinimumDelay(uint256).selector ||
		f.selector == updateMaximumDelay(uint256).selector);

rule executeRevertsBeforeDelay(method f)
filtered{f -> stateVariableUpdate(f)}
{
	env e; 
	env e2;
	calldataarg args;
	calldataarg args2;
	uint256 actionsSetId = getActionsSetCount();
	uint256 delay = getDelay();
	queue2(e, args);

	uint256 execTime1 = getActionsSetExecutionTime(actionsSetId);
		f(e2, args2);
	uint256 execTime2 = getActionsSetExecutionTime(actionsSetId);

	execute@withrevert(e2, actionsSetId);

	assert 
		(e2.block.timestamp < e.block.timestamp + delay => lastReverted)
		&& (execTime2 == execTime1);
}
