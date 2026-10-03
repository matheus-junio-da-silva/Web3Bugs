// Extracted from: contracts/2/contracts/ProofOfReserveAggregator.sol
// Original source range: 89-121

  function areAllReservesBacked(address[] calldata assets)
    external
    view
    returns (bool, bool[] memory)
  {
    bool[] memory unbackedAssetsFlags = new bool[](assets.length);
    bool areReservesBacked = true;

    unchecked {
      for (uint256 i = 0; i < assets.length; ++i) {
        address assetAddress = assets[i];
        address feedAddress = _proofOfReserveList[assetAddress];
        address bridgeAddress = _bridgeWrapperList[assetAddress];
        address totalSupplyAddress = bridgeAddress != address(0)
          ? bridgeAddress
          : assetAddress;

        if (feedAddress != address(0)) {
          (, int256 answer, , , ) = AggregatorV3Interface(feedAddress)
            .latestRoundData();

          if (
            answer < 0 ||
            IERC20(totalSupplyAddress).totalSupply() > uint256(answer)
          ) {
            unbackedAssetsFlags[i] = true;
            areReservesBacked = false;
          }
        }
      }
    }

    return (areReservesBacked, unbackedAssetsFlags);

