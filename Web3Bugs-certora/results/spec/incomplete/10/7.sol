// Source: contracts/10/contracts/Registry.sol, original lines 10-15
    mapping(address => bytes32) public override handlers;
    mapping(address => bytes32) public override callers;
    mapping(address => uint256) public override bannedAgents;
    bool public override fHalt;

    bytes32 public constant DEPRECATED = bytes10(0x64657072656361746564);

// Source: contracts/10/contracts/Registry.sol, original lines 51-69
    function register(address registration, bytes32 info) external onlyOwner {
        require(registration != address(0), "zero address");
        require(info != DEPRECATED, "unregistered info");
        require(handlers[registration] != DEPRECATED, "unregistered");
        handlers[registration] = info;
        emit Registered(registration, info);
    }

    /**
     * @notice Unregister a handler. The handler will be deprecated.
     * @param registration The handler to be unregistered.
     */
    function unregister(address registration) external onlyOwner {
        require(registration != address(0), "zero address");
        require(handlers[registration] != bytes32(0), "no registration");
        require(handlers[registration] != DEPRECATED, "unregistered");
        handlers[registration] = DEPRECATED;
        emit Unregistered(registration);
    }
