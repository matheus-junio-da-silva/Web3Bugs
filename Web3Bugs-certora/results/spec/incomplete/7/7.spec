// Source: contracts/7/specs/AToken.spec
// Literal property: rule integrityTransfer, lines 147-171
// Literal dependency source lines: 7;9;12-14;16;21;23;25;30;37-39;147-171
// Historical syntax retained; no reconstruction or CVL2 migration.

using SimpleERC20 as _underlyingAsset

methods {
	handleAction(address, uint256, uint256) => NONDET 
	getReserveNormalizedIncome(address u) returns (uint256) => gRNI()
	balanceOf(address) returns (uint256) envfree
	finalizeTransfer(address, address, address, uint256, uint256, uint256) => NONDET
}

definition ray() returns uint = 1000000000000000000000000000;

definition bound() returns uint = ((gRNI() / ray()) + 1 ) / 2;

definition bounded_error_eq(uint x, uint y, uint scale) returns bool = x <= y + (bound() * scale) && x + (bound() * scale) >= y;

ghost gRNI() returns uint256 {
	axiom gRNI() == 7 * ray();
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
