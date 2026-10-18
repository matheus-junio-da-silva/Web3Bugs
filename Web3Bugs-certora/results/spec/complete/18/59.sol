// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC1155Pausable.spec:97-105 whenPausedModifierCausesRevertIfUnpaused

// Original: contracts/18/contracts/token/ERC1155/extensions/ERC1155Pausable.sol lines 26-37 function/modifier _beforeTokenTransfer
    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal virtual override {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);

        require(!paused(), "ERC1155Pausable: token transfer while paused");
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

// Original: contracts/18/contracts/mocks/ERC1155PausableMock.sol lines 19-28 function/modifier _beforeTokenTransfer
    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal virtual override(ERC1155, ERC1155Pausable) {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);
    }
