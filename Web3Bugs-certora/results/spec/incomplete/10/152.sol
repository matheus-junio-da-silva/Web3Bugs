// Project 10 example 152; handler HSCompound, property noOverwrite. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/compound/HSCompound.sol original lines 36-61
    }

    function deposit(
        address dsProxy,
        address token,
        uint256 amount
    ) external payable isDSProxyOwner(dsProxy) {
        _deposit(dsProxy, token, amount);
    }

    function withdraw(
        address dsProxy,
        address token,
        uint256 amount
    ) external payable isDSProxyOwner(dsProxy) {
        _withdraw(dsProxy, token, amount);
        if (token != NATIVE_TOKEN_ADDRESS) _updateToken(token);
    }

    function borrow(
        address dsProxy,
        address cTokenIn,
        address cTokenBorrow,
        uint256 cAmountIn,
        uint256 uBorrowAmount,
        bool needEnterMarket

// Source: contracts/10/contracts/handlers/compound/HSCompound.sol original lines 44-69
    }

    function withdraw(
        address dsProxy,
        address token,
        uint256 amount
    ) external payable isDSProxyOwner(dsProxy) {
        _withdraw(dsProxy, token, amount);
        if (token != NATIVE_TOKEN_ADDRESS) _updateToken(token);
    }

    function borrow(
        address dsProxy,
        address cTokenIn,
        address cTokenBorrow,
        uint256 cAmountIn,
        uint256 uBorrowAmount,
        bool needEnterMarket
    ) external payable isDSProxyOwner(dsProxy) {
        if (cAmountIn > 0) {
            _deposit(dsProxy, cTokenIn, cAmountIn);
        }

        if (needEnterMarket) {
            _enterMarket(dsProxy, cTokenIn);
        }

// Source: contracts/10/specs/harnesses/ProxyHarness.sol original lines 7-25 (literal excerpt)

    function getSlot(uint256 s) external view returns (uint256 x) {
        assembly {
            x := sload(s)
        }
    }

    function getStackLengthSlot() external view returns (uint256 x) {
        assembly {
            x := stack_slot
        }
    }

    function getStackLength() external view returns (uint256) {
        return stack.length;
    }

    function ethBalance(address who) external view returns (uint256) {
        return who.balance;
