// Project 10 example 156; handler HFunds, property cacheIsAlwaysCleanedUp. Historical source excerpts only, NOT compilable assembly.
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

// Source: contracts/10/contracts/Storage.sol original lines 8-18 (literal excerpt)
/// @notice A cache structure composed by a bytes32 array
contract Storage {
    using LibCache for mapping(bytes32 => bytes32);
    using LibStack for bytes32[];

    bytes32[] public stack;
    mapping(bytes32 => bytes32) public cache;

    // keccak256 hash of "msg.sender"
    // prettier-ignore
    bytes32 public constant MSG_SENDER_KEY = 0xb2f2618cecbbb6e7468cc0f2aa43858ad8d153e0280b22285e28e853bb9d453a;

// Source: contracts/10/contracts/Storage.sol original lines 30-45 (literal excerpt)
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
