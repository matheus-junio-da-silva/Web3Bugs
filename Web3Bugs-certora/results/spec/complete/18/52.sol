// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/token/ERC1155/extensions/ERC1155Pausable.sol lines 17-32 (target context (no matched entrypoint))
 */
abstract contract ERC1155Pausable is ERC1155, Pausable {
    /**
     * @dev See {ERC1155-_beforeTokenTransfer}.
     *
     * Requirements:
     *
     * - the contract must not be paused.
     */
    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data

// Original: contracts/18/contracts/mocks/ERC1155PausableMock.sol lines 7-22 (target context (no matched entrypoint))

contract ERC1155PausableMock is ERC1155Mock, ERC1155Pausable {
    constructor(string memory uri) ERC1155Mock(uri) {}

    function pause() external {
        _pause();
    }

    function unpause() external {
        _unpause();
    }

    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 70-93 (callable)
    function balanceOf(address account, uint256 id) public view virtual override returns (uint256) {
        require(account != address(0), "ERC1155: address zero is not a valid owner");
        return _balances[id][account];
    }

    /**
     * @dev See {IERC1155-balanceOfBatch}.
     *
     * Requirements:
     *
     * - `accounts` and `ids` must have the same length.
     */
    function balanceOfBatch(address[] memory accounts, uint256[] memory ids)
        public
        view
        virtual
        override
        returns (uint256[] memory)
    {
        require(accounts.length == ids.length, "ERC1155: accounts and ids length mismatch");

        uint256[] memory batchBalances = new uint256[](accounts.length);

        for (uint256 i = 0; i < accounts.length; ++i) {
