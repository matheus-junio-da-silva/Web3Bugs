// Project 10 example 189; handler HComptroller, property stackLengthIncreaseIsBounded. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/compound/HComptroller.sol original lines 17-42
    }

    function claimComp() external payable returns (uint256) {
        IComptroller comptroller = IComptroller(COMPTROLLER);
        address comp = comptroller.getCompAddress();
        address sender = _getSender();

        uint256 beforeCompBalance = IERC20(comp).balanceOf(sender);
        try comptroller.claimComp(sender) {} catch Error(string memory reason) {
            _revertMsg("claimComp", reason);
        } catch {
            _revertMsg("claimComp");
        }
        uint256 afterCompBalance = IERC20(comp).balanceOf(sender);

        return afterCompBalance - beforeCompBalance;
    }

    function claimComp(address holder) external payable returns (uint256) {
        IComptroller comptroller = IComptroller(COMPTROLLER);
        address comp = comptroller.getCompAddress();

        uint256 beforeCompBalance = IERC20(comp).balanceOf(holder);
        try comptroller.claimComp(holder) {} catch Error(string memory reason) {
            _revertMsg("claimComp", reason);
        } catch {

// Source: contracts/10/contracts/handlers/compound/HComptroller.sol original lines 33-49
    }

    function claimComp(address holder) external payable returns (uint256) {
        IComptroller comptroller = IComptroller(COMPTROLLER);
        address comp = comptroller.getCompAddress();

        uint256 beforeCompBalance = IERC20(comp).balanceOf(holder);
        try comptroller.claimComp(holder) {} catch Error(string memory reason) {
            _revertMsg("claimComp", reason);
        } catch {
            _revertMsg("claimComp");
        }
        uint256 afterCompBalance = IERC20(comp).balanceOf(holder);

        return afterCompBalance - beforeCompBalance;
    }
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
