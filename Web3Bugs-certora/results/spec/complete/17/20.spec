// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/general.cvl
// Rule invariantRequireAdminToChangeAdmin original lines 90-126; SHA256 b3bd08f5f815748fa73aca0665ae7a957d24f6035db1189d7a5205fda6323425
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
    _setPendingAdmin(address) returns uint256
    pendingAdmin() returns address
    _acceptAdmin() returns uint256
    admin() returns address
}

invariantRequireAdminToChangeAdmin(address caller, address currentAdmin, address currentPendingAdmin, address desiredAdmin, address newAdmin, address newPendingAdmin)
    description "Failed to prove that required to be admin to change admin (caller=$caller, currentAdmin=$currentAdmin, currentPendingAdmin=$currentPendingAdmin, desiredAdmin=$desiredAdmin, newAdmin=$newAdmin, newPendingAdmin=$newPendingAdmin)"
{
    // Free Variables
    env e0; havoc e0;
    env e1; havoc e1;
    env e2; havoc e2;
    env e3; havoc e3;

    // Strict ordering (TODO: Can e2.block == e1.block?)
    static_require e1.block > e0.block;
    static_require e2.block > e1.block;
    static_require e3.block > e2.block;

    static_require currentAdmin == sinvoke admin(e0);
    static_require currentPendingAdmin == sinvoke pendingAdmin(e0);

    // Start with a zero admin
    static_require currentPendingAdmin == 0;

    static_require caller == e1.msg.caller;

    // Invoke set new pending admin
    uint256 result0 = sinvoke _setPendingAdmin(e1, desiredAdmin);
    uint256 result1 = sinvoke _acceptAdmin(e2);

    static_require newAdmin == sinvoke admin(e3);
    static_require newPendingAdmin == sinvoke pendingAdmin(e3);

    static_assert (
                   e1.msg.sender == currentAdmin ||
                   (
                    newAdmin == currentAdmin &&
                    newPendingAdmin == currentPendingAdmin
                    )
                   );
}
