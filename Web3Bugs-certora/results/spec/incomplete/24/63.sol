// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 48
    address public issuer;
// State line 94
    mapping(address => UserInfo) public getUserInfo;
// State line 97
    IJoePair public pair;
// Function withdrawLiquidity lines 453-507
    function withdrawLiquidity() external isStopped(false) timelockElapsed {
        require(address(pair) != address(0), "LaunchEvent: pair not created");

        UserInfo storage user = getUserInfo[msg.sender];

        uint256 balance = pairBalance(msg.sender);
        require(balance > 0, "LaunchEvent: caller has no liquidity to claim");

        user.hasWithdrawnPair = true;

        if (msg.sender == issuer) {
            emit IssuerLiquidityWithdrawn(msg.sender, address(pair), balance);
        } else {
            emit UserLiquidityWithdrawn(msg.sender, address(pair), balance);
        }

        pair.transfer(msg.sender, balance);
    }

    /// @notice Withdraw incentives tokens
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

// Function pairBalance lines 623-677
    function pairBalance(address _user) public view returns (uint256) {
        UserInfo memory user = getUserInfo[_user];
        if (avaxAllocated == 0 || user.hasWithdrawnPair) {
            return 0;
        }
        if (msg.sender == issuer) {
            return lpSupply / 2;
        }
        return (user.balance * lpSupply) / avaxAllocated / 2;
    }

    /// @dev Bytecode size optimization for the `atPhase` modifier
    /// This works becuase internal functions are not in-lined in modifiers
    function _atPhase(Phase _phase) internal view {
        require(currentPhase() == _phase, "LaunchEvent: wrong phase");
    }

    /// @dev Bytecode size optimization for the `timelockElapsed` modifier
    /// This works becuase internal functions are not in-lined in modifiers
    function _timelockElapsed() internal view {
        uint256 phase3Start = auctionStart +
            phaseOneDuration +
            phaseTwoDuration;
        if (msg.sender == issuer) {
            require(
                block.timestamp > phase3Start + issuerTimelock,
                "LaunchEvent: can't withdraw before issuer's timelock"
            );
        } else {
            require(
                block.timestamp > phase3Start + userTimelock,
                "LaunchEvent: can't withdraw before user's timelock"
            );
        }
    }

    /// @dev Bytecode size optimization for the `isStopped` modifier
    /// This works becuase internal functions are not in-lined in modifiers
    function _isStopped(bool _stopped) internal view {
        if (_stopped) {
            require(stopped, "LaunchEvent: is still running");
        } else {
            require(!stopped, "LaunchEvent: stopped");
        }
    }

    /// @notice Send AVAX
    /// @param _to The receiving address
    /// @param _value The amount of AVAX to send
    /// @dev Will revert on failure
    function _safeTransferAVAX(address _to, uint256 _value) internal {
        require(
            address(this).balance - _value >= avaxReserve,
            "LaunchEvent: not enough avax"
        );
