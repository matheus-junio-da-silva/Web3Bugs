// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC20Wrapper.spec:44-63 depositForSpecBasic

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Wrapper.sol lines 39-43 function/modifier depositFor
    function depositFor(address account, uint256 amount) public virtual returns (bool) {
        SafeERC20.safeTransferFrom(underlying, _msgSender(), address(this), amount);
        _mint(account, amount);
        return true;
    }

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 94-96 function/modifier totalSupply
    function totalSupply() public view virtual override returns (uint256) {
        return _totalSupply;
    }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Wrapper.sol lines 19-19 state declaration
    IERC20 public immutable underlying;

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 36-36 state declaration
    mapping(address => uint256) private _balances;

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 40-40 state declaration
    uint256 private _totalSupply;
