// Project 13 example 52: original Solidity excerpt
// Source: contracts/13/contracts/mocks/certora/GovernanceActionHarness.sol
// Original lines: 72-100
            maxMarketIndex
        );
    }

    /// @notice Returns nToken address for a given currency
    function nTokenAddress(uint16 currencyId) external view returns (address) {
        return nTokenHandler.nTokenAddress(currencyId);
    }

    function getNTokenAccount(address tokenAddress)
        external
        view
        returns (bytes6 nTokenParameters, uint256 incentiveAnnualEmissionRate)
    {
        // prettier-ignore
        (
            /* currencyId */,
            /* totalSupply */,
            incentiveAnnualEmissionRate,
            /* lastInitializedTime */,
            nTokenParameters
        ) = nTokenHandler.getNTokenContext(tokenAddress);
    }

    /// @notice Returns address of contract owner
    function getOwner() external view returns (address) {
        return owner;
    }
}
