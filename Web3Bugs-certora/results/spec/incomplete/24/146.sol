// Historical RocketJoeStaking Solidity implementation excerpts — contracts/24/contracts/RocketJoeStaking.sol
// State line 51
    mapping(address => UserInfo) public userInfo;
// Function deposit lines 106-160
    function deposit(uint256 _amount) external {
        UserInfo storage user = userInfo[msg.sender];

        updatePool();

        uint256 pending;
        if (user.amount > 0) {
            pending =
                (user.amount * accRJoePerShare) /
                PRECISION -
                user.rewardDebt;
        }
        user.amount += _amount;
        user.rewardDebt = (user.amount * accRJoePerShare) / PRECISION;
        totalJoeStaked += _amount;

        if (_amount != 0)
            joe.safeTransferFrom(msg.sender, address(this), _amount);
        if (pending != 0) _safeRJoeTransfer(msg.sender, pending);
        emit Deposit(msg.sender, _amount);
    }

    /// @notice Withdraw JOE and accumulated rJOE from RocketJoeStaking
    /// @param _amount Amount of JOE to withdraw
    function withdraw(uint256 _amount) external {
        UserInfo storage user = userInfo[msg.sender];
        require(
            user.amount >= _amount,
            "RocketJoeStaking: withdraw amount exceeds balance"
        );

        updatePool();

        uint256 pending = (user.amount * accRJoePerShare) /
            PRECISION -
            user.rewardDebt;

        user.amount -= _amount;
        totalJoeStaked -= _amount;

        user.rewardDebt = (user.amount * accRJoePerShare) / PRECISION;

        if (pending > 0) _safeRJoeTransfer(msg.sender, pending);
        joe.safeTransfer(msg.sender, _amount);
        emit Withdraw(msg.sender, _amount);
    }

    /// @notice Withdraw without caring about rewards. EMERGENCY ONLY
    function emergencyWithdraw() external {
        UserInfo storage user = userInfo[msg.sender];

        uint256 _amount = user.amount;
        user.amount = 0;
        user.rewardDebt = 0;

