// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/general.cvl
// Rule _setComptroller original lines 128-167; SHA256 b3bd08f5f815748fa73aca0665ae7a957d24f6035db1189d7a5205fda6323425
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
    admin() returns address
    _setComptroller(address) returns uint256
    comptroller() returns address
}

_setComptroller(address sender, address currAdmin, address currComptroller, address desiredComptroller, address nextComptroller)
    description "Failed to set comptroller: result=$result (sender=$sender, currAdmin=$currAdmin, currComptroller=$currComptroller, desiredComptroller=$desiredComptroller, nextComptroller=$nextComptroller)" {
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
    static_require currComptroller == sinvoke comptroller(e0);

    static_require sender == e1.msg.sender;

    // Invoke set new comptroller
    uint256 result = sinvoke _setComptroller(e1, desiredComptroller);

    static_require nextComptroller == sinvoke comptroller(e2);

    // nextComptroller == desiredComptroller <=> msg.sender == admin
    static_assert ((sender == currAdmin &&
                    result == 0 &&
                    nextComptroller == desiredComptroller)
                   ||
                   (sender != currAdmin &&
                    result == 1 && // UNAUTHORIZED
                    (
                     // It's possible that we're trying to set
                     // it to what it previously was. This is
                     // really the same as "succeeding," since
                     // it does become (remain) what you set it to.
                     desiredComptroller == currComptroller ||
                     nextComptroller != desiredComptroller
                     )));
}
