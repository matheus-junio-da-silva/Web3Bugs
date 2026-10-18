// Historical Solidity source excerpts, with ORIGINAL source lines; no edits/reconstruction.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 52-60
  52 |     function initialize(
  53 |         string calldata _nameArg,
  54 |         string calldata _symbolArg,
  55 |         address _vaultAddress
  56 |     ) external onlyGovernor initializer {
  57 |         InitializableERC20Detailed._initialize(_nameArg, _symbolArg, 18);
  58 |         rebasingCreditsPerToken = 1e18;
  59 |         vaultAddress = _vaultAddress;
  60 |     }

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

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 45-89
  45 |     uint256 public rebasingCreditsPerToken;
  46 |     // Frozen address/credits are non rebasing (value is held in contracts which
  47 |     // do not receive yield unless they explicitly opt in)
  48 |     uint256 public nonRebasingSupply;
  49 |     mapping(address => uint256) public nonRebasingCreditsPerToken;
  50 |     mapping(address => RebaseOptions) public rebaseState;
  51 | 
  52 |     function initialize(
  53 |         string calldata _nameArg,
  54 |         string calldata _symbolArg,
  55 |         address _vaultAddress
  56 |     ) external onlyGovernor initializer {
  57 |         InitializableERC20Detailed._initialize(_nameArg, _symbolArg, 18);
  58 |         rebasingCreditsPerToken = 1e18;
  59 |         vaultAddress = _vaultAddress;
  60 |     }
  61 | 
  62 |     /**
  63 |      * @dev Verifies that the caller is the Savings Manager contract
  64 |      */
  65 |     modifier onlyVault() {
  66 |         require(vaultAddress == msg.sender, "Caller is not the Vault");
  67 |         _;
  68 |     }
  69 | 
  70 |     /**
  71 |      * @return The total supply of OUSD.
  72 |      */
  73 |     function totalSupply() public view returns (uint256) {
  74 |         return _totalSupply;
  75 |     }
  76 | 
  77 |     /**
  78 |      * @dev Gets the balance of the specified address.
  79 |      * @param _account Address to query the balance of.
  80 |      * @return A uint256 representing the _amount of base units owned by the
  81 |      *         specified address.
  82 |      */
  83 |     function balanceOf(address _account) public view returns (uint256) {
  84 |         if (_creditBalances[_account] == 0) return 0;
  85 |         return
  86 |             _creditBalances[_account].divPrecisely(_creditsPerToken(_account));
  87 |     }
  88 | 
  89 |     /**
