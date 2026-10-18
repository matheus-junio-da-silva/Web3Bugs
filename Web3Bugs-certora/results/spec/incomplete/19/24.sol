// Historical Solidity source excerpts, with ORIGINAL source lines; no edits/reconstruction.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 369-402
 369 |     function _isNonRebasingAccount(address _account) internal returns (bool) {
 370 |         RebaseOptions rebaseState = rebaseState[_account];
 371 |         if (rebaseState == RebaseOptions.OptIn) {
 372 |             // The address has chosen to be rebasing.
 373 |             return false;
 374 |         } else if (rebaseState == RebaseOptions.OptOut) {
 375 |             // The address has chosen to be non-rebasing.
 376 |             return true;
 377 |         } else {
 378 |             // The address has not chosen explicitly, so use the default
 379 |             // for its type.
 380 |             if (Address.isContract(_account)) {
 381 |                 // Contracts default to be non-rebasing.
 382 | 
 383 |                 // Migrate if needed, making sure the rebasing/non-rebasing
 384 |                 // supply is updated and fixed credits per token is set
 385 |                 // for this account.
 386 |                 _ensureRebasingMigration(_account);
 387 |                 return true;
 388 |             } else {
 389 |                 // User accounts default to be rebasing.
 390 | 
 391 |                 // Disallow contracts from interacting with OUSD if the following
 392 |                 // sequence has occurred: The contract has self-destructed, been
 393 |                 // recreated at the same address with CREATE2, and then is interacting
 394 |                 // with OUSD again from the contract's constructor.
 395 |                 require(
 396 |                     nonRebasingCreditsPerToken[_account] == 0,
 397 |                     "Previous Contract"
 398 |                 );
 399 |                 return false;
 400 |             }
 401 |         }
 402 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 408-417
 408 |     function _ensureRebasingMigration(address _account) internal {
 409 |         if (nonRebasingCreditsPerToken[_account] == 0) {
 410 |             // Set fixed credits per token for this account
 411 |             nonRebasingCreditsPerToken[_account] = rebasingCreditsPerToken;
 412 |             // Update non rebasing supply
 413 |             nonRebasingSupply = nonRebasingSupply.add(balanceOf(_account));
 414 |             // Update credit tallies
 415 |             rebasingCredits = rebasingCredits.sub(_creditBalances[_account]);
 416 |         }
 417 |     }

// Original: contracts/19/spec/harnesses/OUSDHarness.sol lines 6-6
   6 | 	function Certora_isNonRebasingAccount(address account) external returns (bool) { return _isNonRebasingAccount(account); }
