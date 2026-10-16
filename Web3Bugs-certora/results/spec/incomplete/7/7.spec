// Historical extract: contracts/7/specs/AToken.spec:147-171
// Source preamble: contracts/7/specs/AToken.spec:1-44
// Dependency status: incomplete; CVL2 migration intentionally not attempted.
/**

- values of gRNI passing: ray, 2 * ray

*/

using SimpleERC20 as _underlyingAsset

methods { 
    nonces(address) returns (uint256) envfree
    allowance(address, address) returns (uint256) envfree
	handleAction(address, uint256, uint256) => NONDET 
	getReserveNormalizedIncome(address u) returns (uint256) => gRNI()
	balanceOf(address) returns (uint256) envfree
	additionalData(address) returns uint128 envfree
	finalizeTransfer(address, address, address, uint256, uint256, uint256) => NONDET

	scaledTotalSupply() returns (uint256)
	scaledBalanceOf(address) returns (uint256)
    scaledBalanceOfToBalanceOf(uint256)returns (uint256) envfree
}

definition ray() returns uint = 1000000000000000000000000000;
definition half_ray() returns uint = ray() / 2;
definition bound() returns uint = ((gRNI() / ray()) + 1 ) / 2;

/*
Due to rayDiv and RayMul Rounding (+ 0.5) - blance could increase by (gRNI() / Ray() + 1) / 2.
*/
definition bounded_error_eq(uint x, uint y, uint scale) returns bool = x <= y + (bound() * scale) && x + (bound() * scale) >= y;

ghost sumAllBalance() returns uint256 {
    init_state axiom sumAllBalance() == 0;
}

// summerization for scaledBlanaceOf -> regularBalanceOf + 0.5 (canceling the rayMul)
ghost gRNI() returns uint256 {
	axiom gRNI() == 7 * ray();
}

hook Sstore _userState[KEY address a].balance uint128 balance (uint128 old_balance) STORAGE {
    havoc sumAllBalance assuming sumAllBalance@new() == sumAllBalance@old() + balance - old_balance;
}

rule integrityTransfer(address from, address to, uint256 amount)
{
	env e;
	require e.msg.sender == from;
	address other; // for any address including from, to, currentContract the underlying asset balance should stay the same
	
	uint256 balanceBeforeFrom = balanceOf(from);
	uint256 balanceBeforeTo = balanceOf(to);
	uint256 underlyingBeforeOther =  _underlyingAsset.balanceOf(e, other);
	
	transfer(e, to, amount);
	
	uint256 balanceAfterFrom = balanceOf(from);
	uint256 balanceAfterTo = balanceOf(to);
	uint256 underlyingAfterOther =  _underlyingAsset.balanceOf(e, other);
	
	assert underlyingAfterOther == underlyingBeforeOther, "unexpected change in underlying asserts";
	
	if (from != to) {
		assert bounded_error_eq(balanceAfterFrom, balanceBeforeFrom - amount, 1) &&
	 		bounded_error_eq(balanceAfterTo, balanceBeforeTo + amount, 1), "unexpected balance of from/to, when from!=to";
	} else {
		assert balanceAfterFrom == balanceAfterTo , "unexpected balance of from/to, when from==to";
	}
}
