// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC1155.spec:56-60 approvalRevertCases

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 110-112 function/modifier isApprovedForAll
    function isApprovedForAll(address account, address operator) public view virtual override returns (bool) {
        return _operatorApprovals[account][operator];
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 27-27 state declaration
    mapping(address => mapping(address => bool)) private _operatorApprovals;
