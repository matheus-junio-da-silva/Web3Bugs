// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 97
    IJoePair public pair;
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
