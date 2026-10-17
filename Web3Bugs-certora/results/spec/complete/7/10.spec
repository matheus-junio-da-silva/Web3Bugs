// Source: contracts/7/specs/AToken.spec
// Literal property: rule additiveBurn, lines 249-266
// Literal dependency source lines: 9;12-14;21;23;25;30;37-39;249-266
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
	handleAction(address, uint256, uint256) => NONDET 
	getReserveNormalizedIncome(address u) returns (uint256) => gRNI()
	balanceOf(address) returns (uint256) envfree
}

definition ray() returns uint = 1000000000000000000000000000;

definition bound() returns uint = ((gRNI() / ray()) + 1 ) / 2;

definition bounded_error_eq(uint x, uint y, uint scale) returns bool = x <= y + (bound() * scale) && x + (bound() * scale) >= y;

ghost gRNI() returns uint256 {
	axiom gRNI() == 7 * ray();
}

rule additiveBurn(address user1, address user2, address to1, address to2, uint256 x, uint256 y) 
{
	env e;
	uint256 indexRay = gRNI();
	require (user1 != user2 && to1 != to2 && user1 != to2 && user2 != to1 && 
	        (user1 == to1 <=> user2 == to2) &&
			 balanceOf(user1) == balanceOf(user2) && balanceOf(to1) == balanceOf(to2));
	require user1 != currentContract && user2 != currentContract;

	sinvoke burn(e, user1, to1, x, indexRay);
	sinvoke burn(e, user1, to1, y, indexRay);
	uint256 balanceUserScenario1 = balanceOf(user1);
	
	sinvoke burn(e, user2, to2, x+y, indexRay);
	uint256 balanceUserScenario2 = balanceOf(user2);
	
	assert 	bounded_error_eq(balanceUserScenario1, balanceUserScenario2, 3), "burn is not additive";
}
