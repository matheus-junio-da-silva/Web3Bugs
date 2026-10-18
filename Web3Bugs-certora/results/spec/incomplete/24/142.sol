// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 94
    mapping(address => UserInfo) public getUserInfo;
// Function withdrawAVAX lines 374-428
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

        uint256 feeAmount = (_amount * getPenalty()) / 1e18;
        uint256 amountMinusFee = _amount - feeAmount;

        avaxReserve -= _amount;

        if (feeAmount > 0) {
            _safeTransferAVAX(rocketJoeFactory.penaltyCollector(), feeAmount);
        }
        _safeTransferAVAX(msg.sender, amountMinusFee);
        emit UserWithdrawn(msg.sender, _amount, feeAmount);
    }

    /// @notice Create the JoePair
    /// @dev Can only be called once after phase 3 has started
    function createPair() external isStopped(false) atPhase(Phase.PhaseThree) {
        (address wavaxAddress, address tokenAddress) = (
            address(WAVAX),
            address(token)
        );
        address _pair = factory.getPair(wavaxAddress, tokenAddress);
        require(
            _pair == address(0) || IJoePair(_pair).totalSupply() == 0,
            "LaunchEvent: liquid pair already exists"
        );
        require(avaxReserve > 0, "LaunchEvent: no avax balance");

        uint256 tokenDecimals = token.decimals();
        tokenAllocated = tokenReserve;

        // Adjust the amount of tokens sent to the pool if floor price not met
        if (floorPrice > (avaxReserve * 10**tokenDecimals) / tokenAllocated) {
            tokenAllocated = (avaxReserve * 10**tokenDecimals) / floorPrice;
            tokenIncentivesForUsers =
                (tokenIncentivesForUsers * tokenAllocated) /
                tokenReserve;
            tokenIncentiveIssuerRefund =
                tokenIncentivesBalance -
                tokenIncentivesForUsers;
        }

        avaxAllocated = avaxReserve;
