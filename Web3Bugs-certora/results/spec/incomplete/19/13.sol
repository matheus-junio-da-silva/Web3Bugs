// Historical Solidity source excerpts, with ORIGINAL source lines; no edits/reconstruction.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 298-300
 298 |     function burn(address account, uint256 amount) external onlyVault {
 299 |         return _burn(account, amount);
 300 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 313-344
 313 |     function _burn(address _account, uint256 _amount) internal nonReentrant {
 314 |         require(_account != address(0), "Burn from the zero address");
 315 | 
 316 |         bool isNonRebasingAccount = _isNonRebasingAccount(_account);
 317 |         uint256 creditAmount = _amount.mulTruncate(_creditsPerToken(_account));
 318 |         uint256 currentCredits = _creditBalances[_account];
 319 | 
 320 |         // Remove the credits, burning rounding errors
 321 |         if (
 322 |             currentCredits == creditAmount || currentCredits - 1 == creditAmount
 323 |         ) {
 324 |             // Handle dust from rounding
 325 |             _creditBalances[_account] = 0;
 326 |         } else if (currentCredits > creditAmount) {
 327 |             _creditBalances[_account] = _creditBalances[_account].sub(
 328 |                 creditAmount
 329 |             );
 330 |         } else {
 331 |             revert("Remove exceeds balance");
 332 |         }
 333 | 
 334 |         // Remove from the credit tallies and non-rebasing supply
 335 |         if (isNonRebasingAccount) {
 336 |             nonRebasingSupply = nonRebasingSupply.sub(_amount);
 337 |         } else {
 338 |             rebasingCredits = rebasingCredits.sub(creditAmount);
 339 |         }
 340 | 
 341 |         _totalSupply = _totalSupply.sub(_amount);
 342 | 
 343 |         emit Transfer(_account, address(0), _amount);
 344 |     }

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
