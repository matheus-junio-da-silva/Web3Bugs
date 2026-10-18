// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/frame.cvl
// Rule frame_isCToken original lines 242-257; SHA256 d46af148587537bdc1141ee7fef29b30a2615aa0ecc2f97b81a031eb396b5cfd
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
/*fe9c44ae:*/ isCToken()                    returns bool
}

frame_isCToken(method f)
description "$f may change value of isCToken()"
{
	env e0; havoc e0;
	env e1; havoc e1;
	env e2; havoc e2;
	static_require e1.block.number >= e0.block.number;
	static_require e2.block.number >= e1.block.number;

	bool old = sinvoke isCToken(e0);
	calldataarg arg;
	invoke f(e1, arg);
	bool new = sinvoke isCToken(e2);

	static_assert old == new;
}
