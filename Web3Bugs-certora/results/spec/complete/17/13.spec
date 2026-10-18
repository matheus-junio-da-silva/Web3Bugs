// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/mintAndRedeemFresh.cvl
// Rule mintThenRedeem original lines 402-423; SHA256 9f82ecafa2fef187349021f4707b2471433cdc53a644052c3135fc54e5303c45
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
        mintFreshPub(address,uint256) returns uint256
        redeemFreshPub(address,uint256,uint256) returns uint256
        getCash() returns uint256
}

mintThenRedeem(address account, uint256 amountUnderlying)
description "Mint and redeem are not inverses for account $account, amount $amountUnderlying"
{
	env e0; havoc e0;

	uint origCash = sinvoke getCash(e0);

	// both calls are "fresh"
	uint resultMint = invoke mintFreshPub(e0, account, amountUnderlying);
	bool revertedMint = lastReverted;

	uint resultRedeem = invoke redeemFreshPub(e0, account, 0, amountUnderlying);
	bool revertedRedeem = lastReverted;

	uint newCash = sinvoke getCash(e0);

	static_assert (resultMint == 0 && !revertedMint && resultRedeem == 0 && !revertedRedeem) => newCash == origCash;

	// check that exchange rate is the same, check all the 4 variables that affect the exchange rate are retained.
	// check that accounts balances are the same.
	// the only thing that changes is the interest index. rounding errors.
}
