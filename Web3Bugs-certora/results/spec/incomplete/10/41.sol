// Historical target HAaveProtocol; exact Solidity excerpt
// Historical HAaveProtocol.sol absent: no replacement code; HandlerBase.sol is a shared known dependency.
// Source: contracts/10/contracts/handlers/HandlerBase.sol lines 9-14
import "../Storage.sol";

abstract contract HandlerBase is Storage, Config {
    using SafeERC20 for IERC20;
    using LibStack for bytes32[];
