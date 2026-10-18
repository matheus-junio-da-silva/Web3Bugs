// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/general.cvl
// Rule _setPendingAdmin original lines 12-44; SHA256 b3bd08f5f815748fa73aca0665ae7a957d24f6035db1189d7a5205fda6323425
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
    _setPendingAdmin(address) returns uint256
    pendingAdmin() returns address
    admin() returns address
}

_setPendingAdmin(address currentAdmin, address currentPendingAdmin, address newPendingAdmin)
description "Failed to set new pending admin $currentPendingAdmin to $newPendingAdmin (admin=$currentAdmin)"
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

    // Invoke set new pending admin
    uint256 result = sinvoke _setPendingAdmin(e1, newPendingAdmin);

    // pendingAdmin changes <=> msg.sender == currentAdmin
    static_assert (
                   (
                    e1.msg.sender == currentAdmin &&
                    result == 0 &&
                    sinvoke pendingAdmin(e2) == newPendingAdmin
                    )
                   ||
                   (
                    e1.msg.sender != currentAdmin &&
                    result != 0 &&
                    sinvoke pendingAdmin(e2) == currentPendingAdmin
                    )
                   );
}
