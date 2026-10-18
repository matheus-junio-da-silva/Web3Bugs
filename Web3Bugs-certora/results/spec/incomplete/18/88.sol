// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC20Wrapper.spec:162-187 withdrawToSpecUnderlying

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Wrapper.sol lines 48-52 function/modifier withdrawTo
    function withdrawTo(address account, uint256 amount) public virtual returns (bool) {
        _burn(_msgSender(), amount);
        SafeERC20.safeTransfer(underlying, account, amount);
        return true;
    }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Wrapper.sol lines 19-19 state declaration
    IERC20 public immutable underlying;

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 36-36 state declaration
    mapping(address => uint256) private _balances;

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 40-40 state declaration
    uint256 private _totalSupply;
