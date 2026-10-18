// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC1155.spec:65-76 onlyOneAllowanceChange

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 103-105 function/modifier setApprovalForAll
    function setApprovalForAll(address operator, bool approved) public virtual override {
        _setApprovalForAll(_msgSender(), operator, approved);
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 110-112 function/modifier isApprovedForAll
    function isApprovedForAll(address account, address operator) public view virtual override returns (bool) {
        return _operatorApprovals[account][operator];
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 27-27 state declaration
    mapping(address => mapping(address => bool)) private _operatorApprovals;
