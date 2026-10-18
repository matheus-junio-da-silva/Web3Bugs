// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/compound.cvl
// Rule _setOracle original lines 188-233; SHA256 eaada7efa1edcaa79d4067d10e953fc20e3e7c71a13efd1f0131186f387a210b
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
/*3be59443: */ _setOracle(address) returns uint256
/*f851a440: */ admin() returns address
/*7dc0d1d0: */ oracle() returns address
}

_setOracle(address sender, address currAdmin, address currOracle, address desiredOracle, address nextOracle)
description "Failed to set oracle (sender=$sender, currAdmin=$currAdmin, currOracle=$currOracle, desiredOracle=$desiredOracle, nextOracle=$nextOracle)" {
	// N.B. This merely havocs `oracleInterface.assetPrices(address(0))`
	//      and does not check or concern itself with the result.

	// Free Variables
	env e0; havoc e0;
	env e1; havoc e1;
	env e2; havoc e2;

	// Strict ordering
	static_require e1.block > e0.block;
	static_require e2.block > e1.block;

	static_require currAdmin == sinvoke admin(e0);
	static_require currOracle == sinvoke oracle(e0);

	static_require sender == e1.msg.sender;

	// Invoke set new pending admin
	uint256 result = sinvoke _setOracle(e1, desiredOracle);

	static_require nextOracle == sinvoke oracle(e2);

	// nextOracle == desiredOracle <=> msg.sender == admin
	static_assert (
		(
			sender == currAdmin &&
			result == 0 &&
			nextOracle == desiredOracle
		)
		||
		(
			sender != currAdmin &&
			result != 0 &&
			(
				// It's possible that we're trying to set
				// it to what it previously was. This is
				// really the same as "succeeding," since
				// it does become (remain) what you set it to.
				desiredOracle == currOracle ||
				nextOracle != desiredOracle
			)
		)
	);
}
