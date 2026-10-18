// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 90
    bool public stopped;
// State line 94
    mapping(address => UserInfo) public getUserInfo;
// State line 97
    IJoePair public pair;
// Function currentPhase lines 319-373
    function currentPhase() public view returns (Phase) {
        if (auctionStart == 0 || block.timestamp < auctionStart) {
            return Phase.NotStarted;
        } else if (block.timestamp < auctionStart + phaseOneDuration) {
            return Phase.PhaseOne;
        } else if (
            block.timestamp < auctionStart + phaseOneDuration + phaseTwoDuration
        ) {
            return Phase.PhaseTwo;
        }
        return Phase.PhaseThree;
    }

    /// @notice Deposits AVAX and burns rJoe
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

// Function createPair lines 402-456
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
        avaxReserve = 0;

        tokenReserve -= tokenAllocated;

        WAVAX.deposit{value: avaxAllocated}();
        if (_pair == address(0)) {
            pair = IJoePair(factory.createPair(wavaxAddress, tokenAddress));
        } else {
            pair = IJoePair(_pair);
        }
        WAVAX.transfer(address(pair), avaxAllocated);
        token.safeTransfer(address(pair), tokenAllocated);
        lpSupply = pair.mint(address(this));

        emit LiquidityPoolCreated(
            address(pair),
            tokenAddress,
            wavaxAddress,
            tokenAllocated,
            avaxAllocated
        );
    }

    /// @notice Withdraw liquidity pool tokens
    function withdrawLiquidity() external isStopped(false) timelockElapsed {
        require(address(pair) != address(0), "LaunchEvent: pair not created");

        UserInfo storage user = getUserInfo[msg.sender];
