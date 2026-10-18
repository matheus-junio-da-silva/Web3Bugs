// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: TimelockController.spec:266-279 cooldown

// Original: contracts/18/contracts/governance/TimelockController.sol lines 148-151 function/modifier isOperationReady
    function isOperationReady(bytes32 id) public view virtual returns (bool ready) {
        uint256 timestamp = getTimestamp(id);
        return timestamp > _DONE_TIMESTAMP && timestamp <= block.timestamp;
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 173-175 function/modifier getMinDelay
    function getMinDelay() public view virtual returns (uint256 duration) {
        return _minDelay;
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 214-225 function/modifier schedule
    function schedule(
        address target,
        uint256 value,
        bytes calldata data,
        bytes32 predecessor,
        bytes32 salt,
        uint256 delay
    ) public virtual onlyRole(PROPOSER_ROLE) {
        bytes32 id = hashOperation(target, value, data, predecessor, salt);
        _schedule(id, delay);
        emit CallScheduled(id, 0, target, value, data, predecessor, delay);
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 33-33 state declaration
    mapping(bytes32 => uint256) private _timestamps;

// Original: contracts/18/contracts/governance/TimelockController.sol lines 34-34 state declaration
    uint256 private _minDelay;
