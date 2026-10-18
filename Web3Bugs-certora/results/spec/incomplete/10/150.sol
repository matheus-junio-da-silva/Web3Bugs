// Project 10 example 150; handler HSCompound, property cacheIsAlwaysCleanedUp. Historical source excerpts only, NOT compilable assembly.
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
