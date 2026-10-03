// Extracted from: contracts/2/contracts/ProofOfReserveExecutorBase.sol
// Original source range: 24-28

  /// @dev the list of the tokens, which total supply we would check against data of the associated proof of reserve feed
  address[] internal _assets;

  /// @dev token address = > is it contained in the list
  mapping(address => bool) internal _assetsState;

// Extracted from: contracts/2/contracts/ProofOfReserveExecutorBase.sol
// Original source range: 57-84

  function disableAssets(address[] memory assets) external onlyOwner {
    for (uint256 i = 0; i < assets.length; ++i) {
      if (_assetsState[assets[i]]) {
        _deleteAssetFromArray(assets[i]);
        delete _assetsState[assets[i]];
        emit AssetStateChanged(assets[i], false);
      }
    }
  }

  /**
   * @dev delete asset from array.
   * @param asset the address to delete
   */
  function _deleteAssetFromArray(address asset) internal {
    uint256 assetsLength = _assets.length;

    for (uint256 i = 0; i < assetsLength; ++i) {
      if (_assets[i] == asset) {
        if (i != assetsLength - 1) {
          _assets[i] = _assets[assetsLength - 1];
        }

        _assets.pop();
        break;
      }
    }
  }

// Extracted from: contracts/2/contracts/ProofOfReserveExecutorV2.sol
// Original source range: 14-14

contract ProofOfReserveExecutorV2 is ProofOfReserveExecutorBase {

