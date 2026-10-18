// Project 10 example 261; handler HYVault, property stackLengthIncreaseIsBounded. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/yearn/HYVault.sol original lines 14-39
    }

    function deposit(
        address vault,
        uint256 _amount
    ) external payable returns (uint256) {
        IYVault yVault = IYVault(vault);
        uint256 beforeYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );

        address token = yVault.token();
        // if amount == type(uint256).max return balance of Proxy
        _amount = _getBalance(token, _amount);
        _tokenApprove(token, address(yVault), _amount);
        try yVault.deposit(_amount) {} catch Error(string memory reason) {
            _revertMsg("deposit", reason);
        } catch {
            _revertMsg("deposit");
        }
        _tokenApproveZero(token, address(yVault));

        uint256 afterYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );


// Source: contracts/10/contracts/handlers/yearn/HYVault.sol original lines 42-67
    }

    function depositETH(
        uint256 value,
        address vault
    ) external payable returns (uint256) {
        IYVault yVault = IYVault(vault);
        uint256 beforeYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );
        // if amount == type(uint256).max return balance of Proxy
        value = _getBalance(address(0), value);
        try yVault.depositETH{value: value}() {} catch Error(
            string memory reason
        ) {
            _revertMsg("depositETH", reason);
        } catch {
            _revertMsg("depositETH");
        }
        uint256 afterYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );

        _updateToken(address(yVault));
        return afterYTokenBalance - beforeYTokenBalance;
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

// Source: contracts/10/contracts/handlers/HandlerBase.sol original lines 30-53 (literal excerpt)

    function _updateToken(address token) internal {
        stack.setAddress(token);
        // Ignore token type to fit old handlers
        // stack.setHandlerType(uint256(HandlerType.Token));
    }

    function _updatePostProcess(bytes32[] memory params) internal {
        for (uint256 i = params.length; i > 0; i--) {
            stack.set(params[i - 1]);
        }
        stack.set(msg.sig);
        stack.setHandlerType(HandlerType.Custom);
    }

    function getContractName() public pure virtual returns (string memory);

    function _revertMsg(
        string memory functionName,
        string memory reason
    ) internal pure {
        revert(
            string(
                abi.encodePacked(
