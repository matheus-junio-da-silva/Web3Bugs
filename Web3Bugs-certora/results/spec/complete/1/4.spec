// Extracted from: contracts/1/specs/PolygonBridge.spec
// Property: queuePriviliged
// Dependency status: complete
// CVL2 migration is intentionally out of scope for this catalog stage.
methods {
	processMessageFromRoot(uint256, address, bytes)
}

rule queuePriviliged()
{
	env e1;
	env e2;
	calldataarg args1;
	calldataarg args2;
	processMessageFromRoot(e1, args1);
	processMessageFromRoot@withrevert(e2, args2);
	assert e1.msg.sender != e2.msg.sender => lastReverted;
}
