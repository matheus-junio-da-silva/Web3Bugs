// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 48
    address public issuer;
// State line 94
    mapping(address => UserInfo) public getUserInfo;
// State line 97
    IJoePair public pair;
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

// Function getIncentives lines 591-645
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
    function getReserves() external view returns (uint256, uint256) {
        return (avaxReserve, tokenReserve + tokenIncentivesBalance);
    }

    /// @notice Get the rJOE amount needed to deposit AVAX
    /// @param _avaxAmount The amount of AVAX to deposit
    /// @return The amount of rJOE needed
    function getRJoeAmount(uint256 _avaxAmount) public view returns (uint256) {
        return (_avaxAmount * rJoePerAvax) / 1e18;
    }

    /// @notice The total amount of liquidity pool tokens the user can withdraw
    /// @param _user The address of the user to check
    /// @return The user's balance of liquidity pool token
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
