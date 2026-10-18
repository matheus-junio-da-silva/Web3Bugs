// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: TimelockController.spec:245-261 onlyProposer

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

// Original: contracts/18/contracts/governance/TimelockController.sol lines 236-252 function/modifier scheduleBatch
    function scheduleBatch(
        address[] calldata targets,
        uint256[] calldata values,
        bytes[] calldata payloads,
        bytes32 predecessor,
        bytes32 salt,
        uint256 delay
    ) public virtual onlyRole(PROPOSER_ROLE) {
        require(targets.length == values.length, "TimelockController: length mismatch");
        require(targets.length == payloads.length, "TimelockController: length mismatch");

        bytes32 id = hashOperationBatch(targets, values, payloads, predecessor, salt);
        _schedule(id, delay);
        for (uint256 i = 0; i < targets.length; ++i) {
            emit CallScheduled(id, i, targets[i], values[i], payloads[i], predecessor, delay);
        }
    }

// Original: contracts/18/contracts/access/AccessControl.sol lines 96-98 function/modifier _checkRole
    function _checkRole(bytes32 role) internal view virtual {
        _checkRole(role, _msgSender());
    }

// Original: contracts/18/contracts/access/AccessControl.sol lines 107-120 function/modifier _checkRole
    function _checkRole(bytes32 role, address account) internal view virtual {
        if (!hasRole(role, account)) {
            revert(
                string(
                    abi.encodePacked(
                        "AccessControl: account ",
                        Strings.toHexString(uint160(account), 20),
                        " is missing role ",
                        Strings.toHexString(uint256(role), 32)
                    )
                )
            );
        }
    }

// Original: contracts/18/contracts/governance/TimelockController.sol lines 28-28 state declaration
    bytes32 public constant PROPOSER_ROLE = keccak256("PROPOSER_ROLE");

// Original: contracts/18/contracts/governance/TimelockController.sol lines 221-221 state declaration
    ) public virtual onlyRole(PROPOSER_ROLE) {

// Original: contracts/18/contracts/governance/TimelockController.sol lines 243-243 state declaration
    ) public virtual onlyRole(PROPOSER_ROLE) {
