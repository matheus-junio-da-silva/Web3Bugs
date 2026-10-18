// Project 13 example 53: original Solidity excerpt
// Source: contracts/13/contracts/mocks/certora/GovernanceActionHarness.sol
// Original lines: 92-100
            nTokenParameters
        ) = nTokenHandler.getNTokenContext(tokenAddress);
    }

    /// @notice Returns address of contract owner
    function getOwner() external view returns (address) {
        return owner;
    }
}
