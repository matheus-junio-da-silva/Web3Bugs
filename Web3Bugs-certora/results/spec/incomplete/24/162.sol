// Historical RocketJoeStaking Solidity implementation excerpts — contracts/24/contracts/RocketJoeStaking.sol
// State line 51
    mapping(address => UserInfo) public userInfo;
// Function updatePool lines 179-208
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

