// Project 10 example 166; handler HBProtocol, property senderIsAlwaysCleanedUp. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/bprotocol/HBProtocol.sol original lines 12-21
    }

    function getProxyActions() public pure override returns (address) {
        return 0x351626387B5bb5408f97F8fD6B2EC415Efc9E6a1;
    }

    function getCdpManager() public pure override returns (address) {
        return 0x3f30c2381CD8B917Dd96EB2f1A4F96D91324BBed;
    }
}

// Source: contracts/10/contracts/handlers/bprotocol/HBProtocol.sol original lines 16-21
    }

    function getCdpManager() public pure override returns (address) {
        return 0x3f30c2381CD8B917Dd96EB2f1A4F96D91324BBed;
    }
}

// Source: contracts/10/contracts/Storage.sol original lines 30-45 (literal excerpt)
    modifier isNotInitialized() {
        require(_getSender() == address(0), "Sender is initialized");
        _;
    }

    function _setSender() internal isNotInitialized {
        cache.setAddress(MSG_SENDER_KEY, msg.sender);
    }

    function _resetSender() internal {
        cache.setAddress(MSG_SENDER_KEY, address(0));
    }

    function _getSender() internal view returns (address) {
        return cache.getAddress(MSG_SENDER_KEY);
    }
