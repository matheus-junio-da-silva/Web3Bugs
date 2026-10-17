// Project 10: relevant preserved Solidity excerpts; line annotations retain original provenance.

// Exact source excerpt: contracts/10/contracts/handlers/maker/HMaker.sol:39-47
// L39:         override
// L40:         returns (string memory)
// L41:     {
// L42:         return "HMaker";
// L43:     }
// L44: 
// L45:     function getProxyActions() public pure virtual returns (address) {
// L46:         return 0x82ecD135Dce65Fbc6DbdD0e4237E0AF93FFD5038;
// L47:     }

// Exact source excerpt: contracts/10/contracts/handlers/maker/HMaker.sol:104-120
// L104:         address token = IMakerGemJoin(gemJoin).gem();
// L105: 
// L106:         // if amount == type(uint256).max return balance of Proxy
// L107:         wadC = _getBalance(token, wadC);
// L108: 
// L109:         _tokenApprove(token, address(proxy), wadC);
// L110:         try
// L111:             proxy.execute(
// L112:                 getProxyActions(),
// L113:                 abi.encodeWithSelector(
// L114:                     // selector of "openLockGemAndDraw(address,address,address,address,bytes32,uint256,uint256,bool)"
// L115:                     0xdb802a32,
// L116:                     getCdpManager(),
// L117:                     getMcdJug(),
// L118:                     gemJoin,
// L119:                     daiJoin,
// L120:                     ilk,

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
