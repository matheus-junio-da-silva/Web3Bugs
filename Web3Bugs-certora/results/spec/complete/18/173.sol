// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: TimelockController.spec:199-209 executeRevertsFromUnset

// Original: contracts/18/contracts/governance/TimelockController.sol lines 134-136 function/modifier isOperation
    function isOperation(bytes32 id) public view virtual returns (bool registered) {
        return getTimestamp(id) > 0;
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
