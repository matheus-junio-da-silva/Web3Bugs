// Source: contracts/10/specs/harnesses/ProxyHarness.sol, original lines 22-40
    }

    function ethBalance(address who) external view returns (uint256) {
        return who.balance;
    }

    // internal-to-public
    function getSender() public view returns (address) {
        return _getSender();
    }

    function getCubeCounter() public view returns (uint256) {
        return _getCubeCounter();
    }

    // to distinguish handlers from proxy
    function isHandler() public view returns (bool) {
        return false;
    }

// Source: contracts/10/contracts/Storage.sol, original lines 13-45
    bytes32[] public stack;
    mapping(bytes32 => bytes32) public cache;

    // keccak256 hash of "msg.sender"
    // prettier-ignore
    bytes32 public constant MSG_SENDER_KEY = 0xb2f2618cecbbb6e7468cc0f2aa43858ad8d153e0280b22285e28e853bb9d453a;

    modifier isStackEmpty() {
        require(stack.length == 0, "Stack not empty");
        _;
    }

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

// Source: contracts/10/contracts/Proxy.sol, original lines 327-389
    /// @notice The pre-process phase.
    function _preProcess(
        uint256[] memory ruleIndexes_
    ) internal virtual isStackEmpty {
        // Set the sender.
        _setSender();
        // Set the fee collector
        cache._setFeeCollector(feeRuleRegistry.feeCollector());

        // Calculate fee
        uint256 feeRate = feeRuleRegistry.calFeeRateMulti(
            _getSender(),
            ruleIndexes_
        );
        require(feeRate <= PERCENTAGE_BASE, "fee rate out of range");
        cache._setFeeRate(feeRate);
        if (msg.value > 0 && feeRate > 0) {
            // Process ether fee
            uint256 feeEth = _calFee(msg.value, feeRate);

            // It will fail if fee collector is gnosis contract, because .transfer() will only consume 2300 gas limit.
            // Replacing .transfer() with .call('') to avoid out of gas
            address collector = cache._getFeeCollector();
            (bool success, ) = collector.call{value: feeEth}("");
            require(success, "Send fee to collector failed");
            emit ChargeFee(NATIVE_TOKEN, feeEth);
        }
    }

    /// @notice The post-process phase.
    function _postProcess() internal {
        // Handler type will be parsed at the beginning. Will send the token back to
        // user if the handler type is "Token". Will get the handler address and
        // execute the customized post-process if handler type is "Custom".
        while (stack.length > 0) {
            bytes32 top = stack.get();
            // Get handler type
            HandlerType handlerType = HandlerType(uint96(bytes12(top)));
            if (handlerType == HandlerType.Token) {
                address addr = address(uint160(uint256(top)));
                uint256 tokenAmount = IERC20(addr).balanceOf(address(this));
                if (tokenAmount > 0)
                    IERC20(addr).safeTransfer(msg.sender, tokenAmount);
            } else if (handlerType == HandlerType.Custom) {
                address addr = stack.getAddress();
                _exec(
                    addr,
                    abi.encodeWithSelector(POSTPROCESS_SIG),
                    type(uint256).max
                );
            } else {
                revert("Invalid handler type");
            }
        }

        // Balance should also be returned to user
        uint256 amount = address(this).balance;
        if (amount > 0) payable(msg.sender).transfer(amount);
        // Reset cached datas
        cache._resetFeeCollector();
        cache._resetFeeRate();
        _resetSender();
    }
