// Project 10 example 177; handler HCEther, property stackLengthIncreaseIsBounded. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/compound/HCEther.sol original lines 16-41
    }

    function mint(uint256 value) external payable returns (uint256) {
        ICEther compound = ICEther(CETHER);

        // Get cether balance of proxy before mint
        uint256 beforeCEtherAmount = compound.balanceOf(address(this));

        // if amount == type(uint256).max return balance of Proxy
        value = _getBalance(address(0), value);

        // Execute mint
        try compound.mint{value: value}() {} catch Error(string memory reason) {
            _revertMsg("mint", reason);
        } catch {
            _revertMsg("mint");
        }

        // Get cether balance of proxy after mint
        uint256 afterCEtherAmount = compound.balanceOf(address(this));

        // Update involved token
        _updateToken(CETHER);
        return (afterCEtherAmount - beforeCEtherAmount);
    }


// Source: contracts/10/contracts/handlers/compound/HCEther.sol original lines 40-65
    }

    function redeem(uint256 redeemTokens) external payable returns (uint256) {
        // Get ether balance of proxy before redeem
        uint256 beforeRedeemAmount = address(this).balance;

        // Approve cether
        ICEther compound = ICEther(CETHER);

        // if amount == type(uint256).max return balance of Proxy
        redeemTokens = _getBalance(CETHER, redeemTokens);

        // Execute redeem
        try compound.redeem(redeemTokens) returns (uint256 errorCode) {
            _requireMsg(
                errorCode == 0,
                "redeem",
                string(abi.encodePacked("error ", _uint2String(errorCode)))
            );
        } catch Error(string memory reason) {
            _revertMsg("redeem", reason);
        } catch {
            _revertMsg("redeem");
        }

        // Get ether balance of proxy after redeem

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
