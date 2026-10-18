// Source: contracts/7/specs/AToken.spec
// Literal property: invariant totalSupplyEqualsSumAllBalance, lines 45-55
// Literal dependency source lines: 9;12-13;20-21;23;32-34;37-39;41-43;45-55
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
	handleAction(address, uint256, uint256) => NONDET 
	getReserveNormalizedIncome(address u) returns (uint256) => gRNI()
    scaledBalanceOfToBalanceOf(uint256)returns (uint256) envfree
}

definition ray() returns uint = 1000000000000000000000000000;

ghost sumAllBalance() returns uint256 {
    init_state axiom sumAllBalance() == 0;
}

ghost gRNI() returns uint256 {
	axiom gRNI() == 7 * ray();
}

hook Sstore _userState[KEY address a].balance uint128 balance (uint128 old_balance) STORAGE {
    havoc sumAllBalance assuming sumAllBalance@new() == sumAllBalance@old() + balance - old_balance;
}

invariant totalSupplyEqualsSumAllBalance(env e)
    totalSupply(e) == scaledBalanceOfToBalanceOf(sumAllBalance())
    filtered { f -> !f.isView }
    {
        preserved mint(address caller, address onBehalfOf, uint256 amount, uint256 index) with (env e2) {
            require index == gRNI();
        }
        preserved burn(address from, address receiverOfUnderlying, uint256 amount, uint256 index) with (env e3) {
            require index == gRNI();
        }
    }
