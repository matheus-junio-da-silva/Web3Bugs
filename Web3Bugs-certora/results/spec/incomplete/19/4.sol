// Historical Solidity source excerpts, with ORIGINAL source lines; no edits/reconstruction.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 83-87
  83 |     function balanceOf(address _account) public view returns (uint256) {
  84 |         if (_creditBalances[_account] == 0) return 0;
  85 |         return
  86 |             _creditBalances[_account].divPrecisely(_creditsPerToken(_account));
  87 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 351-361
 351 |     function _creditsPerToken(address _account)
 352 |         internal
 353 |         view
 354 |         returns (uint256)
 355 |     {
 356 |         if (nonRebasingCreditsPerToken[_account] != 0) {
 357 |             return nonRebasingCreditsPerToken[_account];
 358 |         } else {
 359 |             return rebasingCreditsPerToken;
 360 |         }
 361 |     }
