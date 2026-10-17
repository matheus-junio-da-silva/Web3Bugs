// Original Project 10 source excerpts; HBProtocol uses a different Maker actions target than HMaker.

// contracts/10/contracts/handlers/bprotocol/HBProtocol.sol:7-20
// L7: contract HBProtocol is HMaker {
// L8:     using SafeERC20 for IERC20;
// L9: 
// L10:     function getContractName() public pure override returns (string memory) {
// L11:         return "HBProtocol";
// L12:     }
// L13: 
// L14:     function getProxyActions() public pure override returns (address) {
// L15:         return 0x351626387B5bb5408f97F8fD6B2EC415Efc9E6a1;
// L16:     }
// L17: 
// L18:     function getCdpManager() public pure override returns (address) {
// L19:         return 0x3f30c2381CD8B917Dd96EB2f1A4F96D91324BBed;
// L20:     }

// contracts/10/contracts/handlers/maker/HMaker.sol:39-47
// L39:         override
// L40:         returns (string memory)
// L41:     {
// L42:         return "HMaker";
// L43:     }
// L44: 
// L45:     function getProxyActions() public pure virtual returns (address) {
// L46:         return 0x82ecD135Dce65Fbc6DbdD0e4237E0AF93FFD5038;
// L47:     }

// contracts/10/specs/harnesses/Summary.sol:77-94
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
