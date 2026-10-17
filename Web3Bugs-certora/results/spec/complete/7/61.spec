// Source: contracts/7/specs/VariableDebtToken.spec
// Literal property: rule whoChangeTotalSupply, lines 54-66
// Literal dependency source lines: 1;3;5;8;10;13-15;23-29;54-66
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
	getReserveNormalizedVariableDebt(address asset) returns (uint256) => gRNVB()
    handleAction(address, uint256, uint256) => NONDET
}

definition ray() returns uint = 1000000000000000000000000000;

ghost gRNVB() returns uint256 {
	axiom gRNVB() == 7 * ray();
}

definition disAllowedFunctions(method f) returns bool = 
            f.selector == transfer(address, uint256).selector ||
            f.selector == allowance(address, address).selector ||
            f.selector == approve(address, uint256).selector ||
            f.selector == transferFrom(address, address, uint256).selector ||
            f.selector == increaseAllowance(address, uint256).selector ||
            f.selector == decreaseAllowance(address, uint256).selector;

rule whoChangeTotalSupply(method f) 
    filtered { f ->  !f.isView && !disAllowedFunctions(f) } 
{
    env e;
    uint256 oldTotalSupply = totalSupply(e);
    calldataarg args;
    f(e, args);
    uint256 newTotalSupply = totalSupply(e);
    assert oldTotalSupply != newTotalSupply => 
           (e.msg.sender == POOL(e) && 
           (f.selector == burn(address, uint256, uint256).selector || 
            f.selector == mint(address, address, uint256, uint256).selector));
}
