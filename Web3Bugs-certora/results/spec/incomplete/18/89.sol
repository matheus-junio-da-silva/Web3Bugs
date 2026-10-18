// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Wrapper.sol lines 56-63 (callable)
     * function that can be exposed with access control if desired.
     */
    function _recover(address account) internal virtual returns (uint256) {
        uint256 value = underlying.balanceOf(address(this)) - totalSupply();
        _mint(account, value);
        return value;
    }
}

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Wrapper.sol lines 58-63 (callable)
    function _recover(address account) internal virtual returns (uint256) {
        uint256 value = underlying.balanceOf(address(this)) - totalSupply();
        _mint(account, value);
        return value;
    }
}

// Original: contracts/18/contracts/mocks/ERC20WrapperMock.sol lines 14-17 (callable)
    function recover(address account) public returns (uint256) {
        return _recover(account);
    }
}
