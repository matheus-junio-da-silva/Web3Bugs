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
