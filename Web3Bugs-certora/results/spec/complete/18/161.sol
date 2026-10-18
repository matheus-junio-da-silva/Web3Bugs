// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: TimelockController.spec:41-43 operationCheck

// Original: contracts/18/contracts/governance/TimelockController.sol lines 134-136 function/modifier isOperation
    function isOperation(bytes32 id) public view virtual returns (bool registered) {
        return getTimestamp(id) > 0;
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 164-166 function/modifier getTimestamp
    function getTimestamp(bytes32 id) public view virtual returns (uint256 timestamp) {
        return _timestamps[id];
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 33-33 state declaration
    mapping(bytes32 => uint256) private _timestamps;
