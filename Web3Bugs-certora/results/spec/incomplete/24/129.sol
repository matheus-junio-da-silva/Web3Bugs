// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 94
    mapping(address => UserInfo) public getUserInfo;
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

