// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/frame.cvl
// Rule frame_comptroller original lines 138-153; SHA256 d46af148587537bdc1141ee7fef29b30a2615aa0ecc2f97b81a031eb396b5cfd
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
/*5fe3b567:*/ comptroller()                 returns address
}

frame_comptroller(method f)
description "$f may change value of comptroller()"
{
	env e0; havoc e0;
	env e1; havoc e1;
	env e2; havoc e2;
	static_require e1.block.number >= e0.block.number;
	static_require e2.block.number >= e1.block.number;

	address old = sinvoke comptroller(e0);
	calldataarg arg;
	invoke f(e1, arg);
	address new = sinvoke comptroller(e2);

	static_assert old == new;
}
