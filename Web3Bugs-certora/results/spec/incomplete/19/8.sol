// Historical Solidity source excerpts, with ORIGINAL source lines; no edits/reconstruction.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 424-445
 424 |     function rebaseOptIn() public nonReentrant {
 425 |         require(_isNonRebasingAccount(msg.sender), "Account has not opted out");
 426 | 
 427 |         // Convert balance into the same amount at the current exchange rate
 428 |         uint256 newCreditBalance = _creditBalances[msg.sender]
 429 |             .mul(rebasingCreditsPerToken)
 430 |             .div(_creditsPerToken(msg.sender));
 431 | 
 432 |         // Decreasing non rebasing supply
 433 |         nonRebasingSupply = nonRebasingSupply.sub(balanceOf(msg.sender));
 434 | 
 435 |         _creditBalances[msg.sender] = newCreditBalance;
 436 | 
 437 |         // Increase rebasing credits, totalSupply remains unchanged so no
 438 |         // adjustment necessary
 439 |         rebasingCredits = rebasingCredits.add(_creditBalances[msg.sender]);
 440 | 
 441 |         rebaseState[msg.sender] = RebaseOptions.OptIn;
 442 | 
 443 |         // Delete any fixed credits per token
 444 |         delete nonRebasingCreditsPerToken[msg.sender];
 445 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 450-464
 450 |     function rebaseOptOut() public nonReentrant {
 451 |         require(!_isNonRebasingAccount(msg.sender), "Account has not opted in");
 452 | 
 453 |         // Increase non rebasing supply
 454 |         nonRebasingSupply = nonRebasingSupply.add(balanceOf(msg.sender));
 455 |         // Set fixed credits per token
 456 |         nonRebasingCreditsPerToken[msg.sender] = rebasingCreditsPerToken;
 457 | 
 458 |         // Decrease rebasing credits, total supply remains unchanged so no
 459 |         // adjustment necessary
 460 |         rebasingCredits = rebasingCredits.sub(_creditBalances[msg.sender]);
 461 | 
 462 |         // Mark explicitly opted out of rebasing
 463 |         rebaseState[msg.sender] = RebaseOptions.OptOut;
 464 |     }

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
