// Historical Solidity source excerpts, with ORIGINAL source lines; no edits/reconstruction.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 258-260
 258 |     function mint(address _account, uint256 _amount) external onlyVault {
 259 |         return _mint(_account, _amount);
 260 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 298-300
 298 |     function burn(address account, uint256 amount) external onlyVault {
 299 |         return _burn(account, amount);
 300 |     }

// Original: contracts/19/contracts/contracts/vault/VaultCore.sol lines 42-87
  42 |     function mint(
  43 |         address _asset,
  44 |         uint256 _amount,
  45 |         uint256 _minimumOusdAmount
  46 |     ) external whenNotCapitalPaused nonReentrant {
  47 |         require(assets[_asset].isSupported, "Asset is not supported");
  48 |         require(_amount > 0, "Amount must be greater than 0");
  49 | 
  50 |         uint256 price = IMinMaxOracle(priceProvider).priceMin(
  51 |             Helpers.getSymbol(_asset)
  52 |         );
  53 |         if (price > 1e8) {
  54 |             price = 1e8;
  55 |         }
  56 |         uint256 assetDecimals = Helpers.getDecimals(_asset);
  57 |         uint256 unitAdjustedDeposit = _amount.scaleBy(int8(18 - assetDecimals));
  58 |         uint256 priceAdjustedDeposit = _amount.mulTruncateScale(
  59 |             price.scaleBy(int8(10)), // 18-8 because oracles have 8 decimals precision
  60 |             10**assetDecimals
  61 |         );
  62 | 
  63 |         if (_minimumOusdAmount > 0) {
  64 |             require(
  65 |                 priceAdjustedDeposit >= _minimumOusdAmount,
  66 |                 "Mint amount lower than minimum"
  67 |             );
  68 |         }
  69 | 
  70 |         emit Mint(msg.sender, priceAdjustedDeposit);
  71 | 
  72 |         // Rebase must happen before any transfers occur.
  73 |         if (unitAdjustedDeposit >= rebaseThreshold && !rebasePaused) {
  74 |             _rebase();
  75 |         }
  76 | 
  77 |         // Mint matching OUSD
  78 |         oUSD.mint(msg.sender, priceAdjustedDeposit);
  79 | 
  80 |         // Transfer the deposited coins to the vault
  81 |         IERC20 asset = IERC20(_asset);
  82 |         asset.safeTransferFrom(msg.sender, address(this), _amount);
  83 | 
  84 |         if (unitAdjustedDeposit >= autoAllocateThreshold) {
  85 |             _allocate();
  86 |         }
  87 |     }

// Original: contracts/19/contracts/contracts/vault/VaultAdmin.sol lines 25-31
  25 |     modifier onlyGovernorOrStrategist() {
  26 |         require(
  27 |             msg.sender == strategistAddr || isGovernor(),
  28 |             "Caller is not the Strategist or Governor"
  29 |         );
  30 |         _;
  31 |     }

// Original: contracts/19/contracts/contracts/vault/VaultAdmin.sol lines 282-287
 282 |     function transferToken(address _asset, uint256 _amount)
 283 |         external
 284 |         onlyGovernor
 285 |     {
 286 |         IERC20(_asset).safeTransfer(governor(), _amount);
 287 |     }
