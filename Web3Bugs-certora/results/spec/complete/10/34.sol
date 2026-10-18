// Project 10: relevant preserved Solidity excerpts; line annotations retain original provenance.

// Exact source excerpt: contracts/10/specs/harnesses/LibParamHarness.sol:1-24
import "../../contracts/lib/LibParam.sol";

contract LibParamHarness {
	using LibParam for bytes32;

 	bytes32 private constant REFS_MASK =
        0x00000000000000000000000000000000000000000000000000000000000000FF;
    uint256 private constant REFS_LIMIT = 22;
	
	function isStatic(bytes32 x) external returns (bool) { return x.isStatic(); }
	function isReferenced(bytes32 x) external returns (bool) { return x.isReferenced(); }
	function getReturnNum(bytes32 x) external returns (uint256) { return x.getReturnNum(); }
	function getParams(bytes32 x) external { x.getParams(); }
	function getNumOfReferences(bytes32 conf) external returns (uint256) {
		// copied from getParams()
		uint256 n = 0;
        while (conf & REFS_MASK == REFS_MASK && n < REFS_LIMIT) {
            n++;
            conf = conf >> 8;
        }
        n = REFS_LIMIT - n;
		return n;
	}
}

// Exact source excerpt: contracts/10/contracts/lib/LibParam.sol:16-54
    uint256 private constant PARAMS_SIZE_LIMIT = 64;
    uint256 private constant RETURN_NUM_OFFSET = 240;

    function isStatic(bytes32 conf) internal pure returns (bool) {
        if (conf & STATIC_MASK == 0) return true;
        else return false;
    }

    function isReferenced(bytes32 conf) internal pure returns (bool) {
        if (getReturnNum(conf) == 0) return false;
        else return true;
    }

    function getReturnNum(bytes32 conf) internal pure returns (uint256 num) {
        bytes32 temp = (conf & RETURN_NUM_MASK) >> RETURN_NUM_OFFSET;
        num = uint256(temp);
    }

    function getParams(
        bytes32 conf
    ) internal pure returns (uint256[] memory refs, uint256[] memory params) {
        require(!isStatic(conf), "Static params");
        uint256 n = REFS_LIMIT;
        while (conf & REFS_MASK == REFS_MASK && n > 0) {
            n--;
            conf = conf >> 8;
        }
        require(n > 0, "No dynamic param");
        refs = new uint256[](n);
        params = new uint256[](n);
        for (uint256 i = 0; i < n; i++) {
            refs[i] = uint256(conf & REFS_MASK);
            conf = conf >> 8;
        }
        uint256 locCount = 0;
        for (uint256 k = 0; k < PARAMS_SIZE_LIMIT; k++) {
            if (conf & PARAMS_MASK != 0) {
                require(locCount < n, "Location count exceeds ref count");
                params[locCount] = k * 32 + 4;
