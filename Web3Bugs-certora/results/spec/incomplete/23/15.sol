// Original: contracts/23/src/DripsHub.sol lines 159-163
    /// @param erc20 The ERC-20 token
    /// @return balance The balance of the token.
    function totalBalance(IERC20 erc20) public view returns (uint256 balance) {
        return _dripsHubStorage().totalBalances[erc20];
    }

// Original: contracts/23/src/Drips.sol lines 816-919
    /// Must be sorted, deduplicated and without 0 amtPerSecs.
    /// @param newMaxEnd The maximum end time of drips according to the new drips configuration.
    function _updateReceiverStates(
        mapping(uint256 => DripsState) storage states,
        DripsReceiver[] memory currReceivers,
        uint32 lastUpdate,
        uint32 currMaxEnd,
        DripsReceiver[] memory newReceivers,
        uint32 newMaxEnd
    //) private {
    ) internal virtual {
        //return;
        //require(currReceivers.length == 1, "Attempt to reduce computation");
        //require(newReceivers.length == 1, "Attempt to reduce computation");
        uint256 currIdx = 0;
        uint256 newIdx = 0;
        while (true) {
            bool pickCurr = currIdx < currReceivers.length;
            DripsReceiver memory currRecv;
            if (pickCurr) currRecv = currReceivers[currIdx];

            bool pickNew = newIdx < newReceivers.length;
            DripsReceiver memory newRecv;
            if (pickNew) newRecv = newReceivers[newIdx];

            // if-1
            // Limit picking both curr and new to situations when they differ only by start/end time
            if (
                pickCurr &&
                pickNew &&
                (currRecv.userId != newRecv.userId ||
                    currRecv.config.amtPerSec() != newRecv.config.amtPerSec())
            ) {
                pickCurr = _isOrdered(currRecv, newRecv);
                pickNew = !pickCurr;
            }
            
            if (pickCurr && pickNew) {
                // if-2: same userId, same amtPerSec
                // Shift the existing drip to fulfil the new configuration

                // states[currRecv.userId].amtDeltas[_currTimestamp()].thisCycle = thisCycleMapping[currRecv.userId][_currTimestamp()];
                // states[currRecv.userId].amtDeltas[_currTimestamp()].nextCycle = nextCycleMapping[currRecv.userId][_currTimestamp()];
                // states[currRecv.userId].nextReceivableCycle = nextReceivableCycleMapping[currRecv.userId];

                DripsState storage state = states[currRecv.userId];
                (uint32 currStart, uint32 currEnd) = _dripsRangeInFuture(
                    currRecv,
                    lastUpdate,
                    currMaxEnd
                );
                (uint32 newStart, uint32 newEnd) = _dripsRangeInFuture(
                    newRecv,
                    _currTimestamp(),
                    newMaxEnd
                );
                {
                    int256 amtPerSec = int256(uint256(currRecv.config.amtPerSec()));
                    // Move the start and end times if updated
                    _addDeltaRange(state, currStart, newStart, -amtPerSec);
                    _addDeltaRange(state, currEnd, newEnd, amtPerSec);
                }
                // Ensure that the user receives the updated cycles
                uint32 currStartCycle = _cycleOf(currStart);
                uint32 newStartCycle = _cycleOf(newStart);
                if (currStartCycle > newStartCycle && state.nextReceivableCycle > newStartCycle) {
                    state.nextReceivableCycle = newStartCycle;
                }
                
            } else if (pickCurr) {
                // if-3
                // Remove an existing drip
                DripsState storage state = states[currRecv.userId];
                (uint32 start, uint32 end) = _dripsRangeInFuture(currRecv, lastUpdate, currMaxEnd);
                //require (end - start == 10);
                int256 amtPerSec = int256(uint256(currRecv.config.amtPerSec()));
                _addDeltaRange(state, start, end, -amtPerSec);
                //
            } else if (pickNew) {
                // if-4
                // Create a new drip
                DripsState storage state = states[newRecv.userId];
                (uint32 start, uint32 end) = _dripsRangeInFuture(
                    newRecv,
                    _currTimestamp(),
                    newMaxEnd
                );
                int256 amtPerSec = int256(uint256(newRecv.config.amtPerSec()));
                _addDeltaRange(state, start, end, amtPerSec);
                // Ensure that the user receives the updated cycles
                uint32 startCycle = _cycleOf(start);
                if (state.nextReceivableCycle == 0 || state.nextReceivableCycle > startCycle) {
                    state.nextReceivableCycle = startCycle;
                }
                //
                
            } else {
                break;
            }

            if (pickCurr) currIdx++;
            if (pickNew) newIdx++;
        }
    }

// Original: contracts/23/src/Drips.sol lines 507-529
    /// @return balance The balance when drips have been configured for the last time
    /// @return maxEnd The current maximum end time of drips
    function _dripsState(uint256 userId, uint256 assetId)
        //internal
        public
        view
        returns (
            bytes32 dripsHash,
            bytes32 dripsHistoryHash,
            uint32 updateTime,
            uint128 balance,
            uint32 maxEnd
        )
    {
        DripsState storage state = _dripsStorage().states[assetId][userId];
        return (
            state.dripsHash,
            state.dripsHistoryHash,
            state.updateTime,
            state.balance,
            state.maxEnd
        );
    }
