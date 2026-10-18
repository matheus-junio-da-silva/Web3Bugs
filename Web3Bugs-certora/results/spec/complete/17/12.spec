// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/mintAndRedeemFresh.cvl
// Rule redeemFresh original lines 274-400; SHA256 9f82ecafa2fef187349021f4707b2471433cdc53a644052c3135fc54e5303c45
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
	totalSupply() returns uint256
	balanceOf(address) returns uint256
	accrualBlockNumber() returns uint256
        redeemFreshPub(address,uint256,uint256) returns uint256
        getCash() returns uint256
	comptrollerRedeemAllowed(address,address,uint256) returns uint256
	doTransferOutPubSim(address,uint256) returns uint256
}

redeemFresh(uint result, address account, uint256 amountCTokens, uint256 amountUnderlying)
description "Failed to redeemFresh fresh asset with result $result (account=$account, amountCTokens=$amountCTokens, amountUnderlying=$amountUnderlying)" {
	// Free Variables
	env e0; havoc e0; // pre
	env e1; havoc e1; // invocation
	env e1b; havoc e1b; // invocations on behalf of CToken
	env e2; havoc e2; // post

	// Strict ordering
	static_require e1.block.number >= e0.block.number;
	static_require e2.block.number >= e1.block.number;

        // Redeeming from self is assumed to be impossible
        static_require account != currentContract;

	// Capture current values
	uint256 totalSupplyPre = sinvoke totalSupply(e0);
	uint256 accountSupplyPre = sinvoke balanceOf(e0, account);
	uint256 marketBlockNumber = sinvoke accrualBlockNumber(e0);
	uint256 cash = sinvoke getCash(e0);

	// Simulate checks that depend on external contracts
	uint comptrollerCheckResult = sinvoke comptrollerRedeemAllowed(e1, currentContract, account, amountCTokens); // Should include amountUnderlying?
	uint labelDoTransferOut = sinvoke doTransferOutPubSim(e1, account, amountUnderlying);

	// Invoke mintFresh
	static_require result == invoke redeemFreshPub(e1, account, amountCTokens, amountUnderlying);
	bool redeemFreshReverted = lastReverted;

	// Get next values
	uint256 totalSupplyPost = sinvoke totalSupply(e2);
	uint256 accountSupplyPost = sinvoke balanceOf(e2, account);
	uint256 newCash = sinvoke getCash(e2);

	// Helper for checking balance has not changed
	bool staticBalance =
		( totalSupplyPost == totalSupplyPre &&
		  accountSupplyPost == accountSupplyPre )
		  && cash == newCash ;

	// Helper for checking balance has not changed, as expected.
	// Precise change is computed in cTokenComputationLemma
	bool dynamicBalanceBasic = (totalSupplyPre - totalSupplyPost == accountSupplyPre - accountSupplyPost) // Change in totalSupply is same as change in accountSupply
						&& (totalSupplyPre - totalSupplyPost >= 0) // The change in supplies must be <= 0
						&& (cash - newCash >= 0); // This operation transfers out
	bool dynamicBalanceRedeemingUnderlying = (cash - newCash == amountUnderlying); // The change in cash must be amount
	bool dynamicBalanceRedeemingCToken = (totalSupplyPre-totalSupplyPost == amountCTokens); // The change in CToken must be -amountCTokens
	bool dynamicBalanceAdvanced = ((amountCTokens > 0 && amountUnderlying == 0) => dynamicBalanceRedeemingCToken)
								&& ((amountCTokens == 0 && amountUnderlying > 0) => dynamicBalanceRedeemingUnderlying)
								&& ((amountCTokens == 0 && amountUnderlying == 0) => (dynamicBalanceRedeemingCToken && dynamicBalanceRedeemingUnderlying))
								&& !(amountCTokens > 0 && amountUnderlying > 0);

	bool comptrollerCheckSuccess = comptrollerCheckResult == 0;
	bool accrued = marketBlockNumber == e1.block.number;
	bool checkTransferSuccess = cash >= amountUnderlying;
	bool doTransferSuccess = labelDoTransferOut == 0;

	// Track error codes
	uint256 NO_ERROR = 0;
	uint256 COMPTROLLER_REJECTION = 3;
	uint256 NOT_ACCRUED = 10;
	uint256 CHECK_TRANSFER_FAILED = 14; // TOKEN_INSUFFICIENT_CASH
	uint256 TOKEN_TRANSFER_OUT_FAILED = 16;
	uint256 MATH_ERROR = 9;

	// Guarantee return values
	static_assert (!redeemFreshReverted && result != MATH_ERROR) => (
	  result == NO_ERROR ||
	  result == COMPTROLLER_REJECTION ||
	  result == NOT_ACCRUED ||
	  result == CHECK_TRANSFER_FAILED ||
	  result == TOKEN_TRANSFER_OUT_FAILED ||
	  result == MATH_ERROR
	), "Got unexpected error code $result";


	// Success case updates market accordingly
	static_assert (!redeemFreshReverted && result != MATH_ERROR) => (result == NO_ERROR <=> (
		comptrollerCheckSuccess &&
		accrued &&
		checkTransferSuccess &&
		doTransferSuccess &&
		dynamicBalanceBasic &&
		dynamicBalanceAdvanced
	)), "Mismatch in no error case (0). Got result $result";

	// Policy hook rejected case
	static_assert (!redeemFreshReverted && result != MATH_ERROR) => (result == COMPTROLLER_REJECTION <=> (
		!comptrollerCheckSuccess &&
		staticBalance
	)), "Mismatch in comptroller rejection case (3=0x3). Got result $result";

	// Not accrued
	static_assert (!redeemFreshReverted && result != MATH_ERROR) => (result == NOT_ACCRUED <=> (
		comptrollerCheckSuccess &&
		!accrued &&
		staticBalance
	)), "Mismatch in non-accrued case (10=0xa). Got result $result";

	// Check transfer failure
	// Note that since if amountUnderlying == 0 we do not compute in the spec the computed amountUnderlying, so we skip the test for now
	static_assert (!redeemFreshReverted && result != MATH_ERROR && amountUnderlying > 0) => ((result == CHECK_TRANSFER_FAILED) <=> (
		comptrollerCheckSuccess &&
		accrued &&
		!checkTransferSuccess &&
		staticBalance
	)), "Mismatch in check transfer failure (14). Got result $result";

	// Do transfer failure
	// Should be: static_assert !doTransferSuccess => redeemFreshReverted;
	static_assert (!redeemFreshReverted && result != MATH_ERROR) => (result == TOKEN_TRANSFER_OUT_FAILED <=>
	(
		comptrollerCheckSuccess &&
		accrued &&
		checkTransferSuccess &&
		!doTransferSuccess &&
		staticBalance
	)), "Mismatch in do transfer failure (16). Got result $result";

	// Math error -> no state changes (at least, the ones we observe here! This is not checking about the FULL state of the contract)
	// SG: Idea - this could be a useful check that is reused across many of Compound's functions that may return math error codes, and will be more thorough.
	static_assert !redeemFreshReverted => (result == MATH_ERROR =>
	(
		staticBalance &&
		newCash == cash
	)), "State changes occuring despite math error, totalSupplyPre=$totalSupplyPre, totalSupplyPost=$totalSupplyPost ; accountSupplyPre=$accountSupplyPre, accountSupplyPost=$accountSupplyPost";
}
