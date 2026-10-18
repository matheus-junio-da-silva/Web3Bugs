// Source: contracts/10/specs/harnesses/DummyERC20Impl.sol, original lines 46-57
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

// Source: contracts/10/contracts/handlers/HandlerBase.sol, original lines 109-126
    function _tokenApprove(
        address token,
        address spender,
        uint256 amount
    ) internal {
        try IERC20Usdt(token).approve(spender, amount) {} catch {
            IERC20(token).safeApprove(spender, 0);
            IERC20(token).safeApprove(spender, amount);
        }
    }

    function _tokenApproveZero(address token, address spender) internal {
        if (IERC20Usdt(token).allowance(address(this), spender) > 0) {
            try IERC20Usdt(token).approve(spender, 0) {} catch {
                IERC20Usdt(token).approve(spender, 1);
            }
        }
    }
