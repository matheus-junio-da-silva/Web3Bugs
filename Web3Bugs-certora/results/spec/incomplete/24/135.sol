// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 48
    address public issuer;
// State line 114
    uint256 private tokenReserve;
// State line 118
    uint256 private tokenIncentivesBalance;
// Function depositAVAX lines 333-387
    function depositAVAX()
        external
        payable
        isStopped(false)
        atPhase(Phase.PhaseOne)
    {
        require(msg.sender != issuer, "LaunchEvent: issuer cannot participate");
        require(
            msg.value > 0,
            "LaunchEvent: expected non-zero AVAX to deposit"
        );

        UserInfo storage user = getUserInfo[msg.sender];
        uint256 newAllocation = user.balance + msg.value;
        require(
            newAllocation <= maxAllocation,
            "LaunchEvent: amount exceeds max allocation"
        );

        uint256 rJoeNeeded;
        // check if additional allocation is required.
        if (newAllocation > user.allocation) {
            // Get amount of rJOE tokens needed to burn and update allocation
            rJoeNeeded = getRJoeAmount(newAllocation - user.allocation);
            // Set allocation to the current balance as it's impossible
            // to buy more allocation without sending AVAX too
            user.allocation = newAllocation;
        }

        user.balance = newAllocation;
        avaxReserve += msg.value;

        if (rJoeNeeded > 0) {
            rJoe.burnFrom(msg.sender, rJoeNeeded);
        }

        emit UserParticipated(msg.sender, msg.value, rJoeNeeded);
    }

    /// @notice Withdraw AVAX, only permitted during phase 1 and 2
    /// @param _amount The amount of AVAX to withdraw
    function withdrawAVAX(uint256 _amount) external isStopped(false) {
        Phase _currentPhase = currentPhase();
        require(
            _currentPhase == Phase.PhaseOne || _currentPhase == Phase.PhaseTwo,
            "LaunchEvent: unable to withdraw"
        );
        require(_amount > 0, "LaunchEvent: invalid withdraw amount");
        UserInfo storage user = getUserInfo[msg.sender];
        require(
            user.balance >= _amount,
            "LaunchEvent: withdrawn amount exceeds balance"
        );
        user.balance -= _amount;


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

