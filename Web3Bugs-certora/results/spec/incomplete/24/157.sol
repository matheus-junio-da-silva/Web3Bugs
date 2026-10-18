// Historical RocketJoeStaking Solidity implementation excerpts — contracts/24/contracts/RocketJoeStaking.sol
// State line 51
    mapping(address => UserInfo) public userInfo;
// Function withdraw lines 130-184
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

        totalJoeStaked -= _amount;
        joe.safeTransfer(msg.sender, _amount);
        emit EmergencyWithdraw(msg.sender, _amount);
    }

    /// @notice Update emission rate
    /// @param _rJoePerSec The new value for rJoePerSec
    function updateEmissionRate(uint256 _rJoePerSec) external onlyOwner {
        require(
            _rJoePerSec <= MAX_EMISSION_RATE,
            "RocketJoeStaking: emission rate too high"
        );
        updatePool();
        rJoePerSec = _rJoePerSec;
        emit UpdateEmissionRate(msg.sender, _rJoePerSec);
    }

    /// @notice Update reward variables of the given pool with latest data
    function updatePool() public {
        if (block.timestamp <= lastRewardTimestamp) {
            return;
        }
        uint256 joeSupply = totalJoeStaked;
        if (joeSupply == 0) {
