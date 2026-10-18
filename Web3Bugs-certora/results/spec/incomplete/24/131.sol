// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 118
    uint256 private tokenIncentivesBalance;
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
