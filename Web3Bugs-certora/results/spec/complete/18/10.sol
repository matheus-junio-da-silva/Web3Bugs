// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 19-34 (target context (no matched entrypoint))
 */
contract ERC1155 is Context, ERC165, IERC1155, IERC1155MetadataURI {
    using Address for address;

    // Mapping from token ID to account balances
    mapping(uint256 => mapping(address => uint256)) private _balances;

    // Mapping from account to operator approvals
    mapping(address => mapping(address => bool)) private _operatorApprovals;

    // Used as the URI for all token types by relying on ID substitution, e.g. https://token-cdn-domain/{id}.json
    string private _uri;

    /**
     * @dev See {_setURI}.
     */

// Original: contracts/18/contracts/mocks/ERC1155Mock.sol lines 10-25 (target context (no matched entrypoint))
 */
contract ERC1155Mock is ERC1155 {
    constructor(string memory uri) ERC1155(uri) {}

    function setURI(string memory newuri) public {
        _setURI(newuri);
    }

    function mint(
        address to,
        uint256 id,
        uint256 value,
        bytes memory data
    ) public {
        _mint(to, id, value, data);
    }
