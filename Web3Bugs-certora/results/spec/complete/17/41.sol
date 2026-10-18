// Original: contracts/17/contracts/Maximillion.sol lines 26-30
     * @return The initial borrows before the repay
     */
    function repayBehalf(address borrower) public payable {
        return repayBehalfExplicit(borrower, cEther);
    }

