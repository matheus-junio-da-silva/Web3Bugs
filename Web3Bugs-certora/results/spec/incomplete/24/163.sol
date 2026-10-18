// Historical RocketJoeStaking Solidity implementation excerpts — contracts/24/contracts/RocketJoeStaking.sol
// State line 48
    uint256 public totalJoeStaked;
// State line 51
    mapping(address => UserInfo) public userInfo;
// Function emergencyWithdraw lines 154-208
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
            lastRewardTimestamp = block.timestamp;
            return;
        }
        uint256 multiplier = block.timestamp - lastRewardTimestamp;
        uint256 rJoeReward = multiplier * rJoePerSec;
        accRJoePerShare += (rJoeReward * PRECISION) / joeSupply;
        lastRewardTimestamp = block.timestamp;

        rJoe.mint(address(this), rJoeReward);
    }

    /// @notice Safe rJoe transfer function, just in case if rounding error causes pool to not have enough JOEs
    /// @param _to Address that wil receive rJoe
    /// @param _amount The amount to send
    function _safeRJoeTransfer(address _to, uint256 _amount) internal {
        uint256 rJoeBal = rJoe.balanceOf(address(this));
        if (_amount > rJoeBal) {
            IERC20Upgradeable(address(rJoe)).safeTransfer(_to, rJoeBal);
        } else {
            IERC20Upgradeable(address(rJoe)).safeTransfer(_to, _amount);
        }
    }
}

