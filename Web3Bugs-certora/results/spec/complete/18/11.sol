// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC1155.spec:117-129 balanceOfBatchRevertCases

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 82-98 function/modifier balanceOfBatch
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
            batchBalances[i] = balanceOf(accounts[i], ids[i]);
        }

        return batchBalances;
    }

// Original: contracts/18/contracts/token/ERC1155/ERC1155.sol lines 24-24 state declaration
    mapping(uint256 => mapping(address => uint256)) private _balances;
