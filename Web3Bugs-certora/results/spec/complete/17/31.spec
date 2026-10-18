// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/frame.cvl
// Rule frame_interestRateModel original lines 225-240; SHA256 d46af148587537bdc1141ee7fef29b30a2615aa0ecc2f97b81a031eb396b5cfd
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
/*f3fdb15a:*/ interestRateModel()           returns address
}

frame_interestRateModel(method f)
description "$f may change value of interestRateModel()"
{
	env e0; havoc e0;
	env e1; havoc e1;
	env e2; havoc e2;
	static_require e1.block.number >= e0.block.number;
	static_require e2.block.number >= e1.block.number;

	address old = sinvoke interestRateModel(e0);
	calldataarg arg;
	invoke f(e1, arg);
	address new = sinvoke interestRateModel(e2);

	static_assert old == new;
}
