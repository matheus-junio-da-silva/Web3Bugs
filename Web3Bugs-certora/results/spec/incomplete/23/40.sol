// Original: contracts/23/src/Splits.sol lines 141-170
    /// on top of what was collectable before.
    /// @return splitAmt The amount split to the user's splits receivers
    function _split(
        uint256 userId,
        uint256 assetId,
        SplitsReceiver[] memory currReceivers
    ) internal returns (uint128 collectableAmt, uint128 splitAmt) {
        _assertCurrSplits(userId, currReceivers);
        mapping(uint256 => SplitsState) storage splitsStates = _splitsStorage().splitsStates;
        SplitsBalance storage balance = splitsStates[userId].balances[assetId];

        collectableAmt = balance.splittable;
        if (collectableAmt == 0) return (0, 0);

        balance.splittable = 0;
        uint32 splitsWeight = 0;
        for (uint256 i = 0; i < currReceivers.length; i++) {
            splitsWeight += currReceivers[i].weight;
            uint128 currSplitAmt = uint128(
                (uint160(collectableAmt) * splitsWeight) / _TOTAL_SPLITS_WEIGHT - splitAmt
            );
            splitAmt += currSplitAmt;
            uint256 receiver = currReceivers[i].userId;
            splitsStates[receiver].balances[assetId].splittable += currSplitAmt;
            emit Split(userId, receiver, assetId, currSplitAmt);
        }
        collectableAmt -= splitAmt;
        balance.collectable += collectableAmt;
        emit Collectable(userId, assetId, collectableAmt);
    }

// Original: contracts/23/src/Splits.sol lines 108-112
    /// @param assetId The used asset ID.
    /// @return amt The amount received but not split yet.
    function _splittable(uint256 userId, uint256 assetId) internal view returns (uint128 amt) {
        return _splitsStorage().splitsStates[userId].balances[assetId].splittable;
    }

// Original: contracts/23/src/Splits.sol lines 174-178
    /// @param assetId The used asset ID.
    /// @return amt The collectable amount.
    function _collectable(uint256 userId, uint256 assetId) internal view returns (uint128 amt) {
        return _splitsStorage().splitsStates[userId].balances[assetId].collectable;
    }
