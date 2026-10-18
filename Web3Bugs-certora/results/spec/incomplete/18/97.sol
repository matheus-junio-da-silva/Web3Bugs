// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/mocks/ERC721VotesMock.sol lines 6-21 (target context (no matched entrypoint))

contract ERC721VotesMock is ERC721Votes {
    constructor(string memory name, string memory symbol) ERC721(name, symbol) EIP712(name, "1") {}

    function getTotalSupply() public view returns (uint256) {
        return _getTotalSupply();
    }

    function mint(address account, uint256 tokenId) public {
        _mint(account, tokenId);
    }

    function burn(uint256 tokenId) public {
        _burn(tokenId);
    }
