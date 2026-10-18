// Source: contracts/10/contracts/Registry.sol, original lines 10-15
    mapping(address => bytes32) public override handlers;
    mapping(address => bytes32) public override callers;
    mapping(address => uint256) public override bannedAgents;
    bool public override fHalt;

    bytes32 public constant DEPRECATED = bytes10(0x64657072656361746564);

// Source: contracts/10/contracts/Registry.sol, original lines 79-100
    function registerCaller(
        address registration,
        bytes32 info
    ) external onlyOwner {
        require(registration != address(0), "zero address");
        require(info != DEPRECATED, "unregistered info");
        require(callers[registration] != DEPRECATED, "unregistered");
        callers[registration] = info;
        emit CallerRegistered(registration, info);
    }

    /**
     * @notice Unregister a caller. The caller will be deprecated.
     * @param registration The caller to be unregistered.
     */
    function unregisterCaller(address registration) external onlyOwner {
        require(registration != address(0), "zero address");
        require(callers[registration] != bytes32(0), "no registration");
        require(callers[registration] != DEPRECATED, "unregistered");
        callers[registration] = DEPRECATED;
        emit CallerUnregistered(registration);
    }
