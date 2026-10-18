// Original: contracts/17/contracts/CToken.sol lines 571-575
     * @return The quantity of underlying asset owned by this contract
     */
    function getCash() external view returns (uint) {
        return getCashPrior();
    }

