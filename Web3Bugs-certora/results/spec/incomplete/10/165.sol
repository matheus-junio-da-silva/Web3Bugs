// Project 10 example 165; handler HBProtocol, property stackLengthIncreaseIsBounded. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/bprotocol/HBProtocol.sol original lines 12-21
    }

    function getProxyActions() public pure override returns (address) {
        return 0x351626387B5bb5408f97F8fD6B2EC415Efc9E6a1;
    }

    function getCdpManager() public pure override returns (address) {
        return 0x3f30c2381CD8B917Dd96EB2f1A4F96D91324BBed;
    }
}

// Source: contracts/10/contracts/handlers/bprotocol/HBProtocol.sol original lines 16-21
    }

    function getCdpManager() public pure override returns (address) {
        return 0x3f30c2381CD8B917Dd96EB2f1A4F96D91324BBed;
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
