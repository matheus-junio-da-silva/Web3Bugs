// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule integrityAndIndependencyOfBoolSetters, lines 186-200
// Literal dependency source lines: 1;55-57;186-200
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    executeBoolSetterById(uint256, bool) envfree
    executeBoolGetterById(uint256) returns bool envfree
}

rule integrityAndIndependencyOfBoolSetters(uint256 funcId, uint256 otherFuncId, bool val) {
    
    require 0 <= funcId && funcId <= 10;
    require 0 <= otherFuncId && otherFuncId <= 10;
    bool valueBefore = executeBoolGetterById(funcId);
    bool otherValueBefore = executeBoolGetterById(otherFuncId);
    
    executeBoolSetterById(funcId, val);

    bool valueAfter = executeBoolGetterById(funcId);
    bool otherValueAfter = executeBoolGetterById(otherFuncId);

    assert valueAfter == val;
    assert (otherFuncId != funcId => otherValueAfter == otherValueBefore);
}
