// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/mintAndRedeemFresh.cvl
// Rule mintFresh_extended original lines 149-271; SHA256 9f82ecafa2fef187349021f4707b2471433cdc53a644052c3135fc54e5303c45
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
	totalSupply() returns uint256
	balanceOf(address) returns uint256
	accrualBlockNumber() returns uint256
        mintFreshPub(address,uint256) returns uint256
        checkTransferInPub(address,uint256) returns uint256
        getCash() returns uint256
	comptrollerMintAllowed(address,address,uint256) returns uint256
	doTransferInPubSim(address,uint256) returns uint256
}

mintFresh_extended(uint result, address account, uint256 amount)
description "Failed to mint fresh asset with result $result (account=$account, amount=$amount)" {
	// Free Variables
	env e0; havoc e0; // pre
	env e1; havoc e1; // invocation
	env e2; havoc e2; // post

	// Strict ordering
	static_require e1.block.number >= e0.block.number;
	static_require e2.block.number >= e1.block.number;

        // Minting to self is assumed to be impossible
        static_require account != currentContract;

	// Capture current values
	uint256 totalSupplyPre = sinvoke totalSupply(e0);
	uint256 accountSupplyPre = sinvoke balanceOf(e0, account);
	uint256 marketBlockNumber = sinvoke accrualBlockNumber(e0);

	uint256 cash = sinvoke getCash(e0);

	// Label CALL results
	uint comptrollerCheckResult = sinvoke comptrollerMintAllowed(e1, currentContract, account, amount);
	uint labelCheckTransferIn = sinvoke checkTransferInPub(e1, account, amount);
	uint labelDoTransferIn = sinvoke doTransferInPubSim(e1, account, amount);

	// Invoke mintFresh
	static_require result == invoke mintFreshPub(e1, account, amount);
	bool mintFreshReverted = lastReverted;

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
	bool dynamicBalance = (totalSupplyPost - totalSupplyPre == accountSupplyPost - accountSupplyPre) // Change in totalSupply is same as change in accountSupply
						&& (totalSupplyPost - totalSupplyPre >= 0) // The change in supplies must be >= 0
						&& (newCash - cash == amount); // The change in cash must be amount

	bool comptrollerCheckSuccess = comptrollerCheckResult == 0; // Comptroller is an external contract and its error is converted to COMPTROLLER_REJECTION, so no need to require on the label
	bool accrued = marketBlockNumber == e1.block.number;
	bool checkTransferSuccess = labelCheckTransferIn == 0;
	bool doTransferSuccess = labelDoTransferIn == 0;

	// Track error codes
	uint256 NO_ERROR = 0;
	uint256 COMPTROLLER_REJECTION = 3;
	uint256 NOT_ACCRUED = 10;
	uint256 CHECK_TRANSFER_FAILED_1 = 12;
	uint256 CHECK_TRANSFER_FAILED_2 = 13;
	uint256 TOKEN_TRANSFER_IN_FAILED = 15;
	uint256 MATH_ERROR = 9;

	// Guarantee return values
	static_assert (!mintFreshReverted && result != MATH_ERROR) => (
	  result == NO_ERROR ||
	  result == COMPTROLLER_REJECTION ||
	  result == NOT_ACCRUED ||
	  result == CHECK_TRANSFER_FAILED_1 ||
	  result == CHECK_TRANSFER_FAILED_2 ||
	  result == TOKEN_TRANSFER_IN_FAILED ||
	  result == MATH_ERROR
	), "Got unexpected error code $result";

	/* All these cases depend on: (1) mintFresh not reverting; and (2) the error code being anything  other than a math error.
		The idea is that (1) reverts, if are not catched by the caller (could it be a contract by Compound?), will have no effect on the state;
		and (2) math errors, which are handled separately.
	 */
	// Success case updates market accordingly
	static_assert (!mintFreshReverted && result != MATH_ERROR) => (result == NO_ERROR <=> (
		comptrollerCheckSuccess &&
		accrued &&
		checkTransferSuccess &&
		doTransferSuccess &&
		dynamicBalance
	)), "Mismatch in no error case (0). Got result $result";

	// Policy hook rejected case
	static_assert (!mintFreshReverted && result != MATH_ERROR) => (result == COMPTROLLER_REJECTION <=> (
		!comptrollerCheckSuccess &&
		staticBalance
	)), "Mismatch in comptroller rejection case (3). Got result $result";

	// Not accrued
	static_assert (!mintFreshReverted && result != MATH_ERROR) => (result == NOT_ACCRUED <=> (
		comptrollerCheckSuccess &&
		!accrued &&
		staticBalance
	)), "Mismatch in non-accrued case (10=0xa). Got result $result";

	// Check transfer failure
	static_assert (!mintFreshReverted && result != MATH_ERROR) => ((result == CHECK_TRANSFER_FAILED_1 || result == CHECK_TRANSFER_FAILED_2) <=> (
		comptrollerCheckSuccess &&
		accrued &&
		!checkTransferSuccess &&
		staticBalance
	)), "Mismatch in check transfer failure (12,13). Got result $result";

	// Do transfer failure
	static_assert (!mintFreshReverted && result != MATH_ERROR) => (result == TOKEN_TRANSFER_IN_FAILED <=>
	(
		comptrollerCheckSuccess &&
		accrued &&
		checkTransferSuccess &&
		!doTransferSuccess &&
		staticBalance
	)), "Mismatch in do transfer failure (15). Got result $result";

	// Math error -> no state changes (at least, the ones we observe here! This is not checking about the FULL state of the contract)
	// SG: Idea - this could be a useful check that is reused across many of Compound's functions that may return math error codes, and will be more thorough.
	static_assert !mintFreshReverted => (result == MATH_ERROR =>
	(
		staticBalance
	)), "State changes occuring despite math error, totalSupplyPre=$totalSupplyPre, totalSupplyPost=$totalSupplyPost ; accountSupplyPre=$accountSupplyPre, accountSupplyPost=$accountSupplyPost";
}
