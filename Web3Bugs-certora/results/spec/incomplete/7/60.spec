// Source: contracts/7/specs/VariableDebtToken.spec
// Literal property: invariant totalSupplyEqualsSumAllBalance, lines 40-50
// Literal dependency source lines: 1;3;5-6;8;10;13-15;23-29;32-34;36-38;40-50
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
	getReserveNormalizedVariableDebt(address asset) returns (uint256) => gRNVB()
    handleAction(address, uint256, uint256) => NONDET
    scaledBalanceOfToBalanceOf(uint256) returns (uint256) envfree
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

ghost sumAllBalance() returns uint256 {
    init_state axiom sumAllBalance() == 0;
}

hook Sstore _userState[KEY address a].balance uint128 balance (uint128 old_balance) STORAGE {
  havoc sumAllBalance assuming sumAllBalance@new() == sumAllBalance@old() + balance - old_balance;
}

invariant totalSupplyEqualsSumAllBalance(env e)
    totalSupply(e) == scaledBalanceOfToBalanceOf(sumAllBalance())
    filtered { f -> !f.isView && !disAllowedFunctions(f) }
    {
        preserved mint(address user, address onBehalfOf, uint256 amount, uint256 index) with (env e2) {
            require index == gRNVB();
        }
        preserved burn(address from, uint256 amount, uint256 index) with (env e3) {
            require index == gRNVB();
        }
    }
