// Focused historical Solidity excerpts for target VaultAdmin; exact source line numbering.

// Original: contracts/19/contracts/contracts/vault/VaultAdmin.sol lines 13-32
  13 | contract VaultAdmin is VaultStorage {
  14 |     /**
  15 |      * @dev Verifies that the caller is the Vault or Governor.
  16 |      */
  17 |     modifier onlyVaultOrGovernor() {
  18 |         require(
  19 |             msg.sender == address(this) || isGovernor(),
  20 |             "Caller is not the Vault or Governor"
  21 |         );
  22 |         _;
  23 |     }
  24 | 
  25 |     modifier onlyGovernorOrStrategist() {
  26 |         require(
  27 |             msg.sender == strategistAddr || isGovernor(),
  28 |             "Caller is not the Strategist or Governor"
  29 |         );
  30 |         _;
  31 |     }
  32 | 

// Original: contracts/19/contracts/contracts/vault/VaultAdmin.sol lines 41-58
  41 |     function setPriceProvider(address _priceProvider) external onlyGovernor {
  42 |         priceProvider = _priceProvider;
  43 |         emit PriceProviderUpdated(_priceProvider);
  44 |     }
  45 | 
  46 |     /**
  47 |      * @dev Set a fee in basis points to be charged for a redeem.
  48 |      * @param _redeemFeeBps Basis point fee to be charged
  49 |      */
  50 |     function setRedeemFeeBps(uint256 _redeemFeeBps) external onlyGovernor {
  51 |         redeemFeeBps = _redeemFeeBps;
  52 |         emit RedeemFeeUpdated(_redeemFeeBps);
  53 |     }
  54 | 
  55 |     /**
  56 |      * @dev Set a buffer of assets to keep in the Vault to handle most
  57 |      * redemptions without needing to spend gas unwinding assets from a Strategy.
  58 |      * @param _vaultBuffer Percentage using 18 decimals. 100% = 1e18.

// Original: contracts/19/contracts/contracts/vault/VaultAdmin.sol lines 259-273
 259 |     function pauseCapital() external onlyGovernorOrStrategist {
 260 |         capitalPaused = true;
 261 |         emit CapitalPaused();
 262 |     }
 263 | 
 264 |     /**
 265 |      * @dev Set the deposit paused flag to false to enable capital movement.
 266 |      */
 267 |     function unpauseCapital() external onlyGovernorOrStrategist {
 268 |         capitalPaused = false;
 269 |         emit CapitalUnpaused();
 270 |     }
 271 | 
 272 |     /***************************************
 273 |                     Rewards

// Original: contracts/19/contracts/contracts/vault/VaultAdmin.sol lines 282-292
 282 |     function transferToken(address _asset, uint256 _amount)
 283 |         external
 284 |         onlyGovernor
 285 |     {
 286 |         IERC20(_asset).safeTransfer(governor(), _amount);
 287 |     }
 288 | 
 289 |     /**
 290 |      * @dev Collect reward tokens from all strategies and swap for supported
 291 |      *      stablecoin via Uniswap
 292 |      */
