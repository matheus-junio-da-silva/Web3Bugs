// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/general.cvl
// Rule _acceptAdmin original lines 46-87; SHA256 b3bd08f5f815748fa73aca0665ae7a957d24f6035db1189d7a5205fda6323425
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
    pendingAdmin() returns address
    _acceptAdmin() returns uint256
    admin() returns address
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
