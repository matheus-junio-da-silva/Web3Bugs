// Original Solidity excerpt for target HOneInchExchange
// Historical handler absent: no source code is invented.
// HandlerBase.sol:9-14 (known shared base only)
import "../Storage.sol";
abstract contract HandlerBase is Storage, Config {
    using SafeERC20 for IERC20;
    using LibStack for bytes32[];
