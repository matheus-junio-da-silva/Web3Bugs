// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC1155Supply.spec:45-51 total_supply_is_sum_of_balances

// Original: contracts/18/contracts/token/ERC1155/extensions/ERC1155Supply.sol lines 22-24 function/modifier totalSupply
    function totalSupply(uint256 id) public view virtual returns (uint256) {
        return _totalSupply[id];
    }

// Original: contracts/18/contracts/token/ERC1155/extensions/ERC1155Supply.sol lines 29-31 function/modifier exists
    function exists(uint256 id) public view virtual returns (bool) {
        return ERC1155Supply.totalSupply(id) > 0;
    }

// Original: contracts/18/contracts/token/ERC1155/extensions/ERC1155Supply.sol lines 36-63 function/modifier _beforeTokenTransfer
    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal virtual override {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);

        if (from == address(0)) {
            for (uint256 i = 0; i < ids.length; ++i) {
                _totalSupply[ids[i]] += amounts[i];
            }
        }

        if (to == address(0)) {
            for (uint256 i = 0; i < ids.length; ++i) {
                uint256 id = ids[i];
                uint256 amount = amounts[i];
                uint256 supply = _totalSupply[id];
                require(supply >= amount, "ERC1155: burn amount exceeds totalSupply");
                unchecked {
                    _totalSupply[id] = supply - amount;
                }
            }
        }
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 429-436 function/modifier _beforeTokenTransfer
    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal virtual {}

// Original: contracts/18/contracts/mocks/ERC1155SupplyMock.sol lines 11-20 function/modifier _beforeTokenTransfer
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

// Original: contracts/18/contracts/token/ERC1155/extensions/ERC1155Supply.sol lines 17-17 state declaration
    mapping(uint256 => uint256) private _totalSupply;

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 24-24 state declaration
    mapping(uint256 => mapping(address => uint256)) private _balances;
