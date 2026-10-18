// Original: contracts/17/contracts/CToken.sol lines 353-357
     * @return The number of tokens owned by `owner`
     */
    function balanceOf(address owner) external view returns (uint256) {
        return accountTokens[owner];
    }

