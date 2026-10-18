// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 90
    bool public stopped;
// Function allowEmergencyWithdraw lines 543-597
    function allowEmergencyWithdraw() external {
        require(
            msg.sender == Ownable(address(rocketJoeFactory)).owner(),
            "LaunchEvent: caller is not RocketJoeFactory owner"
        );
        stopped = true;
        emit Stopped();
    }

    /// @notice Force balances to match tokens that were deposited, but not sent directly to the contract.
    /// Any excess tokens are sent to the penaltyCollector
    function skim() external {
        require(msg.sender == tx.origin, "LaunchEvent: EOA only");
        address penaltyCollector = rocketJoeFactory.penaltyCollector();

        uint256 excessToken = token.balanceOf(address(this)) -
            tokenReserve -
            tokenIncentivesBalance;
        if (excessToken > 0) {
            token.safeTransfer(penaltyCollector, excessToken);
        }

        uint256 excessAvax = address(this).balance - avaxReserve;
        if (excessAvax > 0) {
            _safeTransferAVAX(penaltyCollector, excessAvax);
        }
    }

    /// @notice Returns the current penalty for early withdrawal
    /// @return The penalty to apply to a withdrawal amount
    function getPenalty() public view returns (uint256) {
        if (block.timestamp < auctionStart) {
            return 0;
        }
        uint256 timeElapsed = block.timestamp - auctionStart;
        if (timeElapsed < phaseOneNoFeeDuration) {
            return 0;
        } else if (timeElapsed < phaseOneDuration) {
            return
                ((timeElapsed - phaseOneNoFeeDuration) * maxWithdrawPenalty) /
                (phaseOneDuration - phaseOneNoFeeDuration);
        }
        return fixedWithdrawPenalty;
    }

    /// @notice Returns the incentives for a given user
    /// @param _user The user to look up
    /// @return The amount of incentives `_user` can withdraw
    function getIncentives(address _user) public view returns (uint256) {
        UserInfo memory user = getUserInfo[_user];

        if (user.hasWithdrawnIncentives) {
            return 0;
        }

