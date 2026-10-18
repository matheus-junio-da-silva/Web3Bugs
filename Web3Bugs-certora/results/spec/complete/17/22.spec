// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/frame.cvl
// Rule frame_balanceOf original lines 70-85; SHA256 d46af148587537bdc1141ee7fef29b30a2615aa0ecc2f97b81a031eb396b5cfd
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
/*70a08231:*/ balanceOf(address) 			returns uint256
}

frame_balanceOf(address a, method f)
description "$f may change value of balanceOf($a)"
{
	env e0; havoc e0;
	env e1; havoc e1;
	env e2; havoc e2;
	static_require e1.block.number >= e0.block.number;
	static_require e2.block.number >= e1.block.number;

	uint256 old = sinvoke balanceOf(e0, a);
	calldataarg arg;
	invoke f(e1, arg);
	uint256 new = sinvoke balanceOf(e2, a);

	static_assert old == new;
}
