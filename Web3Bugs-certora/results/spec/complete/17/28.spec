// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/frame.cvl
// Rule frame_getAccountSnapshot original lines 172-189; SHA256 d46af148587537bdc1141ee7fef29b30a2615aa0ecc2f97b81a031eb396b5cfd
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
/*c37f68e2:*/ getAccountSnapshot(address)   returns uint256,uint256,uint256,uint256
}

frame_getAccountSnapshot(address a, method f)
description "$f may change value of getAccountSnapshot($a)"
{
	env e0; havoc e0;
	env e1; havoc e1;
	env e2; havoc e2;
	static_require e1.block.number >= e0.block.number;
	static_require e2.block.number >= e1.block.number;

	uint256 old1; uint256 old2; uint256 old3; uint256 old4;
	old1,old2,old3,old4 = sinvoke getAccountSnapshot(e0, a);
	calldataarg arg;
	invoke f(e1, arg);
	uint256 new1; uint256 new2; uint256 new3; uint256 new4;
	new1,new2,new3,new4 = sinvoke getAccountSnapshot(e2, a);

	static_assert old1 == new1 && old2 == new2 && old3 == new3 && old4 == new4;
}
