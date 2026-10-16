// Relevant excerpts for integrityOfDepositExpanded.
// Target Contract: BridgeHarness
// NOTE: BridgeHarness was the historical verification target but is absent from the supplied snapshot; excerpts below are available production-code context and may be from a later source revision.

// Source: contracts/5/contracts/l1/Bridge.sol
// Original lines: 74-140

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

// Source: contracts/5/contracts/l1/Bridge.sol
// Original lines: 363-377

    function _dynamicToStaticAmount(
        uint256 amount,
        address asset,
        ILendingPool lendingPool
    ) internal view returns (uint256) {
        return amount.rayDiv(lendingPool.getReserveNormalizedIncome(asset));
    }

    function _staticToDynamicAmount(
        uint256 amount,
        address asset,
        ILendingPool lendingPool
    ) internal view returns (uint256) {
        return amount.rayMul(lendingPool.getReserveNormalizedIncome(asset));
    }
