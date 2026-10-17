// Project 10: relevant preserved Solidity excerpts; line annotations retain original provenance.

// Exact source excerpt: contracts/10/contracts/handlers/compound/HSCompound.sol:13-18
// L13:     using SafeERC20 for IERC20;
// L14: 
// L15:     // prettier-ignore
// L16:     address public constant FCOMPOUND_ACTIONS = 0x05EF8eb657027927fAB9b279138f0189CB144976;
// L17:     // prettier-ignore
// L18:     address public constant COMPTROLLER = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;

// Exact source excerpt: contracts/10/contracts/handlers/compound/HSCompound.sol:75-92
// L75:             } else {
// L76:                 underlying = _getToken(cTokenBorrow);
// L77:             }
// L78:             // Execute borrow, borrowed token will stay in the DSProxy
// L79:             try
// L80:                 IDSProxy(dsProxy).execute(
// L81:                     FCOMPOUND_ACTIONS,
// L82:                     abi.encodeWithSelector(
// L83:                         // selector of "borrow(address,uint256)"
// L84:                         0x4b8a3529,
// L85:                         cTokenBorrow,
// L86:                         uBorrowAmount
// L87:                     )
// L88:                 )
// L89:             {} catch Error(string memory reason) {
// L90:                 _revertMsg("borrow", reason);
// L91:             } catch {
// L92:                 _revertMsg("borrow");

// Exact source excerpt: contracts/10/specs/harnesses/Summary.sol:77-94
// L77:     // for HMaker, HSCompound
// L78:     address[] delegated;
// L79:     function lenDelegated() external returns (uint256) { return delegated.length; }
// L80:     function checkDelegated(address allowed) external returns (bool) {
// L81:         for (uint i = 0 ; i < delegated.length; i++) {
// L82:             if (delegated[i] != allowed) {
// L83:                 return false;
// L84:             }
// L85:         }
// L86: 
// L87:         return true;
// L88:     }
// L89: 
// L90:     function execute(address a, bytes calldata b) external payable returns (bytes32) {
// L91:         delegated.push(a);
// L92:         havocDummyToken();
// L93:         return executeRet;
// L94:     }
