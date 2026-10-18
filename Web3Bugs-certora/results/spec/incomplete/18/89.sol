// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC20Wrapper.spec:192-214 recoverSpec

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Wrapper.sol lines 58-62 function/modifier _recover
    function _recover(address account) internal virtual returns (uint256) {
        uint256 value = underlying.balanceOf(address(this)) - totalSupply();
        _mint(account, value);
        return value;
    }

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 94-96 function/modifier totalSupply
    function totalSupply() public view virtual override returns (uint256) {
        return _totalSupply;
    }

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 101-103 function/modifier balanceOf
    function balanceOf(address account) public view virtual override returns (uint256) {
        return _balances[account];
    }

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 36-36 state declaration
    mapping(address => uint256) private _balances;

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 40-40 state declaration
    uint256 private _totalSupply;
