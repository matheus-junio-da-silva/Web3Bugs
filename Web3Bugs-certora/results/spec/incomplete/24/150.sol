// Historical RocketJoeStaking Solidity implementation excerpts — contracts/24/contracts/RocketJoeStaking.sol
// State line 45
    uint256 public rJoePerSec;
// Function updateEmissionRate lines 168-208
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

