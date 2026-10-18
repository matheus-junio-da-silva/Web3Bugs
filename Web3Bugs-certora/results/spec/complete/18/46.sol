// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC1155Burnable.spec:8-20 onlyHolderOrApprovedCanReduceBalance

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 70-73 function/modifier balanceOf
    function balanceOf(address account, uint256 id) public view virtual override returns (uint256) {
        require(account != address(0), "ERC1155: address zero is not a valid owner");
        return _balances[id][account];
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 110-112 function/modifier isApprovedForAll
    function isApprovedForAll(address account, address operator) public view virtual override returns (bool) {
        return _operatorApprovals[account][operator];
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 24-24 state declaration
    mapping(uint256 => mapping(address => uint256)) private _balances;

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 27-27 state declaration
    mapping(address => mapping(address => bool)) private _operatorApprovals;
