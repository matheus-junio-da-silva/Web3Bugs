// Source: contracts/10/contracts/Registry.sol, original lines 9-15
contract Registry is IRegistry, Ownable {
    mapping(address => bytes32) public override handlers;
    mapping(address => bytes32) public override callers;
    mapping(address => uint256) public override bannedAgents;
    bool public override fHalt;

    bytes32 public constant DEPRECATED = bytes10(0x64657072656361746564);

// Source: contracts/10/contracts/Registry.sol, original lines 26-34
    modifier isNotHalted() {
        require(fHalt == false, "Halted");
        _;
    }

    modifier isHalted() {
        require(fHalt, "Not halted");
        _;
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
