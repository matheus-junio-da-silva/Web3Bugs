// Historical Solidity source excerpts, with ORIGINAL source lines; no edits/reconstruction.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 258-260
 258 |     function mint(address _account, uint256 _amount) external onlyVault {
 259 |         return _mint(_account, _amount);
 260 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 272-293
 272 |     function _mint(address _account, uint256 _amount) internal nonReentrant {
 273 |         require(_account != address(0), "Mint to the zero address");
 274 | 
 275 |         bool isNonRebasingAccount = _isNonRebasingAccount(_account);
 276 | 
 277 |         uint256 creditAmount = _amount.mulTruncate(_creditsPerToken(_account));
 278 |         _creditBalances[_account] = _creditBalances[_account].add(creditAmount);
 279 | 
 280 |         // If the account is non rebasing and doesn't have a set creditsPerToken
 281 |         // then set it i.e. this is a mint from a fresh contract
 282 |         if (isNonRebasingAccount) {
 283 |             nonRebasingSupply = nonRebasingSupply.add(_amount);
 284 |         } else {
 285 |             rebasingCredits = rebasingCredits.add(creditAmount);
 286 |         }
 287 | 
 288 |         _totalSupply = _totalSupply.add(_amount);
 289 | 
 290 |         require(_totalSupply < MAX_SUPPLY, "Max supply");
 291 | 
 292 |         emit Transfer(address(0), _account, _amount);
 293 |     }

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
