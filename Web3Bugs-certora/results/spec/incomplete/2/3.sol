// Extracted from: contracts/2/contracts/ProofOfReserveExecutorBase.sol
// Original source range: 24-28

  /// @dev the list of the tokens, which total supply we would check against data of the associated proof of reserve feed
  address[] internal _assets;

  /// @dev token address = > is it contained in the list
  mapping(address => bool) internal _assetsState;

// Extracted from: contracts/2/contracts/ProofOfReserveExecutorBase.sol
// Original source range: 46-54

  function enableAssets(address[] memory assets) external onlyOwner {
    for (uint256 i = 0; i < assets.length; ++i) {
      if (!_assetsState[assets[i]]) {
        _assets.push(assets[i]);
        _assetsState[assets[i]] = true;
        emit AssetStateChanged(assets[i], true);
      }
    }
  }

// Extracted from: contracts/2/contracts/ProofOfReserveExecutorV2.sol
// Original source range: 14-14

contract ProofOfReserveExecutorV2 is ProofOfReserveExecutorBase {

