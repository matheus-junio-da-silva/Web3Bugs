// Focused historical Solidity excerpts for target UNSPECIFIED; exact source line numbering.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 65-68
  65 |     modifier onlyVault() {
  66 |         require(vaultAddress == msg.sender, "Caller is not the Vault");
  67 |         _;
  68 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 258-260
 258 |     function mint(address _account, uint256 _amount) external onlyVault {
 259 |         return _mint(_account, _amount);
 260 |     }

// Original: contracts/19/contracts/contracts/vault/VaultAdmin.sol lines 17-32
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

// Original: contracts/19/contracts/contracts/vault/VaultCore.sol lines 42-49
  42 |     function mint(
  43 |         address _asset,
  44 |         uint256 _amount,
  45 |         uint256 _minimumOusdAmount
  46 |     ) external whenNotCapitalPaused nonReentrant {
  47 |         require(assets[_asset].isSupported, "Asset is not supported");
  48 |         require(_amount > 0, "Amount must be greater than 0");
  49 | 
