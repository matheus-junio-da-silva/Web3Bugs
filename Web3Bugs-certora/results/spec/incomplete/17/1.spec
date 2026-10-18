// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/compound.cvl
// Rule _setOriginationFee original lines 38-70; SHA256 eaada7efa1edcaa79d4067d10e953fc20e3e7c71a13efd1f0131186f387a210b
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
/*24021127: */ _setOriginationFee(uint256) returns uint256
/*f851a440: */ admin() returns address
/*b8bb5c42: */ originationFee() returns uint256
}

_setOriginationFee(uint currentAdmin, uint currentFee, uint newOriginationFee)
description "Failed to set origination fee from $currentFee to $newOriginationFee (admin=$currentAdmin)" {
	// Free Variables
	env e0; havoc e0;
	env e1; havoc e1;
	env e2; havoc e2;

	// Strict ordering
	static_require e1.block > e0.block;
	static_require e2.block > e1.block;

	// Capture current admin and origination fee
	static_require currentAdmin == sinvoke admin(e0);
	static_require currentFee == sinvoke originationFee(e0);

	// Invoke set origination fee
	uint256 result = sinvoke _setOriginationFee(e1, newOriginationFee);

	// originationFee changes <=> msg.sender == currentAdmin
	static_assert (
		(
			e1.msg.sender == currentAdmin &&
			result == 0 &&
			sinvoke originationFee(e2) == newOriginationFee
		)
		||
		(
			e1.msg.sender != currentAdmin &&
			result != 0 &&
			sinvoke originationFee(e2) == currentFee
		)
	);
}
