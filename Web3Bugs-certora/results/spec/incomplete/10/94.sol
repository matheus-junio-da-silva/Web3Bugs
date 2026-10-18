// Exact Solidity excerpt for HGasTokens
// Target absent: NO replacement handler source available.
// Shared dependency HandlerBase.sol lines 9-14
import "../Storage.sol";
abstract contract HandlerBase is Storage, Config {
    using SafeERC20 for IERC20;
    using LibStack for bytes32[];
