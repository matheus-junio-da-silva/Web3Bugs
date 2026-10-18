// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 97
    IJoePair public pair;
// Function initialize lines 217-271
    function initialize(
        address _issuer,
        uint256 _auctionStart,
        address _token,
        uint256 _tokenIncentivesPercent,
        uint256 _floorPrice,
        uint256 _maxWithdrawPenalty,
        uint256 _fixedWithdrawPenalty,
        uint256 _maxAllocation,
        uint256 _userTimelock,
        uint256 _issuerTimelock
    ) external atPhase(Phase.NotStarted) {
        require(auctionStart == 0, "LaunchEvent: already initialized");
        rocketJoeFactory = IRocketJoeFactory(msg.sender);
        require(
            _token != rocketJoeFactory.wavax(),
            "LaunchEvent: token is wavax"
        );

        WAVAX = IWAVAX(rocketJoeFactory.wavax());
        router = IJoeRouter02(rocketJoeFactory.router());
        factory = IJoeFactory(rocketJoeFactory.factory());
        rJoe = IRocketJoeToken(rocketJoeFactory.rJoe());
        rJoePerAvax = rocketJoeFactory.rJoePerAvax();

        require(
            _maxWithdrawPenalty <= 5e17,
            "LaunchEvent: maxWithdrawPenalty too big"
        ); // 50%
        require(
            _fixedWithdrawPenalty <= 5e17,
            "LaunchEvent: fixedWithdrawPenalty too big"
        ); // 50%
        require(
            _userTimelock <= 7 days,
            "LaunchEvent: can't lock user LP for more than 7 days"
        );
        require(
            _issuerTimelock > _userTimelock,
            "LaunchEvent: issuer can't withdraw before users"
        );
        require(
            _auctionStart > block.timestamp,
            "LaunchEvent: start of phase 1 cannot be in the past"
        );
        require(
            _issuer != address(0),
            "LaunchEvent: issuer must be address zero"
        );
        require(
            _maxAllocation > 0,
            "LaunchEvent: max allocation must not be zero"
        );
        require(
            _tokenIncentivesPercent < 1 ether,

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

