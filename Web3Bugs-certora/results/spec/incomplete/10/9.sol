// Source: contracts/10/contracts/Registry.sol, original lines 9-15
contract Registry is IRegistry, Ownable {
    mapping(address => bytes32) public override handlers;
    mapping(address => bytes32) public override callers;
    mapping(address => uint256) public override bannedAgents;
    bool public override fHalt;

    bytes32 public constant DEPRECATED = bytes10(0x64657072656361746564);

// Source: contracts/10/contracts/Registry.sol, original lines 36-44
    modifier isNotBanned(address agent) {
        require(bannedAgents[agent] == 0, "Banned");
        _;
    }

    modifier isBanned(address agent) {
        require(bannedAgents[agent] != 0, "Not banned");
        _;
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
