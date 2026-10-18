// Historical Solidity source excerpts, with ORIGINAL source lines; no edits/reconstruction.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 83-87
  83 |     function balanceOf(address _account) public view returns (uint256) {
  84 |         if (_creditBalances[_account] == 0) return 0;
  85 |         return
  86 |             _creditBalances[_account].divPrecisely(_creditsPerToken(_account));
  87 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 109-121
 109 |     function transfer(address _to, uint256 _value) public returns (bool) {
 110 |         require(_to != address(0), "Transfer to zero address");
 111 |         require(
 112 |             _value <= balanceOf(msg.sender),
 113 |             "Transfer greater than balance"
 114 |         );
 115 | 
 116 |         _executeTransfer(msg.sender, _to, _value);
 117 | 
 118 |         emit Transfer(msg.sender, _to, _value);
 119 | 
 120 |         return true;
 121 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 472-507
 472 |     function changeSupply(uint256 _newTotalSupply)
 473 |         external
 474 |         onlyVault
 475 |         nonReentrant
 476 |     {
 477 |         require(_totalSupply > 0, "Cannot increase 0 supply");
 478 | 
 479 |         if (_totalSupply == _newTotalSupply) {
 480 |             emit TotalSupplyUpdated(
 481 |                 _totalSupply,
 482 |                 rebasingCredits,
 483 |                 rebasingCreditsPerToken
 484 |             );
 485 |             return;
 486 |         }
 487 | 
 488 |         _totalSupply = _newTotalSupply > MAX_SUPPLY
 489 |             ? MAX_SUPPLY
 490 |             : _newTotalSupply;
 491 | 
 492 |         rebasingCreditsPerToken = rebasingCredits.divPrecisely(
 493 |             _totalSupply.sub(nonRebasingSupply)
 494 |         );
 495 | 
 496 |         require(rebasingCreditsPerToken > 0, "Invalid change in supply");
 497 | 
 498 |         _totalSupply = rebasingCredits
 499 |             .divPrecisely(rebasingCreditsPerToken)
 500 |             .add(nonRebasingSupply);
 501 | 
 502 |         emit TotalSupplyUpdated(
 503 |             _totalSupply,
 504 |             rebasingCredits,
 505 |             rebasingCreditsPerToken
 506 |         );
 507 |     }
