// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: independentQueuedActions
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	getDelay() returns (uint256) envfree 
	processMessageFromRoot(uint256, address, bytes)
	delegatecall(bytes) => NONDET
}

definition stateVariableUpdate(method f)
	returns bool = (
		f.selector == updateDelay(uint256).selector ||
		f.selector == updateGuardian(address).selector ||
		f.selector == updateGracePeriod(uint256).selector ||
		f.selector == updateMinimumDelay(uint256).selector ||
		f.selector == updateMaximumDelay(uint256).selector);

rule independentQueuedActions(method f) 
filtered{f -> stateVariableUpdate(f)}
{
	env e1; env e2; env e3;
	calldataarg args;
	calldataarg argsUpdate;
	
	// Assume different blocks (block3 later than block1)
	require e1.block.timestamp < e3.block.timestamp;
	require e1.msg.sender == e3.msg.sender;
	require e3.msg.value == 0;
	require e3.block.timestamp + getDelay() < max_uint;

	storage initState = lastStorage; 
	processMessageFromRoot(e3, args);

	// queue first set.
	processMessageFromRoot(e1, args) at initState;
	// Update some state variable changing method.
		f(e2, argsUpdate);
	// Try to queue second set, with same arguments.
	processMessageFromRoot@withrevert(e3, args);

	assert !lastReverted;
}
