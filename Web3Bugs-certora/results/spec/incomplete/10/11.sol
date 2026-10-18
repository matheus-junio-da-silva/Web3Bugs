// Source: contracts/10/contracts/Registry.sol, original lines 9-15
contract Registry is IRegistry, Ownable {
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

// Source: contracts/10/contracts/Registry.sol, original lines 106-117
    function ban(address agent) external isNotBanned(agent) onlyOwner {
        bannedAgents[agent] = 1;
        emit Banned(agent);
    }

    /**
     * @notice Unban agent from query
     */
    function unban(address agent) external isBanned(agent) onlyOwner {
        bannedAgents[agent] = 0;
        emit Unbanned(agent);
    }

// Source: contracts/10/contracts/Registry.sol, original lines 139-147
    function halt() external isNotHalted onlyOwner {
        fHalt = true;
        emit Halted();
    }

    function unhalt() external isHalted onlyOwner {
        fHalt = false;
        emit Unhalted();
    }
