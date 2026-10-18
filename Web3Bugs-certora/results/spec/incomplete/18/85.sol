// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Wrapper.sol lines 39-62 (callable)
    function depositFor(address account, uint256 amount) public virtual returns (bool) {
        SafeERC20.safeTransferFrom(underlying, _msgSender(), address(this), amount);
        _mint(account, amount);
        return true;
    }

    /**
     * @dev Allow a user to burn a number of wrapped tokens and withdraw the corresponding number of underlying tokens.
     */
    function withdrawTo(address account, uint256 amount) public virtual returns (bool) {
        _burn(_msgSender(), amount);
        SafeERC20.safeTransfer(underlying, account, amount);
        return true;
    }

    /**
     * @dev Mint wrapped token to cover any underlyingTokens that would have been transferred by mistake. Internal
     * function that can be exposed with access control if desired.
     */
    function _recover(address account) internal virtual returns (uint256) {
        uint256 value = underlying.balanceOf(address(this)) - totalSupply();
        _mint(account, value);
        return value;
    }

// Original: contracts/18/contracts/mocks/ERC20WrapperMock.sol lines 6-17 (target context (no matched entrypoint))

contract ERC20WrapperMock is ERC20Wrapper {
    constructor(
        IERC20 _underlyingToken,
        string memory name,
        string memory symbol
    ) ERC20(name, symbol) ERC20Wrapper(_underlyingToken) {}

    function recover(address account) public returns (uint256) {
        return _recover(account);
    }
}
