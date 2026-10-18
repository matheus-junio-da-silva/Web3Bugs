// Source: contracts/7/specs/AToken.spec
// Literal property: rule mintArgsPositive, lines 68-74
// Literal dependency source lines: 9;21;68-74
// Historical syntax retained; no reconstruction or CVL2 migration.

rule mintArgsPositive(address user, uint256 amount, uint256 index) 
{
    env e;
	address caller;
    mint@withrevert(e, caller, user, amount, index);
    assert amount == 0 => lastReverted;
}
