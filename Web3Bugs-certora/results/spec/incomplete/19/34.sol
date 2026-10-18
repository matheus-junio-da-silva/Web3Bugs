// Focused historical Solidity excerpts for target VaultCore; exact source line numbering.

// Original: contracts/19/contracts/contracts/vault/VaultCore.sol lines 28-34
  28 |     /**
  29 |      * @dev Verifies that the deposits are not paused.
  30 |      */
  31 |     modifier whenNotCapitalPaused() {
  32 |         require(!capitalPaused, "Capital paused");
  33 |         _;
  34 |     }

// Original: contracts/19/contracts/contracts/vault/VaultCore.sol lines 42-49
  42 |     function mint(
  43 |         address _asset,
  44 |         uint256 _amount,
  45 |         uint256 _minimumOusdAmount
  46 |     ) external whenNotCapitalPaused nonReentrant {
  47 |         require(assets[_asset].isSupported, "Asset is not supported");
  48 |         require(_amount > 0, "Amount must be greater than 0");
  49 | 

// Original: contracts/19/contracts/contracts/vault/VaultCore.sol lines 158-167
 158 |     function redeem(uint256 _amount, uint256 _minimumUnitAmount)
 159 |         public
 160 |         whenNotCapitalPaused
 161 |         nonReentrant
 162 |     {
 163 |         if (_amount > rebaseThreshold && !rebasePaused) {
 164 |             _rebase();
 165 |         }
 166 |         _redeem(_amount, _minimumUnitAmount);
 167 |     }

// Original: contracts/19/contracts/contracts/vault/VaultCore.sol lines 363-370
 363 |     function rebase()
 364 |         public
 365 |         whenNotRebasePaused
 366 |         nonReentrant
 367 |         returns (uint256 newTotalSupply)
 368 |     {
 369 |         return _rebase();
 370 |     }
