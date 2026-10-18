// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: TimelockController.spec:214-225 executeRevertsEffectCheck

// Original: contracts/18/contracts/governance/TimelockController.sol lines 141-143 function/modifier isOperationPending
    function isOperationPending(bytes32 id) public view virtual returns (bool pending) {
        return getTimestamp(id) > _DONE_TIMESTAMP;
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 148-151 function/modifier isOperationReady
    function isOperationReady(bytes32 id) public view virtual returns (bool ready) {
        uint256 timestamp = getTimestamp(id);
        return timestamp > _DONE_TIMESTAMP && timestamp <= block.timestamp;
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 289-302 function/modifier execute
    function execute(
        address target,
        uint256 value,
        bytes calldata payload,
        bytes32 predecessor,
        bytes32 salt
    ) public payable virtual onlyRoleOrOpenRole(EXECUTOR_ROLE) {
        bytes32 id = hashOperation(target, value, payload, predecessor, salt);

        _beforeCall(id, predecessor);
        _execute(target, value, payload);
        emit CallExecuted(id, 0, target, value, payload);
        _afterCall(id);
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 31-31 state declaration
    uint256 internal constant _DONE_TIMESTAMP = uint256(1);

// Original: contracts/18/contracts/governance/TimelockController.sol lines 33-33 state declaration
    mapping(bytes32 => uint256) private _timestamps;
