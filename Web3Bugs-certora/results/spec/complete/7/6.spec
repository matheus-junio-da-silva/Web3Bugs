// Source: contracts/7/specs/AToken.spec
// Literal property: rule additiveMint, lines 125-140
// Literal dependency source lines: 9;12-14;21;23;25;30;37-39;125-140
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

rule additiveMint(address a, address b, address c, uint256 x, uint256 y) 
{
	env e;
	uint256 indexRay = gRNI();
	require(balanceOf(a) == balanceOf(b) && a != b);
	uint256 balanceScenario0 = balanceOf(a);
	// storage initialStorage = lastStorage;
	mint(e,c,a,x,indexRay);
	mint(e,c,a,y,indexRay);
	uint256 balanceScenario1 = balanceOf(a);
	// mint(e,c, a, x+y ,indexRay) at initialStorage;
	mint(e, c, b, x+y ,indexRay);

	uint256 balanceScenario2 = balanceOf(b);
	assert bounded_error_eq(balanceScenario1, balanceScenario2, 3), "mint is not additive";
}
