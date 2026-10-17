// Project 10: relevant preserved Solidity excerpts; line annotations retain original provenance.
// HBalancer target itself is MISSING; the Summary is only an external-model excerpt.

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
