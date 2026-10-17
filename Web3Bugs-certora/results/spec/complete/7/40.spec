// Source: contracts/7/specs/StableDebtToken.spec
// Literal property: rule whoChangeTotalSupply, lines 211-223
// Literal dependency source lines: 1-2;5;8-10;12;14-20;22-42;44-83;85-103;211-223
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    calculateCompoundedInterest(uint256 r, uint40 t0, uint256 t1) returns (uint256) => calculateCompoundedInterestSummary(r, t0, t1)
	handleAction(address, uint256, uint256) => NONDET
	rayMul(uint256 x, uint256 y) returns (uint256) => rayMulSummariztion(x, y)
	rayDiv(uint256 x, uint256 y) returns (uint256) => rayDivSummariztion(x, y)
}

definition RAY() returns uint = 1000000000000000000000000000;

definition disAllowedFunctions(method f) returns bool = 
            f.selector == transfer(address, uint256).selector ||
            f.selector == allowance(address, address).selector ||
            f.selector == approve(address, uint256).selector ||
            f.selector == transferFrom(address, address, uint256).selector ||
            f.selector == increaseAllowance(address, uint256).selector ||
            f.selector == decreaseAllowance(address, uint256).selector;

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

rule whoChangeTotalSupply(method f)
    filtered { f ->  !f.isView && !disAllowedFunctions(f) }
{
    env e;
    uint256 oldTotalSupply = totalSupply(e);
    calldataarg args;
    f(e, args);
    uint256 newTotalSupply = totalSupply(e);
    assert oldTotalSupply != newTotalSupply => 
           (e.msg.sender == POOL(e) && 
           (f.selector == burn(address, uint256).selector || 
            f.selector == mint(address, address, uint256, uint256).selector));
}
