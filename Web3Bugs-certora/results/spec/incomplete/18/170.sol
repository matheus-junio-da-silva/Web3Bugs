// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/governance/TimelockController.sol lines 33-37 (state)
    mapping(bytes32 => uint256) private _timestamps;
    uint256 private _minDelay;

    /**
     * @dev Emitted when a call is scheduled as part of operation `id`.
