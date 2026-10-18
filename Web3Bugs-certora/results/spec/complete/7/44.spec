// Source: contracts/7/specs/StableDebtToken.spec
// Literal property: rule burnZeroDoesntChangeBalance, lines 281-287
// Literal dependency source lines: 1-2;5;8-10;12;22-42;44-83;85-103;281-287
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    calculateCompoundedInterest(uint256 r, uint40 t0, uint256 t1) returns (uint256) => calculateCompoundedInterestSummary(r, t0, t1)
	handleAction(address, uint256, uint256) => NONDET
	rayMul(uint256 x, uint256 y) returns (uint256) => rayMulSummariztion(x, y)
	rayDiv(uint256 x, uint256 y) returns (uint256) => rayDivSummariztion(x, y)
}

definition RAY() returns uint = 1000000000000000000000000000;

ghost mapping(uint256 => mapping(uint256 => uint256)) calculateCompoundedInterestSummaryValues;

function calculateCompoundedInterestSummary(uint256 rate, uint40 t0, uint256 t1) returns uint256
{
	uint256 deltaT = t1 - t0;
	if (deltaT == 0)
	{
		return RAY();
	}
	if (rate == RAY())
	{
		return RAY();
	}
	if (rate >= RAY())
	{
		require calculateCompoundedInterestSummaryValues[rate][deltaT] >= rate;
	}
	else{
		require calculateCompoundedInterestSummaryValues[rate][deltaT] < rate;
	}
	return calculateCompoundedInterestSummaryValues[rate][deltaT];
}

ghost mapping(uint256 => mapping(uint256 => uint256)) rayMulSummariztionValues;

function rayMulSummariztion(uint256 x, uint256 y) returns uint256
{
	if (x == 0) || (y == 0)
	{
		return 0;
	}
	if (x == RAY())
	{
		return y;
	}
	if (y == RAY())
	{
		return x;
	}
	
	if (y > x)
	{
		if (y > RAY())
		{
			require rayMulSummariztionValues[y][x] >= x;
		}
		if (x > RAY())
		{
			require rayMulSummariztionValues[y][x] >= y;
		}
		return rayMulSummariztionValues[y][x];
	}
	else{
		if (x > RAY())
		{
			require rayMulSummariztionValues[x][y] >= y;
		}
		if (y > RAY())
		{
			require rayMulSummariztionValues[x][y] >= x;
		}
		return rayMulSummariztionValues[x][y];
	}
}

ghost mapping(uint256 => mapping(uint256 => uint256)) rayDivSummariztionValues;

function rayDivSummariztion(uint256 x, uint256 y) returns uint256
{
	if (x == 0)
	{
		return 0;
	}
	if (y == RAY())
	{
		return x;
	}
	if (y == x)
	{
		return RAY();
	}
	require y > RAY() => rayDivSummariztionValues[x][y] <= x;
	// require y < RAY() => rayDivSummariztionValues[x][y] =< x;
	return rayDivSummariztionValues[x][y];
}

rule burnZeroDoesntChangeBalance(address u) {
	env e;
	uint256 balanceBefore = balanceOf(e, u);
	burn(e, u, 0);
	uint256 balanceAfter = balanceOf(e, u);
	assert balanceBefore == balanceAfter;
}
