// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/compound.cvl
// Rule _acceptAdmin original lines 106-147; SHA256 eaada7efa1edcaa79d4067d10e953fc20e3e7c71a13efd1f0131186f387a210b
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
/*e9c714f2: */ _acceptAdmin() returns uint256
/*f851a440: */ admin() returns address
/*26782247: */ pendingAdmin() returns address
}

_acceptAdmin(address currentAdmin, address currentPendingAdmin, address newAdmin, address newPendingAdmin)
description "Failed to accept pending admin currentAdmin=$currentAdmin, currentPendingAdmin=$currentPendingAdmin, newPendingAdmin=$newPendingAdmin, newAdmin=$newAdmin"
{
	// Free Variables
	env e0; havoc e0;
	env e1; havoc e1;
	env e2; havoc e2;

	// Strict ordering
	static_require e1.block > e0.block;
	static_require e2.block > e1.block;

	static_require currentAdmin == sinvoke admin(e0);
	static_require currentPendingAdmin == sinvoke pendingAdmin(e0);

	// Invoke accept admin
	uint256 result = sinvoke _acceptAdmin(e1);

	static_require newAdmin == sinvoke admin(e2);
	static_require newPendingAdmin == sinvoke pendingAdmin(e2);

	// admin == pendingAdmin <=> msg.sender == pendingAdmin
	static_assert (
		(
			e1.msg.sender == currentPendingAdmin &&
			currentPendingAdmin != 0 &&
			result == 0 &&
			newAdmin == currentPendingAdmin &&
			newPendingAdmin == 0
		)
		||
		(
			(
				e1.msg.sender != currentPendingAdmin ||
				currentPendingAdmin == 0
			) &&
			result != 0 &&
			newAdmin == currentAdmin &&
			newPendingAdmin == currentPendingAdmin
		)
	);
}
