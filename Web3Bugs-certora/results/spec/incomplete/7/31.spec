// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule integrityAndIndependencyOfIntSetters, lines 169-183
// Literal dependency source lines: 1;51-52;57;169-183
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    executeIntSetterById(uint256, uint256) envfree
    executeIntGetterById(uint256) returns uint256 envfree
}

rule integrityAndIndependencyOfIntSetters(uint256 funcId, uint256 otherFuncId, uint256 val) {
    
    require 0 <= funcId && funcId <= 10;
    require 0 <= otherFuncId && otherFuncId <= 10;
    uint256 valueBefore = executeIntGetterById(funcId);
    uint256 otherValueBefore = executeIntGetterById(otherFuncId);

    executeIntSetterById(funcId, val);

    uint256 valueAfter = executeIntGetterById(funcId);
    uint256 otherValueAfter = executeIntGetterById(otherFuncId);

    assert valueAfter == val;
    assert (otherFuncId != funcId => otherValueAfter == otherValueBefore);
}
