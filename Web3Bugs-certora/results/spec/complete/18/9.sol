// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC1155.spec:87-103 unexpectedBalanceChange

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 70-73 function/modifier balanceOf
    function balanceOf(address account, uint256 id) public view virtual override returns (uint256) {
        require(account != address(0), "ERC1155: address zero is not a valid owner");
        return _balances[id][account];
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 117-129 function/modifier safeTransferFrom
    function safeTransferFrom(
        address from,
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) public virtual override {
        require(
            from == _msgSender() || isApprovedForAll(from, _msgSender()),
            "ERC1155: caller is not token owner nor approved"
        );
        _safeTransferFrom(from, to, id, amount, data);
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 134-146 function/modifier safeBatchTransferFrom
    function safeBatchTransferFrom(
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) public virtual override {
        require(
            from == _msgSender() || isApprovedForAll(from, _msgSender()),
            "ERC1155: caller is not token owner nor approved"
        );
        _safeBatchTransferFrom(from, to, ids, amounts, data);
    }

// Original: contracts/18/contracts/mocks/ERC1155Mock.sol lines 18-25 function/modifier mint
    function mint(
        address to,
        uint256 id,
        uint256 value,
        bytes memory data
    ) public {
        _mint(to, id, value, data);
    }

// Original: contracts/18/contracts/mocks/ERC1155Mock.sol lines 27-34 function/modifier mintBatch
    function mintBatch(
        address to,
        uint256[] memory ids,
        uint256[] memory values,
        bytes memory data
    ) public {
        _mintBatch(to, ids, values, data);
    }

// Original: contracts/18/contracts/mocks/ERC1155Mock.sol lines 36-42 function/modifier burn
    function burn(
        address owner,
        uint256 id,
        uint256 value
    ) public {
        _burn(owner, id, value);
    }

// Original: contracts/18/contracts/mocks/ERC1155Mock.sol lines 44-50 function/modifier burnBatch
    function burnBatch(
        address owner,
        uint256[] memory ids,
        uint256[] memory values
    ) public {
        _burnBatch(owner, ids, values);
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 160-187 function/modifier _safeTransferFrom
    function _safeTransferFrom(
        address from,
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) internal virtual {
        require(to != address(0), "ERC1155: transfer to the zero address");

        address operator = _msgSender();
        uint256[] memory ids = _asSingletonArray(id);
        uint256[] memory amounts = _asSingletonArray(amount);

        _beforeTokenTransfer(operator, from, to, ids, amounts, data);

        uint256 fromBalance = _balances[id][from];
        require(fromBalance >= amount, "ERC1155: insufficient balance for transfer");
        unchecked {
            _balances[id][from] = fromBalance - amount;
        }
        _balances[id][to] += amount;

        emit TransferSingle(operator, from, to, id, amount);

        _afterTokenTransfer(operator, from, to, ids, amounts, data);

        _doSafeTransferAcceptanceCheck(operator, from, to, id, amount, data);
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 24-24 state declaration
    mapping(uint256 => mapping(address => uint256)) private _balances;
