// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 90
    bool public stopped;
// State line 97
    IJoePair public pair;
// State line 107
    uint256 private lpSupply;
// Function withdrawIncentives lines 473-527
    function withdrawIncentives() external {
        require(address(pair) != address(0), "LaunchEvent: pair not created");

        uint256 amount = getIncentives(msg.sender);
        require(amount > 0, "LaunchEvent: caller has no incentive to claim");

        UserInfo storage user = getUserInfo[msg.sender];
        user.hasWithdrawnIncentives = true;

        if (msg.sender == issuer) {
            tokenIncentivesBalance -= tokenIncentiveIssuerRefund;
            tokenReserve = 0;
        } else {
            tokenIncentivesBalance -= amount;
        }

        token.safeTransfer(msg.sender, amount);
        emit IncentiveTokenWithdraw(msg.sender, address(token), amount);
    }

    /// @notice Withdraw AVAX if launch has been cancelled
    function emergencyWithdraw() external isStopped(true) {
        if (address(pair) == address(0)) {
            if (msg.sender != issuer) {
                UserInfo storage user = getUserInfo[msg.sender];
                require(
                    user.balance > 0,
                    "LaunchEvent: expected user to have non-zero balance to perform emergency withdraw"
                );

                uint256 balance = user.balance;
                user.balance = 0;
                avaxReserve -= balance;

                _safeTransferAVAX(msg.sender, balance);

                emit AvaxEmergencyWithdraw(msg.sender, balance);
            } else {
                uint256 balance = tokenReserve + tokenIncentivesBalance;
                tokenReserve = 0;
                tokenIncentivesBalance = 0;
                token.safeTransfer(issuer, balance);
                emit TokenEmergencyWithdraw(msg.sender, balance);
            }
        } else {
            UserInfo storage user = getUserInfo[msg.sender];

            uint256 balance = pairBalance(msg.sender);
            require(
                balance > 0,
                "LaunchEvent: caller has no liquidity to claim"
            );

            user.hasWithdrawnPair = true;


// Function emergencyWithdraw lines 494-548
    function emergencyWithdraw() external isStopped(true) {
        if (address(pair) == address(0)) {
            if (msg.sender != issuer) {
                UserInfo storage user = getUserInfo[msg.sender];
                require(
                    user.balance > 0,
                    "LaunchEvent: expected user to have non-zero balance to perform emergency withdraw"
                );

                uint256 balance = user.balance;
                user.balance = 0;
                avaxReserve -= balance;

                _safeTransferAVAX(msg.sender, balance);

                emit AvaxEmergencyWithdraw(msg.sender, balance);
            } else {
                uint256 balance = tokenReserve + tokenIncentivesBalance;
                tokenReserve = 0;
                tokenIncentivesBalance = 0;
                token.safeTransfer(issuer, balance);
                emit TokenEmergencyWithdraw(msg.sender, balance);
            }
        } else {
            UserInfo storage user = getUserInfo[msg.sender];

            uint256 balance = pairBalance(msg.sender);
            require(
                balance > 0,
                "LaunchEvent: caller has no liquidity to claim"
            );

            user.hasWithdrawnPair = true;

            if (msg.sender == issuer) {
                emit IssuerLiquidityWithdrawn(
                    msg.sender,
                    address(pair),
                    balance
                );
            } else {
                emit UserLiquidityWithdrawn(msg.sender, address(pair), balance);
            }

            pair.transfer(msg.sender, balance);
        }
    }

    /// @notice Stops the launch event and allows participants to withdraw deposits
    function allowEmergencyWithdraw() external {
        require(
            msg.sender == Ownable(address(rocketJoeFactory)).owner(),
            "LaunchEvent: caller is not RocketJoeFactory owner"
        );
        stopped = true;

// Function skim lines 554-608
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

        if (_user == issuer) {
            if (address(pair) == address(0)) return 0;
            return tokenIncentiveIssuerRefund + tokenReserve;
        } else {
            if (avaxAllocated == 0) return 0;
            return (user.balance * tokenIncentivesForUsers) / avaxAllocated;
        }
    }

    /// @notice Returns the outstanding balance of the launch event contract
    /// @return The balances of AVAX and issued token held by the launch contract
