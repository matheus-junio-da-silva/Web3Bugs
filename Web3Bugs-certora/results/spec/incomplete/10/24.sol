// Source: contracts/10/contracts/Storage.sol, original lines 25-45
    modifier isInitialized() {
        require(_getSender() != address(0), "Sender is not initialized");
        _;
    }

    modifier isNotInitialized() {
        require(_getSender() == address(0), "Sender is initialized");
        _;
    }

    function _setSender() internal isNotInitialized {
        cache.setAddress(MSG_SENDER_KEY, msg.sender);
    }

    function _resetSender() internal {
        cache.setAddress(MSG_SENDER_KEY, address(0));
    }

    function _getSender() internal view returns (address) {
        return cache.getAddress(MSG_SENDER_KEY);
    }

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

// Source: contracts/10/contracts/Registry.sol, original lines 129-137
    /**
     * @notice Check if the caller is valid.
     * @param caller The caller to be verified.
     */
    function isValidCaller(
        address caller
    ) external view override returns (bool) {
        return callers[caller] != 0 && callers[caller] != DEPRECATED;
    }
