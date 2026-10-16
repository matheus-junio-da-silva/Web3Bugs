// Relevant excerpts for integrityOfWithdraw.
// Target Contract: BridgeHarness
// NOTE: BridgeHarness was the historical verification target but is absent from the supplied snapshot; excerpts below are available production-code context and may be from a later source revision.

// Source: contracts/5/contracts/l1/Bridge.sol
// Original lines: 143-205

    function withdraw(
        address l1AToken,
        uint256 l2sender,
        address recipient,
        uint256 staticAmount,
        uint256 l2RewardsIndex,
        bool toUnderlyingAsset
    ) external override {
        require(recipient != address(0), Errors.B_INVALID_ADDRESS);
        require(staticAmount > 0, Errors.B_INSUFFICIENT_AMOUNT);

        _consumeMessage(
            l1AToken,
            l2sender,
            recipient,
            staticAmount,
            l2RewardsIndex,
            toUnderlyingAsset ? 1 : 0
        );

        address underlyingAsset = address(
            _aTokenData[l1AToken].underlyingAsset
        );
        ILendingPool lendingPool = _aTokenData[l1AToken].lendingPool;
        uint256 amount = _staticToDynamicAmount(
            staticAmount,
            underlyingAsset,
            lendingPool
        );

        if (toUnderlyingAsset) {
            lendingPool.withdraw(underlyingAsset, amount, recipient);
        } else {
            IERC20(l1AToken).safeTransfer(recipient, amount);
        }

        emit Withdrawal(l1AToken, l2sender, recipient, amount);

        // update L2 state

        uint256 l1CurrentRewardsIndex = _getCurrentRewardsIndex(l1AToken);

        _sendIndexUpdateMessage(
            l1AToken,
            msg.sender,
            block.number,
            l1CurrentRewardsIndex
        );

        emit L2StateUpdated(l1AToken, l1CurrentRewardsIndex);

        // transfer rewards

        uint256 rewardsAmount = _computeRewardsDiff(
            staticAmount,
            l2RewardsIndex,
            l1CurrentRewardsIndex
        );
        if (rewardsAmount > 0) {
            _transferRewards(recipient, rewardsAmount);
            emit RewardsTransferred(l2sender, recipient, rewardsAmount);
        }
    }
