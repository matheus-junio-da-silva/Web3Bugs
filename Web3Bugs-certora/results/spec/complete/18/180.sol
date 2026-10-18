// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: TimelockController.spec:315-323 cancelChange

// Original: contracts/18/contracts/governance/TimelockController.sol lines 164-166 function/modifier getTimestamp
    function getTimestamp(bytes32 id) public view virtual returns (uint256 timestamp) {
        return _timestamps[id];
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 270-275 function/modifier cancel
    function cancel(bytes32 id) public virtual onlyRole(CANCELLER_ROLE) {
        require(isOperationPending(id), "TimelockController: operation cannot be cancelled");
        delete _timestamps[id];

        emit Cancelled(id);
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 31-31 state declaration
    uint256 internal constant _DONE_TIMESTAMP = uint256(1);

// Original: contracts/18/contracts/governance/TimelockController.sol lines 33-33 state declaration
    mapping(bytes32 => uint256) private _timestamps;
