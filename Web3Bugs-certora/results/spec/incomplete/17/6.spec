// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/compound.cvl
// Rule _setMaxAssets original lines 235-266; SHA256 eaada7efa1edcaa79d4067d10e953fc20e3e7c71a13efd1f0131186f387a210b
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
/*d9226ced: */ _setMaxAssets(uint256) returns uint256
/*f851a440: */ admin() returns address
/*94b2294b: */ maxAssets() returns uint256
}

_setMaxAssets(address currentAdmin, uint newMaxAssets, uint oldMaxAssets)
description "Failed to set new maxAssets admin: $currentAdmin, new: $newMaxAssets, old: $old"
{
	// Free Variables
	env e0; havoc e0;
	env e1; havoc e1;
	env e2; havoc e2;

	// Strict ordering
	static_require e1.block > e0.block;
	static_require e2.block > e1.block;

	static_require oldMaxAssets == sinvoke maxAssets(e0);
	static_require currentAdmin == sinvoke admin(e0);

	// Invoke set new max assets
	uint256 result = sinvoke _setMaxAssets(e1, newMaxAssets);

	static_assert (
		(
			e1.msg.sender == currentAdmin &&
			result == 0 &&
			sinvoke maxAssets(e2) == newMaxAssets
		)
		||
		(
			e1.msg.sender != currentAdmin &&
			result != 0 &&
			sinvoke maxAssets(e2) == oldMaxAssets
		)
	);
}
