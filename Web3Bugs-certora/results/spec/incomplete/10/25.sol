// Source: contracts/10/contracts/Storage.sol, original lines 9-14
contract Storage {
    using LibCache for mapping(bytes32 => bytes32);
    using LibStack for bytes32[];

    bytes32[] public stack;
    mapping(bytes32 => bytes32) public cache;

// Source: contracts/10/contracts/Proxy.sol, original lines 311-325
    function _setPostProcess(address to_) internal {
        // If the stack length equals 0, just skip
        // If the top is a custom post-process, replace it with the handler
        // address.
        if (stack.length == 0) {
            return;
        } else if (
            stack.peek() == bytes32(bytes12(uint96(HandlerType.Custom))) &&
            bytes4(stack.peek(1)) != 0x00000000
        ) {
            stack.pop();
            stack.setAddress(to_);
            stack.setHandlerType(HandlerType.Custom);
        }
    }

// Source: contracts/10/contracts/Proxy.sol, original lines 357-389
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
