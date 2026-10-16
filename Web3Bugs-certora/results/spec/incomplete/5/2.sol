// Relevant excerpts for balanceOfUnderlyingAssetChanged.
// Target Contract: BridgeHarness
// NOTE: BridgeHarness was the historical verification target but is absent from the supplied snapshot; excerpts below are available production-code context and may be from a later source revision.

// Source: contracts/5/contracts/l1/Bridge.sol
// Original lines: 74-205

    function deposit(
        address l1AToken,
        uint256 l2Recipient,
        uint256 amount,
        uint16 referralCode,
        bool fromUnderlyingAsset
    ) external override onlyValidL2Address(l2Recipient) returns (uint256) {
        require(
            IERC20(l1AToken).balanceOf(address(this)) + amount <=
                _aTokenData[l1AToken].ceiling,
            Errors.B_ABOVE_CEILING
        );
        IERC20 underlyingAsset = _aTokenData[l1AToken].underlyingAsset;
        ILendingPool lendingPool = _aTokenData[l1AToken].lendingPool;
        require(
            underlyingAsset != IERC20(address(0)),
            Errors.B_ATOKEN_NOT_APPROVED
        );
        require(amount > 0, Errors.B_INSUFFICIENT_AMOUNT);
        // deposit aToken or underlying asset

        if (fromUnderlyingAsset) {
            underlyingAsset.safeTransferFrom(msg.sender, address(this), amount);
            lendingPool.deposit(
                address(underlyingAsset),
                amount,
                address(this),
                referralCode
            );
        } else {
            IERC20(l1AToken).safeTransferFrom(
                msg.sender,
                address(this),
                amount
            );
        }

        // update L2 state and emit deposit event

        uint256 rewardsIndex = _getCurrentRewardsIndex(l1AToken);

        uint256 staticAmount = _dynamicToStaticAmount(
            amount,
            address(underlyingAsset),
            lendingPool
        );
        uint256 l2MsgNonce = _messagingContract.l1ToL2MessageNonce();
        _sendDepositMessage(
            l1AToken,
            msg.sender,
            l2Recipient,
            staticAmount,
            block.number,
            rewardsIndex
        );
        emit Deposit(
            msg.sender,
            l1AToken,
            staticAmount,
            l2Recipient,
            block.number,
            rewardsIndex,
            l2MsgNonce
        );

        return staticAmount;
    }

    /// @inheritdoc IBridge
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

// Source: contracts/5/contracts/l1/Bridge.sol
// Original lines: 465-554

    function startDepositCancellation(
        address l1Token,
        uint256 amount,
        uint256 l2Recipient,
        uint256 rewardsIndex,
        uint256 blockNumber,
        uint256 nonce
    ) external onlyValidL2Address(l2Recipient) {
        uint256[] memory payload = new uint256[](9);
        payload[0] = uint256(uint160(msg.sender));
        payload[1] = l2Recipient;
        payload[2] = _aTokenData[l1Token].l2TokenAddress;
        (payload[3], payload[4]) = Cairo.toSplitUint(amount);
        (payload[5], payload[6]) = Cairo.toSplitUint(blockNumber);
        (payload[7], payload[8]) = Cairo.toSplitUint(rewardsIndex);

        _messagingContract.startL1ToL2MessageCancellation(
            _l2Bridge,
            Cairo.DEPOSIT_HANDLER,
            payload,
            nonce
        );
        emit StartedDepositCancellation(
            l2Recipient,
            rewardsIndex,
            blockNumber,
            amount,
            nonce
        );
    }

    /// @inheritdoc IBridge
    function cancelDeposit(
        address l1AToken,
        uint256 amount,
        uint256 l2Recipient,
        uint256 rewardsIndex,
        uint256 blockNumber,
        uint256 nonce
    ) external onlyValidL2Address(l2Recipient) {
        uint256[] memory payload = new uint256[](9);
        payload[0] = uint256(uint160(msg.sender));
        payload[1] = l2Recipient;
        payload[2] = _aTokenData[l1AToken].l2TokenAddress;
        (payload[3], payload[4]) = Cairo.toSplitUint(amount);
        (payload[5], payload[6]) = Cairo.toSplitUint(blockNumber);
        (payload[7], payload[8]) = Cairo.toSplitUint(rewardsIndex);

        _messagingContract.cancelL1ToL2Message(
            _l2Bridge,
            Cairo.DEPOSIT_HANDLER,
            payload,
            nonce
        );

        address underlyingAsset = address(
            _aTokenData[l1AToken].underlyingAsset
        );
        ILendingPool lendingPool = _aTokenData[l1AToken].lendingPool;
        uint256 dynamicAmount = _staticToDynamicAmount(
            amount,
            underlyingAsset,
            lendingPool
        );

        //transfer aTokens back to depositor
        IERC20(l1AToken).safeTransfer(msg.sender, dynamicAmount);

        //claim any accrued rewards for the depositor during the cancellation period
        uint256 currentRewardsIndex = _getCurrentRewardsIndex(l1AToken);
        uint256 rewardsAmount = _computeRewardsDiff(
            amount,
            rewardsIndex,
            currentRewardsIndex
        );

        if (rewardsAmount > 0) {
            _transferRewards(msg.sender, rewardsAmount);
            emit RewardsTransferred(_l2Bridge, msg.sender, rewardsAmount);
        }

        emit CancelledDeposit(
            l2Recipient,
            msg.sender,
            rewardsIndex,
            blockNumber,
            dynamicAmount,
            nonce
        );
    }
