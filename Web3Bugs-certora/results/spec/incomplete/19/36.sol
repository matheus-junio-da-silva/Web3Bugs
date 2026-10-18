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
