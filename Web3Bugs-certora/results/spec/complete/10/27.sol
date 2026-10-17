// Source: contracts/10/specs/harnesses/Summary.sol, original lines 1090-1112
    }

    // HGelatoV2LimitOrder
    function encodeEthOrder(
        address _module,
        address _inputToken,
        address payable _owner,
        address _witness,
        bytes calldata _data,
        bytes32 _secret
    ) external pure returns (bytes memory) {
        return
            abi.encode(_module, _inputToken, _owner, _witness, _data, _secret);
    }
    function depositEth(bytes calldata _data) external payable {
        consumedToken = address(0);
        shouldBeConsumedAmount = msg.value;
    }

    address public consumedToken;
    address public generatedToken;
    uint public shouldBeConsumedAmount;
    function getBalance(address token, address who) public returns (uint) { return IERC20WithDummyFunctionality(token).balanceOf(who); }

// Source: contracts/10/specs/harnesses/DummyERC20Impl.sol, original lines 29-68
    function totalSupply() external view returns (uint256) {
        return t;
    }

    function balanceOf(address account) external view returns (uint256) {
        return b[account];
    }

    function transfer(address recipient, uint256 amount)
        external
        returns (bool)
    {
        b[msg.sender] = sub(b[msg.sender], amount);
        b[recipient] = add(b[recipient], amount);
        return true;
    }

    function allowance(address owner, address spender)
        external
        view
        returns (uint256)
    {
        return a[owner][spender];
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        a[msg.sender][spender] = amount;
        return true;
    }

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool) {
        b[sender] = sub(b[sender], amount);
        b[recipient] = add(b[recipient], amount);
        a[sender][msg.sender] = sub(a[sender][msg.sender], amount);
        return true;
    }

// Source: contracts/10/contracts/Proxy.sol, original lines 128-180
    function _execs(
        address[] memory tos,
        bytes32[] memory configs,
        bytes[] memory datas
    ) internal {
        bytes32[256] memory localStack;
        uint256 index;
        uint256 counter;

        require(
            tos.length == datas.length,
            "Tos and datas length inconsistent"
        );
        require(
            tos.length == configs.length,
            "Tos and configs length inconsistent"
        );
        for (uint256 i = 0; i < tos.length; i++) {
            address to = tos[i];
            bytes32 config = configs[i];
            bytes memory data = datas[i];
            // Check if the data contains dynamic parameter
            if (!config.isStatic()) {
                // If so, trim the exectution data base on the configuration and stack content
                _trim(data, config, localStack, index);
            }
            // Emit the execution log before call
            bytes4 selector = _getSelector(data);
            emit LogBegin(to, selector, data);

            // Check if the output will be referenced afterwards
            bytes memory result = _exec(to, data, counter);
            counter++;

            // Emit the execution log after call
            emit LogEnd(to, selector, result);

            if (config.isReferenced()) {
                // If so, parse the output and place it into local stack
                uint256 num = config.getReturnNum();
                uint256 newIndex = _parse(localStack, result, index);
                require(
                    newIndex == index + num,
                    "Return num and parsed return num not matched"
                );
                index = newIndex;
            }

            // Setup the process to be triggered in the post-process phase
            _setPostProcess(to);
        }
    }

