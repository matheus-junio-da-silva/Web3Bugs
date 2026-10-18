// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: TimelockController.spec:47-49 pendingCheck

// Original: contracts/18/contracts/governance/TimelockController.sol lines 141-143 function/modifier isOperationPending
    function isOperationPending(bytes32 id) public view virtual returns (bool pending) {
        return getTimestamp(id) > _DONE_TIMESTAMP;
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 164-166 function/modifier getTimestamp
    function getTimestamp(bytes32 id) public view virtual returns (uint256 timestamp) {
        return _timestamps[id];
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 31-31 state declaration
    uint256 internal constant _DONE_TIMESTAMP = uint256(1);

// Original: contracts/18/contracts/governance/TimelockController.sol lines 33-33 state declaration
    mapping(bytes32 => uint256) private _timestamps;
