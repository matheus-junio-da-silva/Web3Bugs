// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC1155.spec:710-728 cantBurnMoreBatch

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 70-73 function/modifier balanceOf
    function balanceOf(address account, uint256 id) public view virtual override returns (uint256) {
        require(account != address(0), "ERC1155: address zero is not a valid owner");
        return _balances[id][account];
    }

// Original: contracts/18/contracts/mocks/ERC1155Mock.sol lines 44-50 function/modifier burnBatch
    function burnBatch(
        address owner,
        uint256[] memory ids,
        uint256[] memory values
    ) public {
        _burnBatch(owner, ids, values);
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 366-392 function/modifier _burnBatch
    function _burnBatch(
        address from,
        uint256[] memory ids,
        uint256[] memory amounts
    ) internal virtual {
        require(from != address(0), "ERC1155: burn from the zero address");
        require(ids.length == amounts.length, "ERC1155: ids and amounts length mismatch");

        address operator = _msgSender();

        _beforeTokenTransfer(operator, from, address(0), ids, amounts, "");

        for (uint256 i = 0; i < ids.length; i++) {
            uint256 id = ids[i];
            uint256 amount = amounts[i];

            uint256 fromBalance = _balances[id][from];
            require(fromBalance >= amount, "ERC1155: burn amount exceeds balance");
            unchecked {
                _balances[id][from] = fromBalance - amount;
            }
        }

        emit TransferBatch(operator, from, address(0), ids, amounts);

        _afterTokenTransfer(operator, from, address(0), ids, amounts, "");
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 24-24 state declaration
    mapping(uint256 => mapping(address => uint256)) private _balances;
