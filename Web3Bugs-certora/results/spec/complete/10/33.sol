// Project 10: relevant preserved Solidity excerpts; line annotations retain original provenance.

// Exact source excerpt: contracts/10/specs/harnesses/LibParamHarness.sol:1-24
// L1: import "../../contracts/lib/LibParam.sol";
// L2: 
// L3: contract LibParamHarness {
// L4: 	using LibParam for bytes32;
// L5: 
// L6:  	bytes32 private constant REFS_MASK =
// L7:         0x00000000000000000000000000000000000000000000000000000000000000FF;
// L8:     uint256 private constant REFS_LIMIT = 22;
// L9: 	
// L10: 	function isStatic(bytes32 x) external returns (bool) { return x.isStatic(); }
// L11: 	function isReferenced(bytes32 x) external returns (bool) { return x.isReferenced(); }
// L12: 	function getReturnNum(bytes32 x) external returns (uint256) { return x.getReturnNum(); }
// L13: 	function getParams(bytes32 x) external { x.getParams(); }
// L14: 	function getNumOfReferences(bytes32 conf) external returns (uint256) {
// L15: 		// copied from getParams()
// L16: 		uint256 n = 0;
// L17:         while (conf & REFS_MASK == REFS_MASK && n < REFS_LIMIT) {
// L18:             n++;
// L19:             conf = conf >> 8;
// L20:         }
// L21:         n = REFS_LIMIT - n;
// L22: 		return n;
// L23: 	}
// L24: }

// Exact source excerpt: contracts/10/contracts/lib/LibParam.sol:16-54
// L16:     uint256 private constant PARAMS_SIZE_LIMIT = 64;
// L17:     uint256 private constant RETURN_NUM_OFFSET = 240;
// L18: 
// L19:     function isStatic(bytes32 conf) internal pure returns (bool) {
// L20:         if (conf & STATIC_MASK == 0) return true;
// L21:         else return false;
// L22:     }
// L23: 
// L24:     function isReferenced(bytes32 conf) internal pure returns (bool) {
// L25:         if (getReturnNum(conf) == 0) return false;
// L26:         else return true;
// L27:     }
// L28: 
// L29:     function getReturnNum(bytes32 conf) internal pure returns (uint256 num) {
// L30:         bytes32 temp = (conf & RETURN_NUM_MASK) >> RETURN_NUM_OFFSET;
// L31:         num = uint256(temp);
// L32:     }
// L33: 
// L34:     function getParams(
// L35:         bytes32 conf
// L36:     ) internal pure returns (uint256[] memory refs, uint256[] memory params) {
// L37:         require(!isStatic(conf), "Static params");
// L38:         uint256 n = REFS_LIMIT;
// L39:         while (conf & REFS_MASK == REFS_MASK && n > 0) {
// L40:             n--;
// L41:             conf = conf >> 8;
// L42:         }
// L43:         require(n > 0, "No dynamic param");
// L44:         refs = new uint256[](n);
// L45:         params = new uint256[](n);
// L46:         for (uint256 i = 0; i < n; i++) {
// L47:             refs[i] = uint256(conf & REFS_MASK);
// L48:             conf = conf >> 8;
// L49:         }
// L50:         uint256 locCount = 0;
// L51:         for (uint256 k = 0; k < PARAMS_SIZE_LIMIT; k++) {
// L52:             if (conf & PARAMS_MASK != 0) {
// L53:                 require(locCount < n, "Location count exceeds ref count");
// L54:                 params[locCount] = k * 32 + 4;
