// Source: contracts/7/specs/UserConfiguration.spec
// Literal property: rule integrityOfIsolationModeState, lines 142-147
// Literal dependency source lines: 1;7;12;16;142-147
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
	isUsingAsCollateralOne() returns bool envfree
    getIsolationModeState() returns (bool, address, uint256) envfree
}

rule integrityOfIsolationModeState(){
    bool existExactlyOneCollateral = isUsingAsCollateralOne();
    bool answer; address asset; uint256 ceiling;
    answer, asset, ceiling = getIsolationModeState();
    assert answer => existExactlyOneCollateral;
}
