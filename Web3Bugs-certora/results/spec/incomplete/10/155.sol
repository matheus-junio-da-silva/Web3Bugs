// Project 10 example 155; handler HFunds, property cubeCounterIsAlwaysCleanedUp. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/funds/HFunds.sol original lines 17-42
    }

    function updateTokens(
        address[] calldata tokens
    ) external payable returns (uint256[] memory) {
        uint256[] memory balances = new uint256[](tokens.length);
        for (uint256 i = 0; i < tokens.length; ) {
            address token = tokens[i];
            if (token != address(0) && token != NATIVE_TOKEN_ADDRESS) {
                // Update involved token
                _updateToken(token);
            }
            balances[i] = _getBalance(token, type(uint256).max);
            unchecked {
                ++i;
            }
        }
        return balances;
    }

    function inject(
        address[] calldata tokens,
        uint256[] calldata amounts
    ) external payable returns (uint256[] memory) {
        return _inject(tokens, amounts);
    }

// Source: contracts/10/contracts/handlers/funds/HFunds.sol original lines 35-60
    }

    function inject(
        address[] calldata tokens,
        uint256[] calldata amounts
    ) external payable returns (uint256[] memory) {
        return _inject(tokens, amounts);
    }

    // Same as inject() and just to make another interface for different use case
    function addFunds(
        address[] calldata tokens,
        uint256[] calldata amounts
    ) external payable returns (uint256[] memory) {
        return _inject(tokens, amounts);
    }

    function sendTokens(
        address[] calldata tokens,
        uint256[] calldata amounts,
        address payable receiver
    ) external payable {
        for (uint256 i = 0; i < tokens.length; ) {
            uint256 amount = _getBalance(tokens[i], amounts[i]);
            if (amount > 0) {
                // ETH case

// Source: contracts/10/specs/harnesses/ProxyHarness.sol original lines 30-36 (literal excerpt)
        return _getSender();
    }

    function getCubeCounter() public view returns (uint256) {
        return _getCubeCounter();
    }
