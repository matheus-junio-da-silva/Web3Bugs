// Source: contracts/7/specs/UserConfiguration.spec
// Literal property: rule setBorrowing, lines 20-24
// Literal dependency source lines: 1-2;5;16;20-24
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setBorrowing(uint256, bool) envfree
    isBorrowing(uint256) returns bool envfree
}

rule setBorrowing(uint256 reserveIndex, bool borrowing)
{	
	setBorrowing(reserveIndex, borrowing);
	assert isBorrowing(reserveIndex) == borrowing, "unexpected result";
}
