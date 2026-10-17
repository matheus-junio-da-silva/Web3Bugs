// Source: contracts/7/specs/AToken.spec
// Literal property: rule additiveTransfer, lines 178-201
// Literal dependency source lines: 9;12-14;16;21;23;25;30;37-39;178-201
// Historical syntax retained; no reconstruction or CVL2 migration.

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

rule additiveTransfer(address from1, address from2, address to1, address to2, uint256 x, uint256 y)
{
	env e1;
	env e2;
    uint256 indexRay = gRNI();
	require (from1 != from2 && to1 != to2 && from1 != to2 && from2 != to1 && 
	        (from1 == to1 <=> from2 == to2) &&
			 balanceOf(from1) == balanceOf(from2) && balanceOf(to1) == balanceOf(to2));

	require e1.msg.sender == from1;
	require e2.msg.sender == from2;
	transfer(e1, to1, x);
	transfer(e1, to1, y);
	uint256 balanceFromScenario1 = balanceOf(from1);
	uint256 balanceToScenario1 = balanceOf(to1);

	transfer(e2, to2, x+y);
	
	uint256 balanceFromScenario2 = balanceOf(from2);
	uint256 balanceToScenario2 = balanceOf(to2);
	
	assert 	bounded_error_eq(balanceFromScenario1, balanceFromScenario2, 3)  &&
	 		bounded_error_eq(balanceToScenario1, balanceToScenario2, 3), "transfer is not additive";
}
