// Source: contracts/10/contracts/Registry.sol, original lines 10-13
    mapping(address => bytes32) public override handlers;
    mapping(address => bytes32) public override callers;
    mapping(address => uint256) public override bannedAgents;
    bool public override fHalt;

// Source: contracts/10/contracts/Registry.sol, original lines 139-147
    function halt() external isNotHalted onlyOwner {
        fHalt = true;
        emit Halted();
    }

    function unhalt() external isHalted onlyOwner {
        fHalt = false;
        emit Unhalted();
    }

// Source: contracts/10/contracts/Proxy.sol, original lines 40-47
    modifier isNotBanned() {
        require(registry.bannedAgents(address(this)) == 0, "Banned");
        _;
    }

    modifier isNotHalted() {
        require(registry.fHalt() == false, "Halted");
        _;

// Source: contracts/10/contracts/Proxy.sol, original lines 64-120
    fallback() external payable isNotHalted isNotBanned isInitialized {
        // If triggered by a function call, caller should be registered in
        // registry.
        // The function call will then be forwarded to the location registered
        // in registry.
        require(_isValidCaller(msg.sender), "Invalid caller");

        address target = address(bytes20(registry.callers(msg.sender)));
        bytes memory result = _exec(target, msg.data, type(uint256).max);

        // return result for aave v2 flashloan()
        uint256 size = result.length;
        assembly {
            let loc := add(result, 0x20)
            return(loc, size)
        }
    }

    /**
     * @notice Direct transfer from EOA should be reverted.
     */
    receive() external payable {
        require(Address.isContract(msg.sender), "Not allowed from EOA");
    }

    /**
     * @notice Combo execution function. Including three phases: pre-process,
     * exection and post-process.
     * @param tos The handlers of combo.
     * @param configs The configurations of executing cubes.
     * @param datas The combo datas.
     * @param ruleIndexes The indexes of rules.
     */
    function batchExec(
        address[] calldata tos,
        bytes32[] calldata configs,
        bytes[] memory datas,
        uint256[] calldata ruleIndexes
    ) external payable override isNotHalted isNotBanned {
        _preProcess(ruleIndexes);
        _execs(tos, configs, datas);
        _postProcess();
    }

    /**
     * @notice The execution interface for callback function to be executed.
     * @dev This function can only be called through the handler, which makes
     * the caller become proxy itself.
     */
    function execs(
        address[] calldata tos,
        bytes32[] calldata configs,
        bytes[] memory datas
    ) external payable override isNotHalted isNotBanned isInitialized {
        require(msg.sender == address(this), "Does not allow external calls");
        _execs(tos, configs, datas);
    }
