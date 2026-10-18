// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/frame.cvl
// Rule frame_borrowRatePerBlock original lines 121-136; SHA256 d46af148587537bdc1141ee7fef29b30a2615aa0ecc2f97b81a031eb396b5cfd
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
/*f8f9da28:*/ borrowRatePerBlock()          returns uint256
}

frame_borrowRatePerBlock(method f)
description "$f may change value of borrowRatePerBlock()"
{
	env e0; havoc e0;
	env e1; havoc e1;
	env e2; havoc e2;
	static_require e1.block.number >= e0.block.number;
	static_require e2.block.number >= e1.block.number;

	uint256 old = sinvoke borrowRatePerBlock(e0);
	calldataarg arg;
	invoke f(e1, arg);
	uint256 new = sinvoke borrowRatePerBlock(e2);

	static_assert old == new;
}
