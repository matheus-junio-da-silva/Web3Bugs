// Focused historical Solidity excerpts for target OUSD; exact source line numbering.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 39-50
  39 |     uint256 private constant MAX_SUPPLY = ~uint128(0); // (2^128) - 1
  40 |     uint256 public _totalSupply;
  41 |     mapping(address => mapping(address => uint256)) private _allowances;
  42 |     address public vaultAddress = address(0);
  43 |     mapping(address => uint256) private _creditBalances;
  44 |     uint256 public rebasingCredits;
  45 |     uint256 public rebasingCreditsPerToken;
  46 |     // Frozen address/credits are non rebasing (value is held in contracts which
  47 |     // do not receive yield unless they explicitly opt in)
  48 |     uint256 public nonRebasingSupply;
  49 |     mapping(address => uint256) public nonRebasingCreditsPerToken;
  50 |     mapping(address => RebaseOptions) public rebaseState;

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 65-68
  65 |     modifier onlyVault() {
  66 |         require(vaultAddress == msg.sender, "Caller is not the Vault");
  67 |         _;
  68 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 258-260
 258 |     function mint(address _account, uint256 _amount) external onlyVault {
 259 |         return _mint(_account, _amount);
 260 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 298-300
 298 |     function burn(address account, uint256 amount) external onlyVault {
 299 |         return _burn(account, amount);
 300 |     }
