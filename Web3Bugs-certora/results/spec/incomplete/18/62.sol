// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/token/ERC1155/extensions/ERC1155Supply.sol lines 15-30 (target context (no matched entrypoint))
 */
abstract contract ERC1155Supply is ERC1155 {
    mapping(uint256 => uint256) private _totalSupply;

    /**
     * @dev Total amount of tokens in with a given id.
     */
    function totalSupply(uint256 id) public view virtual returns (uint256) {
        return _totalSupply[id];
    }

    /**
     * @dev Indicates whether any token exist with a given id, or not.
     */
    function exists(uint256 id) public view virtual returns (bool) {
        return ERC1155Supply.totalSupply(id) > 0;

// Original: contracts/18/contracts/mocks/ERC1155SupplyMock.sol lines 7-21 (target context (no matched entrypoint))

contract ERC1155SupplyMock is ERC1155Mock, ERC1155Supply {
    constructor(string memory uri) ERC1155Mock(uri) {}

    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal virtual override(ERC1155, ERC1155Supply) {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);
    }
}
